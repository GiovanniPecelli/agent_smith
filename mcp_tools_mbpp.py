#!/usr/bin/env python3
"""MCP Server for MBPP - provides run_tests tool."""
import io
import json
import signal
import sys
from contextlib import redirect_stderr, redirect_stdout


def _timeout_handler(signum, frame):
    """
    Python’s internal C runtime (signal module) supplies those two arguments
    automatically at the exact moment the OS kernel delivers the signal.
    """
    raise TimeoutError("Test execution timed out")


def run_tests(
    code: str,
    test_list: list[str],
    timeout_seconds: int = 10
) -> dict:
    """
    Execute code against test assertions.
    Returns JSON-serializable dict.

    NOTE creaiamo 2 buffer con StringIO() salvate in memoria cosi da rendere
    l'output stderr e stderr consultabile: senza i buffer l'output sparisce
    nel terminale del server, l'LLM non riceve feedback.
    """

    # namespace for exec
    namespace: dict = {}
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    def _with_captured_output(message: str) -> str:
        out = stdout_buf.getvalue().strip()
        err = stderr_buf.getvalue().strip()
        parts = [message]
        if out:
            parts.append(f"Stdout:\n{out}")
        if err:
            parts.append(f"Stderr:\n{err}")
        return "\n".join(parts)

    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout_seconds)

    try:
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            # define the function
            exec(code, namespace)
            for test in test_list:
                exec(test, namespace)

        return {
            "success": True,
            "output": _with_captured_output("All tests passed")
        }
    except TimeoutError as e:
        return {
            "success": False,
            "output": _with_captured_output(str(e))
        }
    except AssertionError as e:
        return {
            "success": False,
            "output": _with_captured_output(f"Assertion failed: {e}")
        }
    except Exception as e:
        return {
            "success": False,
            "output": _with_captured_output(f"{type(e).__name__}: {e}")
        }
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)

def handle_initialize(req_id: int) -> dict:
    """Handle initialize request - return server capabilities."""
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "mcp-tools-mbpp",
                "version": "0.1.0"
            }
        }
    }


def handle_tools_list(req_id: int) -> dict:
    """Return available tools for tools/list request."""
    schema = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Python code to test"},
            "test_list": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of test assertions"
            }
        },
        "required": ["code", "test_list"]
    }
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "tools": [
                {
                    "name": "run_tests",
                    "description": "Execute code against test assertions",
                    "inputSchema": schema
                }
            ]
        }
    }


def handle_tools_call(req_id: int, params: dict) -> dict:
    """Execute a tool call for tools/call request."""
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    if not isinstance(arguments, dict):
        return error_response(
            req_id,
            -32602,
            "Invalid params: 'arguments' must be an object"
        )

    if tool_name == "run_tests":
        code = arguments.get("code", "")
        test_list = arguments.get("test_list", [])

        if not isinstance(code, str) or not isinstance(test_list, list):
            return error_response(req_id, -32602, "Invalid params")

        result = run_tests(code, test_list)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result),
                    }
                ],
                "isError": not result.get("success", False),
            },
        }

    return error_response(req_id, -32601, f"Unknown tool: {tool_name}")


def error_response(req_id: int, code: int, message: str) -> dict:
    """Standard JSON-RPC error response."""
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def main():
    # JSON-RPC loop su stdin/stdout
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError as e:
            # -32700 is the official standard code for Parse Error
            # defined in the JSON-RPC 2.0 specification
            response = error_response(None, -32700, f"Parse error: {e}")
            print(json.dumps(response), flush=True)
            continue

        if not isinstance(request, dict):
            response = error_response(
                None,
                -32600,
                "Invalid Request: expected JSON object"
            )
            print(json.dumps(response), flush=True)
            continue

        method = request.get("method") or ""
        req_id = request.get("id")
        params = request.get("params", {})

        if not isinstance(method, str) or not isinstance(params, dict):
            response = error_response(req_id, -32600, "Invalid Request")
            print(json.dumps(response), flush=True)
            continue

        # JSON-RPC notifications (no 'id') must not receive a response
        if req_id is None or method.startswith("notifications/"):
            continue

        if method == "initialize":
            response = handle_initialize(req_id)
        elif method == "tools/list":
            response = handle_tools_list(req_id)
        elif method == "tools/call":
            response = handle_tools_call(req_id, params)
        else:
            response = error_response(req_id, -32601, "Method not found")

        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
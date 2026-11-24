#!/usr/bin/env python3
"""MCP Server for MBPP - provides run_tests tool."""
from contextlib import redirect_stdout, redirect_stderr

import json
import sys
import io


def run_tests(code: str, test_list: list) -> dict:
    """
    Execute code against test assertions.
    Returns JSON-serializable dict.

    NOTE creaiamo 2 buffer con StringIO() salvate in memoria cosi da rendere
    l'output stderr e stderr consultabile: senza i buffer l'output sparisce
    nel terminale del server, l'LLM non riceve feedback.
    """
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    # namespace for exec
    namespace = {}

    try:
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            # define the function
            exec(code, namespace)

            for test in test_list:
                exec(test, namespace)

        return {"success": True, "output": "All tests passed"}
    except AssertionError as e:
        return {"success": False, "output": f"Assertion failed: {e}"}
    except Exception as e:
        return {"success": False, "output": f"{type(e).__name__}: {e}"}


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

    if tool_name == "run_tests":
        code = arguments.get("code", "")
        test_list = arguments.get("test_list", [])
        result = run_tests(code, test_list)
        return {"jsonrpc": "2.0", "id": req_id, "result": result}

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
        request = json.loads(line)

        method = request.get("method")
        req_id = request.get("id")
        params = request.get("params", {})

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
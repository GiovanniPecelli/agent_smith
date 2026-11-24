from pathlib import Path
import subprocess
import argparse
import json
import sys

from src.sandbox import Sandbox, SandboxExecutionResult
from src.models import SandboxConfig


def mcp_initialize(mcp_proc: subprocess.Popen) -> dict:
    """Send initialize request and return server response."""
    request = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "agent-smith", "version": "0.1.0"}
        }
    }
    # Serialize request to JSON and add newline delimiter for JSON-RPC
    mcp_proc.stdin.write(json.dumps(request) + "\n")
    # Force immediate send - flush Python buffer so server receives it now
    mcp_proc.stdin.flush()
    # Block until server writes a complete line (JSON response) on its stdout
    response_line = mcp_proc.stdout.readline()
    # Parse JSON response string back to Python dict
    return json.loads(response_line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Smith Sandbox REPL")

    parser.add_argument(
        "config_file", nargs="?", default=None,
        help="Path to sandbox config JSON"
    )

    # MCP stdio mode
    parser.add_argument(
        "--mcp-stdio", metavar="COMMAND",
        help="MCP server command (stdio mode)"
    )

    # MCP HTTP mode
    parser.add_argument(
        "--mcp-server", metavar="URL",
        help="MCP server URL (HTTP mode)"
    )

    args = parser.parse_args()

    # IF the user provides a specific config_file
    if args.config_file:
        with open(args.config_file) as f:
            config_data = json.load(f)

        # Using SandboxConfig validates the configuration via Pydantic,
        # ensuring alternative configs are valid/compatible.
        config = SandboxConfig(**config_data)
    else:
        config = SandboxConfig()

    sandbox = Sandbox(config)

    # MCP connection if required
    if args.mcp_stdio:
        # start MCP process - Popen runs the process in background
        # mcp_proc is a child process who rapresent the server MCP
        mcp_proc = subprocess.Popen(
            args.mcp_stdio,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Handshake: initialize + tools/list
        init_resp = mcp_initialize(mcp_proc)
        print(f"[MCP] Initialized: {init_resp}", file=sys.stderr)

    # REPL loop
    print("Agent Smith Sandbox REPL. Type 'exit' or Ctrl+D to quit.")
    print("Type 'reset' to clear namespace.")

    while True:
        try:
            code = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if code.strip() == "exit":
            break
        if code.strip() == "reset":
            sandbox.reset()
            print("[namespace reset]")
            continue

        result: SandboxExecutionResult = sandbox.execute(code)

        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        if result.error:
            print(f"Error: {result.error}", file=sys.stderr)
        if result.is_final:
            print(f"[FINAL ANSWER] {result.final_answer}")
            break


if __name__ == "__main__":
    sys.exit(main())
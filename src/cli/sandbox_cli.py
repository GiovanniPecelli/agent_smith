from pathlib import Path
import subprocess
import argparse
import json
import sys

from src.sandbox import Sandbox, SandboxExecutionResult
from src.models import SandboxConfig

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

    # IF the use provide a specific config_file
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
        # start MCP process - Popen run the process in background
        mcp_proc = subprocess.Popen(
            args.mcp_stdio,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # TODO: handshake MCP, scopri tool, registrali con sandbox.register_tool()

        print(f"[MCP] Started: {args.mcp_stdio}", file=sys.stderr)

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
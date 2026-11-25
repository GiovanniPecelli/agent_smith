.PHONY: help lint clean clean-venv sandbox sandbox-mcp mcp-test

help:
	@echo "Available targets:"
	@echo "  lint        - Run ruff linter"
	@echo "  clean       - Remove cache files"
	@echo "  clean-venv  - Remove .venv"
	@echo "  sandbox     - Run interactive sandbox REPL"
	@echo "  sandbox-mcp - Run sandbox with MCP MBPP server"
	@echo "  mcp-test    - Test MCP server manually"

lint:
	uv run ruff check .

clean:
	python3 -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.pytest_cache')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.ruff_cache')]; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]" 2>/dev/null || python -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.pytest_cache')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.ruff_cache')]; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"

clean-venv:
	python3 -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)" 2>/dev/null || python -c "import shutil; shutil.rmtree('.venv', ignore_errors=True)" 2>/dev/null || rm -rf .venv

sandbox:
	uv run sandbox

sandbox-mcp:
	uv run sandbox --mcp-stdio "python mcp_tools_mbpp.py" config/sandbox_config.json

mcp-test:
	echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python mcp_tools_mbpp.py
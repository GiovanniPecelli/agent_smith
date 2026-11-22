# Task Board & Progress Tracking

> Practical Kanban-style checklist for team tasks, statuses, and deliverables.

---

## 🟢 Shared / Setup Phase
- [x] Configure Python 3.10 and `uv` project (`pyproject.toml`)
- [x] Create project models in `src/models/` (`SandboxConfig`, `StepMetrics`, `SolutionOutput`, tasks)
- [x] Configure API keys in `.env` and catalogue in `config/models_config.json`
- [x] Define architecture, roadmap, and team contracts

---

## 🛡️ Gpecelli's Tasks (Sandbox & Tools)

### Milestone 1: Sandbox Security Engine (`src/sandbox/sandbox.py`)
- [ ] Implement `_is_import_authorized` (handling wildcard pattern matching)
- [ ] Implement `_safe_import` (hooking `__import__` with allowlist enforcement)
- [ ] Implement `_is_path_allowed` & `_safe_open` (path resolution and directory boundary)
- [ ] Implement `_block_network` (blocking raw socket calls)
- [ ] Implement `_apply_memory_limit` (via `resource.RLIMIT_AS`)
- [ ] Implement `_final_answer` & `FinalAnswerException`
- [ ] Implement `execute` with timeout enforcement (`signal.alarm`), stdout capture, and zero silent failures
- [ ] Implement namespace variable persistence across steps

### Milestone 2: Sandbox REPL CLI (`src/cli/sandbox_cli.py`)
- [ ] Implement interactive REPL loop for `uv run sandbox`
- [ ] Support `--mcp-stdio` and `--mcp-server` arguments
- [ ] Support custom configuration JSON files

### Milestone 3: MCP Servers (`mcp_tools_*.py`)
- [ ] Create `mcp_tools_mbpp.py` (implementing `run_tests`)
- [ ] Create `mcp_tools_swebench.py` (reading `TESTBED_PATH`):
  - [ ] File system tools: `read_file`, `edit_file`, `list_files`
  - [ ] Code search tools: `search_code`, `search_function_or_class_definition_in_code`, `find_references`
  - [ ] Execution tools: `run_tests`, `get_patch`, `run_command`
- [ ] Validate against `exam_sandbox.sh`

---

## 🧠 Gipimpin's Tasks (Agent & LLM Orchestrator)

### Milestone 1: LLM Client (`src/agent/llm_client.py`)
- [ ] Implement HTTP client for OpenRouter, Google Gemini, and Groq endpoints
- [ ] Implement multi-token rotation upon receiving HTTP 429 (Rate Limit)
- [ ] Compute and record per-request metrics (`input_tokens`, `output_tokens`, `latency_ms`, `retries`)

### Milestone 2: Extraction Layer & Prompts (`src/agent/`)
- [ ] Implement `src/agent/extraction.py` supporting Markdown, XML, JSON, and ReAct formats
- [ ] Implement `src/agent/prompts.py` (system prompt with slots: Thought, Code, Observation)
- [ ] Dynamic tool manual generator from connected MCP schema

### Milestone 3: Agent Orchestrator & CLI Runners (`src/agent/`, `src/cli/`)
- [ ] Implement `src/agent/orchestrator.py` (the Thought ➔ Code ➔ Observation loop)
- [ ] Enforce cumulative iteration, token, and timeout limits (MBPP & SWE-bench)
- [ ] Implement `agent_mbpp.py` entrypoint and dump/validate workflow
- [ ] Implement `agent_swebench.py` entrypoint and Docker container interaction
- [ ] Output serialization to `solution.json` matching `SolutionOutput` schema
- [ ] Validate against `exam_mbpp.sh` and `exam_swebench.sh`

---

## 🏆 Final Joint Tasks (Gpecelli + Gipimpin)
- [ ] Run benchmark evaluation across 5 models and 3 SWE-bench tasks
- [ ] Author `BENCHMARK_REPORT.md` (results table, latency, reliability, intermediary metrics, ablation)
- [ ] Finalize `README.md` following School 42 requirements
- [ ] Rehearsal for peer review live coding session (2-5 min test)

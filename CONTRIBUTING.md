# Contributing & Git Workflow Guidelines

> Standard engineering guidelines for team collaboration on **Agent Smith**.

---

## 🌿 Git Branching Strategy

To keep the repository stable and avoid merge conflicts, all development should be done on feature branches:

| Branch | Owner | Purpose |
|---|---|---|
| `main` | Both | Production branch. Always green and passing tests. |
| `feature/sandbox-security` | `gpecelli` | Sandbox implementation, security filters, REPL CLI |
| `feature/mcp-tools` | `gpecelli` | `mcp_tools_mbpp.py` and `mcp_tools_swebench.py` |
| `feature/llm-client` | `gipimpin` | Multi-token LLM client, rate-limit rotation |
| `feature/agent-orchestrator` | `gipimpin` | Extraction layer, agent loop, MBPP & SWE-bench runners |
| `feature/benchmark-report` | Both | Benchmarks, evaluations, and `BENCHMARK_REPORT.md` |

---

## 📝 Commit Conventions

Use concise, descriptive commit messages:
- `feat(sandbox): implement import allowlist filtering`
- `feat(llm): add automatic token rotation on 429`
- `fix(tools): format cat -n output correctly in read_file`
- `docs: update roadmap and taskboard`

---

## 🧪 Pre-Push Quality Checks

Before merging any branch into `main`:
1. **Formatting & Type Check**:
   ```bash
   uv run python -m py_compile src/**/*.py
   ```
2. **Sandbox Validation**:
   ```bash
   uv run sandbox
   ```
3. **No Hardcoded Secrets Check**:
   Ensure no API keys are committed:
   ```bash
   git diff --cached | grep -iE 'api[_-]?key|token'
   ```

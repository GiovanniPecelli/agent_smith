# Team Organization & Architecture Contract

> Official team division of responsibilities, module contracts, and collaboration guidelines for **Agent Smith** (42 School).

---

## 👥 Team Members & Roles

| Member | GitHub/42 Login | Role / Domain | Core Responsibilities |
|---|---|---|---|
| **Giovanni Pecelli** | `gpecelli` | **Execution & Safety Lead** | Sandbox, Security Isolation, REPL CLI, MCP Servers & Tools (`exam_sandbox.sh`) |
| **Gipimpin** | `gipimpin` | **Agent & Intelligence Lead** | LLM Client, Multi-token rotation, Prompts, Extraction Layer, Orchestrator Loop (`exam_mbpp.sh`, `exam_swebench.sh`) |

---

## 🏛️ Module Boundaries & Technical Ownership

```
┌─────────────────────────────────────────────────────────────┐
│                   GIPIMPIN's DOMAIN                         │
│                                                             │
│   1. LLM Client (`src/agent/llm_client.py`)                 │
│      - Multi-token rotation (HTTP 429 recovery)             │
│      - Metrics calculation (tokens, latency, retries)       │
│                                                             │
│   2. Extraction Layer (`src/agent/extraction.py`)           │
│      - Markdown / XML / JSON / ReAct -> Python code         │
│                                                             │
│   3. System Prompt & Manual (`src/agent/prompts.py`)        │
│                                                             │
│   4. Orchestrator Loop (`src/agent/orchestrator.py`)        │
│      - Thought -> Code -> Observation loop                  │
│      - Execution limits (iterations, timeout, tokens)       │
│      - CLI Runners (`agent_mbpp.py`, `agent_swebench.py`)   │
│      - Output generation: `solution.json`                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                Calls Interface: sandbox.execute(code)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   GPECELLI's DOMAIN                         │
│                                                             │
│   1. Sandbox Core (`src/sandbox/sandbox.py`)                │
│      - Import allowlist enforcement (`authorized_imports`)  │
│      - Filesystem restriction (`allowed_directories`)       │
│      - Network access denial (socket blocking)              │
│      - Resource limits (timeout 30s, memory 512MB)          │
│      - Native injection of `final_answer(answer)`           │
│      - Variable persistence across consecutive steps        │
│                                                             │
│   2. Interactive REPL CLI (`src/cli/sandbox_cli.py`)        │
│      - `uv run sandbox [config.json]`                       │
│                                                             │
│   3. MCP Servers at Repository Root                         │
│      - `mcp_tools_mbpp.py`: run_tests tool                  │
│      - `mcp_tools_swebench.py`: read/edit/search/exec tools │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤝 The Integration Contract (API Boundary)

To avoid merge conflicts and allow 100% parallel development, both members agree on this Python interface:

### 1. How Gipimpin calls Gpecelli's Sandbox:
```python
from src.sandbox.sandbox import Sandbox, SandboxExecutionResult
from src.models import SandboxConfig

# 1. Gipimpin instantiates Gpecelli's Sandbox with config
sandbox = Sandbox(config=sandbox_config)

# 2. Gpecelli exposes register_tool to connect MCP tools
sandbox.register_tool(name="read_file", func=read_file_func)
sandbox.register_tool(name="edit_file", func=edit_file_func)

# 3. Gipimpin executes LLM-generated code and receives structured result:
result: SandboxExecutionResult = sandbox.execute(python_code)

# 4. Gipimpin inspects the result:
if result.is_final:
    # Task solved! result.final_answer contains the solution code/patch
    solution = result.final_answer
elif result.error:
    # Execution failed (syntax error, timeout, permission denied)
    # Gipimpin sends result.error back to the LLM as observation
    observation = result.error
else:
    # Standard output to return to LLM
    observation = result.stdout
```

---

## 📅 Joint Responsibilities (Both Members)

1. **System Integration**:
   - Connecting `src/agent/orchestrator.py` with `src/sandbox/sandbox.py`.
2. **Benchmark Report (`BENCHMARK_REPORT.md`)**:
   - Running the 5 models across 2+ providers on the 3 SWE-bench tasks.
   - Recording intermediary metrics and ablation study.
3. **Repository Documentation (`README.md`)**:
   - Writing the final evaluation documentation required by School 42.

# Specifiche Tecniche e Strumenti (Cheat Sheet)

> Riferimento rapido per tutte le firme dei metodi, formati di output, comandi CLI e vincoli rigidi richiesti dal subject.

---

## 1. Strumenti MCP Obbligatori (Mandatory Tools)

Tutti i tool sono esposti dai server MCP (`mcp_tools_mbpp.py` e `mcp_tools_swebench.py`) e testati singolarmente dalla moulinette.

### A. File System Tools

#### `read_file(filepath: str, start_line: int = 1, end_line: int = -1) -> str`
- Legge il contenuto del file numerando le righe in stile `cat -n`.
- **Formato di output esatto**:
  ```text
  1:def example():
  2:    return True
  ```

#### `edit_file(filepath: str, old_str: str, new_str: str) -> str`
- Sostituisce una stringa esatta (`old_str`) con una nuova stringa (`new_str`) all'interno del file.
- Deve restituire un messaggio chiaro di successo o errore se la stringa `old_str` non viene trovata o compare più volte in modo ambiguo.

#### `list_files(directory: str, pattern: str = "*") -> List[str] / str`
- Elenca tutti i file all'interno della directory specificata che corrispondono al pattern (es. `*.py`).

---

### B. Code Search Tools

#### `search_code(pattern: str, file_pattern: str = "*") -> str`
- Esegue una ricerca grep-like di testo o regex nei file.
- **Formato di output esatto**:
  ```text
  /absolute/path_to_file.py:12 def target_function():
  /absolute/path_to_file.py:45 return target_function()
  ```

#### `search_function_or_class_definition_in_code(name: str) -> str`
- Cerca la definizione (`def name` o `class name`) all'interno del codice.
- Formato di output uguale a `search_code` (`/path/to/file.py:line_number content`).

#### `find_references(name: str, filepath: str = "", line: int = -1) -> str`
- Cerca tutti gli utilizzi/riferimenti a un simbolo (funzione o classe).
- Formato di output uguale a `search_code`.

---

### C. Execution Tools

#### `run_tests(code: str = "", test_list: list = None) -> str (JSON)`
- Per MBPP: esegue `code` contro la lista di asserzioni `test_list`. Restituisce una stringa JSON:
  ```json
  {"success": true, "output": "All tests passed"}
  ```
- Per SWE-bench: esegue lo script di evaluation bash del task nel repository e restituisce l'output dei test.

#### `get_patch() -> str`
- Estrae il git unified diff di tutte le modifiche apportate al repository di lavoro.
- Deve eseguire internamente il comando git specifico:
  ```bash
  git -c core.fileMode=false diff
  ```

#### `run_command(command: str, workdir: str = ".") -> str`
- Esegue un comando shell all'interno della cartella di lavoro specificata.
- Restituisce stdout, stderr ed exit code del processo.

---

## 2. Lo Strumento Speciale: `final_answer`

> [!WARNING]
> `final_answer` **NON è un tool MCP**.
> È un costrutto nativo iniettato direttamente dal Sandbox nel namespace Python globale.

- **MBPP**: l'agente passa il codice Python della soluzione:
  ```python
  final_answer(your_solution_code)
  ```
- **SWE-bench**: l'agente passa la git patch estratta con `get_patch()`:
  ```python
  final_answer(get_patch())
  ```
- Chiamare `final_answer` genera un'eccezione interna controllata che interrompe l'esecuzione nel Sandbox e segnala all'orchestrazione che il task è terminato con successo.

---

## 3. Comandi CLI Richiesti

### A. Sandbox Interattivo (REPL)
```bash
# Avvio semplice
uv run sandbox

# Con configurazione personalizzata
uv run sandbox config/sandbox_config.json

# Con strumenti MBPP via stdio
uv run sandbox --mcp-stdio "python mcp_tools_mbpp.py" config/sandbox_config.json

# Con strumenti SWE-bench via stdio
uv run sandbox --mcp-stdio "python mcp_tools_swebench.py" config/sandbox_config.json

# Con server MCP via HTTP
uv run sandbox --mcp-server http://localhost:8000 config/sandbox_config.json
```

### B. Runner per MBPP
```bash
uv run python -m agent_mbpp \
  --task-file /cache/mbpp_task.json \
  --output ../cache/mbpp_solution.json \
  --model-name "qwen/qwen-2.5-coder-32b-instruct" \
  --provider-url "https://openrouter.ai/api/v1"
```

### C. Runner per SWE-bench
```bash
uv run python -m agent_swebench \
  --task-file /cache/swebench_task.json \
  --output ../cache/swebench_solution.json \
  --model-name "qwen/qwen-2.5-coder-32b-instruct" \
  --provider-url "https://openrouter.ai/api/v1"
```

---

## 4. Tabella dei Limiti Rigidi (Hard Limits)

| Vincolo | **MBPP** | **SWE-bench** |
|---|---|---|
| **Max Iterazioni Loop** | **10** | **30** |
| **Max Token Input** | **6.000** (cumulativi) | **300.000** (cumulativi) |
| **Max Token Output** | **1.500** (cumulativi) | **10.000** (cumulativi) |
| **Timeout Globale** | **120 secondi** | **900 secondi** (15 minuti) |
| **Timeout Singolo Step Sandbox** | Configurato in `SandboxConfig` (default 30s) | Configurato in `SandboxConfig` (default 30s) |
| **Memoria Max Sandbox** | 512 MB | 512 MB |
| **Soglia Promozione Esame** | 4 task su 5 (80%) | 2 task su 3 (66%) |

> [!NOTE]
> I token di "thinking" (per modelli di tipo reasoning come QwQ o DeepSeek R1) sono conteggiati nei token totali. Per questo motivo, per rimanere agevolmente sotto i limiti (specie su MBPP dove il tetto è 6.000 in / 1.500 out), è consigliato prediligere modelli non-reasoning efficienti (es. Qwen 2.5 Coder 32B, Llama 3.3 70B Versatile, Gemini 1.5 Flash).

---

## 5. Script di Esame della Moulinette

Gli script di esame automatico invocano il tuo codice in questo modo:

```bash
./exam_mbpp.sh \
  --student-path ./student \
  --moulinette-path ./moulinette \
  --env-file /path/to/.env

./exam_swebench.sh \
  --student-path ./student \
  --moulinette-path ./moulinette \
  --env-file /path/to/.env

./exam_sandbox.sh \
  --student-path ./student \
  --moulinette-path ./moulinette \
  --env-file /path/to/.env
```

Cosa testa `exam_sandbox.sh`:
- Blocco di importazioni non permesse.
- Blocco di builtin pericolosi.
- Blocco di tentativi di connessione di rete (socket).
- Restrizione di lettura/scrittura alle sole `allowed_directories`.
- Rispetto del timeout e del limite di memoria RAM.
- Connessione e corretta scoperta del protocollo MCP.

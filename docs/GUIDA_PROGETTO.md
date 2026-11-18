# Agent Smith — Guida Completa e Modello Mentale

> Guida introduttiva e concettuale per comprendere a fondo l'architettura, i componenti e il funzionamento del progetto **Agent Smith** (Scuola 42).

---

## 1. Cos'è Agent Smith?

Nel paradigma classico, un LLM (Large Language Model) riceve una richiesta e produce direttamente una risposta o un blocco di codice finale.
In **Agent Smith**, costruiamo un **Code Agent autonomo**:
Un programma che non si limita a generare codice "al buio", ma:
1. **Ragiona sul problema** (*Thought*).
2. **Genera ed esegue codice Python** (*Code*) per interrogare l'ambiente ed eseguire azioni.
3. **Osserva il risultato reale** (*Observation*): stdout, stderr, errori, esito dei test.
4. **Reitera e corregge la propria rotta** finché non risolve il task o raggiunge i limiti massimi consentiti.

Al termine del ciclo, l'agente salva un file strutturato (`solution.json`) contenente la soluzione trovata e la cronologia dettagliata di ogni singolo passaggio.

---

## 2. Il Modello Mentale a 4 Livelli

Per non perdersi, immagina il progetto come un'architettura a cipolla (o a 4 strati concentrici):

```
┌─────────────────────────────────────────────────────────────┐
│  1. CLI & BENCHMARK RUNNERS                                 │
│     (agent_mbpp, agent_swebench, interactive sandbox CLI)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  2. AGENT ORCHESTRATOR LOOP                                 │
│     Thought ➔ Code ➔ Observation                            │
│     - Chiama l'LLM con rotazione multi-token                │
│     - Extraction Layer (Markdown, XML, JSON, ReAct)         │
│     - Gestisce limiti iterazioni, token e timeout           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  3. SANDBOX BOUNDARY (Sicurezza e Isolamento)               │
│     - Solo librerie standard Python (NO RestrictedPython)   │
│     - Filtro importazioni (authorized_imports)              │
│     - Directory permesse (allowed_directories)              │
│     - Blocco totale connessioni di rete                     │
│     - Timeout esecuzione codice & limiti memoria            │
│     - Builtin speciali iniettati:                           │
│       * final_answer(...)  <-- chiude il loop dell'agente   │
│       * Wrapper Python dei Tool MCP                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
               (Stdio o HTTP)  ▼
┌─────────────────────────────────────────────────────────────┐
│  4. MCP SERVERS & TOOLS ESTERNI                             │
│     (mcp_tools_mbpp.py / mcp_tools_swebench.py)             │
│     - Eseguono azioni fuori dal sandbox:                    │
│       * File system: read_file, edit_file, list_files       │
│       * Code search: search_code, find_references           │
│       * Esecuzione: run_tests, run_command, get_patch       │
│     - In SWE-bench: interagiscono col container via TESTBED │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. I Componenti Chiave Spiegati Semplice

### A. Il Loop dell'Agente: `Thought ➔ Code ➔ Observation`
Il "cervello" non esegue uno script prefissato. A ogni ciclo:
1. **Prompt**: L'agente invia all'LLM il manuale del sandbox, l'elenco dei tool disponibili e la cronologia finora accumulata.
2. **Thought + Code**: L'LLM scrive cosa intende fare (*Thought*) e produce del codice Python (*Code*).
3. **Extraction**: Il tuo codice estrae i comandi Python dalla risposta (anche se il modello ha usato markdown ```python, XML `<invoke>` o JSON `<tool_call>`).
4. **Execution**: Il codice estratto viene passato al Sandbox.
5. **Observation**: Il Sandbox restituisce output o errori, che vengono reinseriti nel prompt del ciclo successivo.
6. **Zero Silent Failures**: Se il modello sbaglia sintassi, va in timeout o genera un formato invalido, il sandbox deve restituire un messaggio d'errore chiarissimo affinché l'LLM capisca e corregga il tiro.

### B. Il Sandbox (La Gabbia di Sicurezza)
L'LLM scrive codice arbitrario. Il sandbox serve a evitare che tale codice faccia disastri o imbrogli:
- **Nessuna libreria esterna permessa per la sicurezza**: vietato usare `RestrictedPython`. Tutto deve essere implementato con moduli standard Python (es. `sys.modules`, `builtins`, `ast`, `resource`, `signal`, o processi separati).
- **Import allowlist**: consentiti solo i moduli in `authorized_imports` (es. `math`, `collections.*`, `re`, `json`, `typing`, ecc.). Tutto il resto è bloccato.
- **Directory allowlist**: il codice sandboxed può accedere solo a cartelle sicure (es. `/testbed`, `/tmp/agent`).
- **No Network**: nessun socket in entrata/uscita consentito al codice sandboxed.
- **`final_answer(...)`**: è una funzione **speciale iniettata direttamente dal Sandbox**, NON è un tool MCP! Quando il codice dell'agente invoca `final_answer(risultato)`, il sandbox intercetta la chiamata, interrompe il loop e registra la soluzione.

### C. I Server MCP (Model Context Protocol)
MCP è uno standard che separa l'agente dagli strumenti concreti.
- Nel repository devi creare due file standalone:
  - `mcp_tools_mbpp.py` (per test MBPP).
  - `mcp_tools_swebench.py` (per esplorazione e modifiche in SWE-bench).
- Questi server espongono strumenti come:
  - `read_file(filepath, start_line, end_line)` (formato tipo `cat -n`).
  - `edit_file(filepath, old_str, new_str)` (sostituzione stringa esatta).
  - `search_code(pattern, file_pattern)` (ricerca stile grep `file:line content`).
  - `run_tests()` (lancia i test di validazione).
  - `get_patch()` (genera il `git -c core.fileMode=false diff`).
  - `run_command(command, workdir)` (esegue un comando di shell).
- Il Sandbox fa da **MCP Client**: si connette al server (via `stdio` lanciando il processo Python, oppure via `HTTP`), scopre i tool disponibili, e inietta nel namespace del Sandbox delle normali funzioni Python che l'LLM può chiamare direttamente!

### D. I Due Benchmark

| Caratteristica | **MBPP (Mostly Basic Python Problems)** | **SWE-bench (Software Engineering)** |
|---|---|---|
| **Obiettivo** | Risolvere problemi algoritmici in puro Python (es. "trova il primo elemento non ripetuto"). | Risolvere bug reali in grandi repository open-source (es. sympy, xarray, django). |
| **Ambiente** | Interprete locale sandboxed. | Container Docker con il repository reale del bug. |
| **Cosa fa l'agente** | Scrive e testa una funzione Python. Chiama `final_answer(codice_funzione)`. | Naviga il codice, trova il bug, modifica i file con `edit_file`, testa con `run_tests()`, estrae la patch con `get_patch()` e chiama `final_answer(patch)`. |
| **Soluzione prodotta** | Stringa con il codice della funzione Python. | Stringa con il git unified diff (`git diff`). |
| **Max Iterazioni** | **10** iterazioni. | **30** iterazioni. |
| **Max Input Token** | **6.000** token cumulativi. | **300.000** token cumulativi. |
| **Max Output Token** | **1.500** token cumulativi. | **10.000** token cumulativi. |
| **Timeout Totale** | **120** secondi. | **900** secondi (15 minuti). |
| **Soglia di Promozione** | **4 / 5** task random superati. | **2 / 3** task random superati. |

---

## 4. Come Funziona Docker in SWE-bench (Il "Bridge")

Il subject offre due possibilità per SWE-bench:
- (A) Mettere tutto il sandbox all'interno del container Docker.
- (B) **Far girare Sandbox e Agente sull'Host, e usare i Tool MCP come "Bridge" dentro il container.**

**L'approccio (B) è di gran lunga il più pulito e consigliato:**
1. Ogni task di SWE-bench ha un'immagine Docker diversa (con dipendenze complesse come sympy, numpy, scipy). Se mettessi il sandbox dentro il container, dovresti iniettare il tuo intero codice in ogni container.
2. Invece, tenendo l'agente e il sandbox sull'host:
   - Quando la moulinette avvia il task, imposta la variabile d'ambiente `TESTBED_PATH` indicando la radice del repository.
   - Il server MCP legge `TESTBED_PATH` ed esegue i comandi (lettura file, scrittura file, esecuzione test, `git diff`) puntando direttamente a quella cartella o interagendo con l'ambiente del container.
   - Sandbox, orchestratore e parser restano universali, indipendenti dal task!

---

## 5. Come Funziona la Valutazione della Moulinette

La valutazione segue un ciclo in 3 passaggi per ciascun task:

```bash
# 1. La moulinette estrae un task e genera il JSON di input
uv run moulinette_eval dump mbpp --output ../cache/mbpp_task.json

# 2. Il TUO agente viene eseguito sul task e produce solution.json
uv run python -m agent_mbpp \
  --task-file ../cache/mbpp_task.json \
  --output ../cache/mbpp_solution.json \
  --model-name "qwen/qwen-2.5-coder-32b-instruct" \
  --provider-url "https://openrouter.ai/api/v1"

# 3. La moulinette valida la correttezza del codice e controlla i limiti
uv run moulinette_eval validate mbpp ../cache/mbpp_task.json ../cache/mbpp_solution.json
```

Durante l'esame ufficiale:
- Ci sono script automatici (`exam_mbpp.sh`, `exam_swebench.sh`, `exam_sandbox.sh`).
- Le chiavi API sono passate tramite file `.env` (nessuna chiave hardcodata nel codice sorgente, pena bocciatura immediata!).
- Verrà svolta una **modifica live del codice** (2-5 minuti): l'esaminatore ti chiederà di fare una piccola modifica al volo all'agente per verificare che il codice sia farina del tuo sacco.

---

## 6. Il Modello di Dati di Output: `solution.json`

Al termine del task, l'agente deve scrivere un file JSON su disco conforme alla classe Pydantic `SolutionOutput`:

```json
{
  "task_id": "123",
  "benchmark": "mbpp",
  "success": true,
  "solution": "def my_func(x):\n    return x * 2\n",
  "iterations": 3,
  "total_requests": 3,
  "total_input_tokens": 2450,
  "total_output_tokens": 420,
  "total_time_seconds": 14.5,
  "steps": [
    {
      "step": 1,
      "input_tokens": 800,
      "output_tokens": 150,
      "request_time_ms": 1200.0,
      "timestamp": "2026-11-18T12:00:00",
      "api_url": "https://openrouter.ai/api/v1",
      "model_name": "qwen/qwen-2.5-coder-32b-instruct",
      "llm_output": "I will inspect the problem...\n```python\nprint(1)\n```",
      "sandbox_input": "print(1)",
      "sandbox_output": "1\n",
      "retries": 0
    }
  ],
  "system_prompt": "... full system prompt ...",
  "error": null,
  "timestamp": "2026-11-18T12:00:15"
}
```

La presenza di ogni singolo passaggio in `steps` garantisce ai revisori che la soluzione derivi da vero ragionamento e iterazione, non da risposte pre-memorizzate.

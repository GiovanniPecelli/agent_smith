# Indice della Documentazione di Agent Smith

Benvenuto nella documentazione di progetto di **Agent Smith**.
Questa cartella contiene tutti i documenti necessari per comprendere l'architettura del sistema, le regole imposte dal subject e la guida operativa per implementarlo passo dopo passo.

---

## 📚 Documenti Disponibili

1. [**GUIDA_PROGETTO.md**](file:///home/gpecelli/Desktop/agent_smith/docs/GUIDA_PROGETTO.md)
   - **Il Modello Mentale**: Cos'è un Code Agent e come funziona il loop `Thought ➔ Code ➔ Observation`.
   - **I 4 Livelli Architetturali**: CLI Runner, Orchestrator, Sandbox Boundary e Server MCP.
   - **I Due Benchmark**: Differenze tra MBPP (algoritmi puri) e SWE-bench (bug reali nei repository).
   - **Docker e Architettura "Bridge"**: Perché far girare il sandbox sull'host e i tool MCP dentro il container.
   - **Formato di output `solution.json`** e requisiti di trasparenza.

2. [**ROADMAP_IMPLEMENTAZIONE.md**](file:///home/gpecelli/Desktop/agent_smith/docs/ROADMAP_IMPLEMENTAZIONE.md)
   - **Divisione del team**: Ruoli di `gpecelli` (Sandbox & MCP) e `gipimpin` (LLM & Loop).
   - **Struttura cartelle** del repository.
   - **Le 8 Fasi (Milestone) di sviluppo** in ordine logico.

3. [**TEAM_ORGANIZATION.md**](file:///home/gpecelli/Desktop/agent_smith/docs/TEAM_ORGANIZATION.md)
   - **Contratto di Architettura**: Ruoli precisi di `gpecelli` e `gipimpin`.
   - **API Boundary**: L'interfaccia esatta con cui l'Orchestratore di Gipimpin invoca il Sandbox di Gpecelli.

4. [**TASK_BOARD.md**](file:///home/gpecelli/Desktop/agent_smith/docs/TASK_BOARD.md)
   - **Kanban Checklist**: Elenco delle attività spuntabili assegnate a ciascun membro.

5. [**SPECIFICHE_TECNICHE_E_TOOLS.md**](file:///home/gpecelli/Desktop/agent_smith/docs/SPECIFICHE_TECNICHE_E_TOOLS.md)
   - **Firme e formati di output dei tool MCP obbligatori**:
     - `read_file` (formato numerato `cat -n`), `edit_file`, `list_files`.
     - `search_code` (formato grep `path:line content`), `search_function_or_class_definition_in_code`, `find_references`.
     - `run_tests`, `get_patch` (`git -c core.fileMode=false diff`), `run_command`.
   - **Specifiche di `final_answer`**: cos'è e perché non è un tool MCP.
   - **Tabella Limiti Rigidi (Hard Limits)**: iterazioni, token, timeout per MBPP e SWE-bench.
   - **Comandi CLI e script d'esame della moulinette**.

---

## 🎯 Da Dove Iniziare?
- Leggi prima [**GUIDA_PROGETTO.md**](file:///home/gpecelli/Desktop/agent_smith/docs/GUIDA_PROGETTO.md) per avere chiara la visione d'insieme.
- Segui la scaletta di [**ROADMAP_IMPLEMENTAZIONE.md**](file:///home/gpecelli/Desktop/agent_smith/docs/ROADMAP_IMPLEMENTAZIONE.md) partendo dalla **Fase 1 (Modelli Pydantic)** e dalla **Fase 2 (Sandbox)**.
- Consulta [**SPECIFICHE_TECNICHE_E_TOOLS.md**](file:///home/gpecelli/Desktop/agent_smith/docs/SPECIFICHE_TECNICHE_E_TOOLS.md) come riferimento per non sbagliare firme dei metodi e formati di output richiesti dalla moulinette.

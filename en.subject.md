

# Agent Smith 

Autonomous reasoning, code generation, and execution 

_Summary: In this project, you will build an_ **_agentic framework_** _capable of autonomously solving coding challenges. Your agent will reason, write code, execute it in a sandboxed environment, and iterate until a solution is found._ 

_This project introduces_ **_Code Agents_** _,_ **_Model Context Protocol (MCP)_** _, and controlled code execution. Made in collaboration with @ldevelle_ 

_Version: 1.1_ 

# **Contents** 

|**I**|**Foreword**|**2**|
|---|---|---|
|**II**|**AI Instructions**|**3**|
|**III**|**Overview**|**5**|
|III.|1<br>What is a Code Agent? . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>6|
|**IV**|**Common Instructions**|**9**|
|IV.|1<br>General Rules<br>. . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>9|
|IV.|2<br>Technical Constraints . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>9|
|**V**|**Mandatory Part**|**10**|
|V.1|Agentic Framework . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>10|
||V.1.1<br>Common Output Models . . . . . . . . . . . . .|. . . . . . . . . .<br>11|
||V.1.2<br>Development Approach . . . . . . . . . . . . . .|. . . . . . . . . .<br>13|
|V.2|The Sandbox . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>13|
|V.3|MBPP Agent<br>. . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>17|
|V.4|SWE-bench Agent . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>18|
|V.5|Mandatory Tools<br>. . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>20|
||V.5.1<br>File System Tools . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>21|
||V.5.2<br>Code Search Tools<br>. . . . . . . . . . . . . . . .|. . . . . . . . . .<br>21|
||V.5.3<br>Execution Tools . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>21|
|V.6|LLM API Providers . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>22|
||V.6.1<br>Examples of Free Providers<br>. . . . . . . . . . .|. . . . . . . . . .<br>22|
|V.7|Model Benchmark Report . . . . . . . . . . . . . . .|. . . . . . . . . .<br>23|
|**VI**|**Evaluation**|**25**|
|VI.|1<br>Hard Requirements and Limits . . . . . . . . . . . .|. . . . . . . . . .<br>26|
||VI.1.1 MBPP Limits . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>26|
||VI.1.2 SWE-bench Limits . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>26|
|VI.|2<br>Pass Criteria . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>27|
|VI.|3<br>Grading Criteria . . . . . . . . . . . . . . . . . . . .|. . . . . . . . . .<br>27|
|VI.|4<br>What We Will Test in the Review . . . . . . . . . .|. . . . . . . . . .<br>27|
||VI.4.1 AI Safety in Evaluation . . . . . . . . . . . . . .|. . . . . . . . . .<br>28|
|VI.|5<br>Evaluation logging structure<br>. . . . . . . . . . . . .|. . . . . . . . . .<br>28|
|**VII**|**Readme Requirements**|**29**|
|**VIII**|**Submission**|**31**|



1 

# **Chapter I Foreword** 

Software engineering is no longer only about writing correct code, it is about **understanding systems, navigating large codebases, debugging failures, and iterating efficiently** . Modern LLMs generate code well, but fixing real bugs also needs exploration, hypothesis testing, execution, and observation. 

This is where **Agent Smith** comes in. A Code Agent is not just a model that writes code: it **reasons about a task, interacts with tools, executes code safely, observes results, and adapts its strategy** . In this project, you will design and implement such a system, moving beyond static prompts and JSON-based tool calling to build a **fully agentic loop** driven by executable Python code. 

2 

# **Chapter II** 

# **AI Instructions** 

## ● **Context** 

AI is now a powerful coding partner — alongside your peers — for tackling large and demanding projects. You will guide it through both technical and non-technical aspects of your work. 

AI tools can boost your efficiency and improve the quality of your output, but you should be able to dive deep into any part of the project without relying on them. 

Your AI partner supports you, but you remain fully responsible for making informed technical decisions and to clearly explain and defend them. 

## ● **Main message** 

- ☛ Strive for a mature and responsible use of AI. 

- ☛ Never let AI take responsibility for decisions — especially when it lacks awareness of your goals, constraints, or team dynamics. 

- ☛ Maintain creativity, innovation, and human oversight through active collaboration with your peers. AI is trained on existing data and rarely generates truly new ideas. 

- ☛ Stay informed about emerging trends and be ready to adapt to new concepts and technologies. 

## ● **Learner rules:** 

- Maintain intellectual leadership over your projects and make your own informed decisions. 

- Prioritise the collective intelligence of your team and peers. 

- Actively stay informed about the ongoing evolution of AI technologies. 

3 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

## ● **Phase outcomes:** 

- AI engineering skills. 

- Increased efficiency. 

- Greater reliability and quality. 

- A pioneering mindset. 

## ● **Comments and examples:** 

- Your peers can identify trade-offs, question assumptions, and help you improve. The first answer from an AI might not be the best — it may lack efficiency, security, or real added value. Now more than ever, you should rely on your peers. 

- AI can make you faster, but your peers make you better. Collaboration, discussion, and mutual challenge are key to success. 

- Be transparent about how AI was used in your projects, and clearly identify what was generated by AI tools. 

#### ✓ **Good practice:** 

I asked AI to help generate unit tests for my API. I reviewed them with my teammate, and we adjusted them for edge cases. It saved time, and we both learned something new. 

#### ✗ **Bad practice:** 

I had AI generate the entire architecture of my project. It “works,” but when I’m asked to explain design decisions during the peer review or in front from of a customer, I cannot. I lose credibility and I fail. 

4 

# **Chapter III** 

# **Overview** 

This project explores a new paradigm in AI-driven software engineering: **agentic code generation** . 

Unlike classical approaches where an LLM outputs a final answer, your system will allow the model to: 

- Write executable Python code 

- Call tools directly from code 

- Observe execution results 

- Iterate until the task is solved 

Your agent will operate through a structured loop: **Thought →Code →Observation** . 



<!-- Start of picture text -->
AGENT LOOP<br>THOUGHT |——>» CODE —»| OBSERVATION<br>LLM LLM Code runs<br>reasons writes in sandbox<br>A<br>(repeat until solution found)<br>FINAL ANSWER<br>Submit solution<br><!-- End of picture text -->

You will apply this framework to two different benchmarks: 

5 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

- **MBPP** : algorithmic Python problems 

- **SWE-bench** : real-world bug fixing in production repositories 

The core challenge of this project is not only to make the agent intelligent, but also to make it **safe, controlled, reproducible, and measurable** . 

In particular, you are expected to **evaluate and benchmark multiple language models** in order to analyze their performance and identify the most effective ones according to success rate and iteration efficiency. 

## **III.1 What is a Code Agent?** 

A **Code Agent** is an AI system that can: 

- Reason about a programming task 

- Generate executable code 

- Execute that code in a controlled environment 

- Use tools to interact with files, tests, and repositories 

- Observe the results and refine its approach 

In this project, you will implement a **code-based tool calling** approach, where the LLM generates Python code such as: 

`result = search_code("validate_email")` print (result) `content = read_file("models.py", 1, 50)` print (content) 

This approach is more expressive than JSON tool calling, allowing: 

- Persistent variables between steps 

- Conditional logic and loops 

- Complex multi-step reasoning 

6 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



<!-- Start of picture text -->
Conversation<br>Systen<Pranework Explanation?<br>‘<Sondbon Manel<br>Solve the bug with “is_volid_emeil()* when an email contoins a ‘+’ sign Sandbox<br>onOkay, Fret let's Find where is defined “is vahd_enai() Python 3.10.0<br>print(resutt) "<br>hesthedsrelmail py. des. validemai(mai st) -> boot hestbed/scmail 65 des. vaid_emal(ait st) -> boot<br>festbedlerchiserpy2 from mal import s-validemal, send_emall hestbedsrcliserpy:2 from mai imports valld-emal, send_emait<br>hestbedkrchiserpy21 His. vald-emalluser<br>mail Restbedircserpy.21 iis. valid emailuser-mal<br>Okay, now T should read “sre/moiliey><br>content=<br>read fle(Restheddsrcimailpy, start tine=65,end.ine=70) See comentfons Hel Resvdiscnaloy’, sar nes68, end. ine=70)<br>65:end.defcode>e-vald_emai(mat sr) -> boot | 65:65: detis.valid_emailfmai"Validate ema formatie=ste -> boot<br>66: \"Validate emai formati 67: pattern<br>67; pattern =n(ar2A-20-9, WG la-2A-20-9-Jofo-2A-21(2)1S 68: _fetumbool(rematchipatern,= PAfarzA-20-9_-]+@la-2A-20-9-}WLemai) (0-24-22)<br>68:69:70: dereturnsavetsetbool(ematehipater, ema) 670: det savesein<br>1 Found the grotlen! The regex patterns incomplete<br><!-- End of picture text -->



<!-- Start of picture text -->
7<br><!-- End of picture text -->

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



<!-- Start of picture text -->
Agent Code<br>Prompt<br>LLM APL Orchestrator<br>Response \ Response containing code block<br>Code.<br>extraction<br>Extracted code<br>‘Sandbox<br>Tool Call<br>Python<br>Interpreter NCP Client<br>STDIO / HTTP<br><!-- End of picture text -->

1. **Agent/Orchestrator** is the central loop. It calls the LLM, extracts code, feeds it to the sandbox, reads observations, and repeats. 

2. **Code Extraction** is a transform step between the LLM response and the sandbox. 

3. **Sandbox** is the execution boundary. It enforces security restrictions on LLMgenerated code. The sandbox contains an MCP client that connects to an external MCP server. 

4. **final_answer()** is a built-in sandbox construct — it is NOT an MCP tool. 

5. **MCP Server(s)** run as separate process(es) (via stdio or HTTP). Only your own MCP server(s) are allowed. 

8 

# **Chapter IV** 

# **Common Instructions** 

## **IV.1 General Rules** 

- You must use **Python 3.10** . 

- You must use **uv** as your package manager. 

- Your project must follow clean software architecture principles. 

- All errors must be handled gracefully — crashes during evaluation will result in failure. 

- Your code must be readable, structured, and documented. 

- All execution must happen in a **sandboxed environment** . 

## **IV.2 Technical Constraints** 

- You must support multiple LLM providers and models. 

- You must implement usage tracking (tokens, retries, latency, requests). 

- You must implement a configurable sandbox (imports, filesystem access), as specified in Section 5.2. 

- Your tools must work independently of the agent loop. 

- You must not use any library that re-implements agent orchestration logic (e.g., llama-index, smolagents, langgraph, crewai, autogen). 

- The agent loop must be your own implementation. 

- Even though the project can be completed without it, multi-agent architectures are allowed, but the orchestration must be your own code. 

9 

# **Chapter V** 

# **Mandatory Part** 

## **V.1 Agentic Framework** 

In this project, you must build an **agentic framework** capable of autonomously solving coding challenges. 

For LLM provider selection, see Section 5.6.1 for examples of free-tier APIs. 

Your system must: 

1. Implement a **Thought →Code →Observation** loop 

2. Extract LLM-generated Python code from the model responses 

```
Whenbenchmarkingacrossmultipleproviders(Section5.7),your
extractionlayershouldhandledifferentoutputformatsthatLLMs
produce—aswellastofitwhattheLLMsyouuseweretrainedon—
notjustPythoncodeblocks.Anon-exhaustivelist:
```

- `(a)` **`Python code blocks (primary)`** `— “‘python ... “‘ <end_code>` 



- `(b)` **`XML tool calls`** `— Anthropic-style <invoke name="..."><parameter>...</parameter></invoke>` 

- `(c)` **`JSON/Hermes tool calls`** `— <tool_call>{"name": "...", "arguments": {...}}</tool_call>` 

- `(d)` **`ReAct format`** `— Action: tool_name / Action Input: {...}` 

```
Non-PythonformatsshouldbeconvertedtoequivalentPythonfunction
calls(e.g.,result=read_file(filepath="/testbed/file.py"))before
sandboxexecution.Thisletsthesandboxremainformat-agnostic
whilesupportinganymodel.
```

3. Execute the generated code inside a sandboxed environment 

4. Feed the sandbox execution results back to the LLM 

10 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

5. Solve benchmark tasks autonomously using the agent loop 

6. Design the **system prompt** , including: 

   - clear documentation of the available tools 

   - examples of structured response slots (e.g. `Thought` , `Code` , `Observation` ) 

   - examples of effective agent reasoning loops 

```
YoursandboxmustprovideexplicitfeedbacktotheLLMinallof
thesesituations:
```

- `No valid code block was found in the model’s response` 



- `A code block was malformed but was interpreted anyway (explain how)` 

- `Execution hit the timeout and output is partial` 

- `Tool output was truncated due to size limits` 

- `An edit introduced a syntax error or lint violation` 

```
TheLLMshouldneverbeleftguessingaboutwhathappened.Silent
failuresleadtohallucinatedobservationsandwastediterations.
```

### **V.1.1 Common Output Models** 

Both MBPP and SWE-bench agents produce the same `StepMetrics` / `SolutionOutput` shape; only the `benchmark` and `solution` field semantics change (Python code for MBPP, a git patch for SWE-bench). 

```
classStepMetrics(BaseModel):
```

```
"""Metricsforasingleagentstep.
```

```
EachstepcorrespondstooneLLMgenerate->sandboxexecutecycle.
Allfieldsarerequiredforevaluation,emptystringsareacceptable
forstepswhereafielddoesn'tapply(e.g.,nosandboxexecution).
"""
step:int=Field(...,description="1-indexediterationnumber")
input_tokens:int=Field(...,description="TokenssenttotheLLMforthis
step")
output_tokens:int=Field(...,description="TokensgeneratedbytheLLM
forthisstep")
request_time_ms:float=Field(...,description="Wall-clocktimeforthe
LLMAPIcallinmilliseconds")
timestamp:str=Field(default_factory=lambda:datetime.now().isoformat(),
description="ISO8601timestampofwhenthisstepwasrecorded")
api_url:str=Field(default="",description="BaseURLoftheLLMAPI
endpoint(e.g.,'https://openrouter.ai/api/v1')")
```

11 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

```
model_name:str=Field(default="",description="Modelidentifierusedfor
thisstep(e.g.,'qwen/qwen3-235b-a22b-2507')")
llm_output:str=Field(default="",description="Rawtextgeneratedbythe
LLMbeforecodeextraction")
sandbox_input:str=Field(default="",description="Pythoncodesenttothe
sandboxforexecution")
sandbox_output:str=Field(default="",description="Sandboxexecution
result(stdout/stderr/errormessage)")
retries:int=Field(default=0,description="NumberofLLMAPIretries
beforegettingasuccessfulresponse(0=firstattemptsucceeded)")
```

```
classSolutionOutput(BaseModel):
```

```
"""Outputfromstudentsolution,requiredformatforevaluation.
```

```
ThisistheJSONstructureyouragentmustproduceandwritetosolution.
json.
Themoulinettevalidatesthisagainsttaskcorrectnessandmetricslimits.
"""
task_id:str=Field(...,description="Taskidentifier(MBPPtask_idas
string,orSWE-benchinstance_id)")
benchmark:str=Field(...,description="Benchmarktype:'mbpp'or'
swebench'")
success:bool=Field(...,description="Whethertheagentbelievesit
solvedthetask")
solution:str=Field(...,description="ForMBPP:thePythonfunctioncode.
ForSWE-bench:thegitpatch(diff)")
iterations:int=Field(...,description="Numberofagentloopiterations
used")
```

```
total_requests:int=Field(...,description="TotalnumberofLLMAPI
requestsmade(includingretries)")
```

```
total_input_tokens:int=Field(...,description="Sumofinput_tokens
acrossallsteps")
```

```
total_output_tokens:int=Field(...,description="Sumofoutput_tokens
acrossallsteps")
```

```
total_time_seconds:float=Field(...,description="Wall-clocktimefrom
agentstarttofinish")
steps:List[StepMetrics]=Field(default_factory=list,description="Per-
stepmetrics,oneentryperagentiteration")
```

```
system_prompt:str=Field(default="",description="Fullsystempromptsent
totheLLM(forprovenancechecking)")
error:Optional[str]=Field(default=None,description="Errormessageif
theagentfailed(Noneifsuccessful)")
```

```
timestamp:str=Field(default_factory=lambda:datetime.now().isoformat(),
description="ISO8601timestampofwhenthesolutionwasproduced")
```

12 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



```
EachstepinthestepsarrayofSolutionOutputmustincludeapi_url,
model_name,fieldsidentifyingtheLLMendpointusedforthatstep,
plusllm_output(rawLLMresponse),sandbox_input(codesentto
sandbox),sandbox_output(executionresult),andretries(APIretry
count).
```

### **V.1.2 Development Approach** 

Building an autonomous agent is a complex task. Here are questions to guide your development: 

**Starting out:** Which benchmark is simpler and should be tackled first? Am I testing with the most capable model available, or handicapping myself with constraints too early? Can my system solve the easiest task with token and iteration limits temporarily removed? If not, adding constraints will only make it worse. 

**Debugging your agent:** What happens in the first 3–5 iterations: tool-calling struggles, hallucinated observations, or an unexpected path? Have I tried solving the target task myself, manually, and does my prompt reflect that methodology? For SWEbench, break the eval script into smaller goals and track whether individual tests pass rather than waiting for the full script to succeed. 

**Scaling up:** Does a solution that works on one task generalize, or did I overfit? Am I optimizing too early (tokens, model choice), or have I proven the approach works first? Different models prefer different tool-calling styles: am I fighting the model’s natural tendencies, or working with them? 

## **V.2 The Sandbox** 

This part focuses on the design and implementation of a secure and configurable execution sandbox for the agent. 

1. Implement a **sandbox CLI usage** 

```
#Launchinteractivesandbox
uvrunsandbox
```

```
#Withcustomconfiguration
```

```
uvrunsandboxsandbox_template.json
```

```
#WithMBPPtools(stdio)
```

```
uvrunsandbox--mcp-stdio"pythonmcp_tools_mbpp.py"sandbox_template.
json
```

```
#WithMBPPtools(HTTP)
```

```
uvrunsandbox--mcp-server<URL>
```

```
#WithSWE-benchtools
```

```
uvrunsandbox--mcp-stdio"pythonmcp_tools_swebench.py"
sandbox_template.json
```

13 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

The **interactive sandbox** ( `uv run sandbox` with no task argument) is a REPLstyle command-line mode. It must open a prompt, read user-typed code in a loop, and execute each entry inside the sandbox namespace, subject to the same import, filesystem, timeout and memory restrictions defined in Section 5.2, with the connected MCP tool wrappers and `final_answer` available. After each entry it prints the result or any raised error and returns to the prompt. It exits cleanly on the `exit` command or on EOF ( `Ctrl+D` ). 

2. Implement a `final_answer` tool **What** **`final_answer` IS:** 

`final_answer` is a callable function that the sandbox injects into the execution namespace. When the agent’s code calls `final_answer(answer_string)` , the sandbox captures the argument and signals to the agent loop that the task is complete. The agent loop then terminates and produces the `SolutionOutput` . 

**What** **`final_answer` is NOT:** `final_answer` is **not** an MCP tool — it is not provided by any MCP server. It is always available in the sandbox namespace regardless of which MCP server is connected. MCP tools operate outside the sandbox (e.g., reading files in Docker, running tests), while `final_answer` operates within the sandbox to control the agent loop. 

**How to use** **`final_answer` :** 

- **MBPP** : call `final_answer(your_solution_code)` : pass your Python code as the argument 

- **SWE-bench** : call `final_answer(get_patch())` : pass the git patch retrieved via `get_patch()` as the argument 

#### **Architectural boundary:** 

The sandbox provides two kinds of callable functions in the execution namespace: 

- (a) **MCP tool wrappers** : discovered dynamically from the connected MCP server 

- (b) **`final_answer`** : always present, provided by the sandbox itself 

When you connect a different MCP server, the MCP tool wrappers change but `final_answer` remains. 

**Exception propagation:** Your sandbox must correctly propagate exceptions that control program flow. In particular, `KeyboardInterrupt` and `SystemExit` must not be silently caught — they need to reach the agent loop for proper shutdown. 

3. Enforce sandbox security constraints: Running LLM-generated code is inherently risky. Your sandbox is not just a technical component; it is a **safety boundary** 

14 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

between an autonomous system and the real world. 

   - **Import restrictions** : Only modules from the configured allowlist may be imported 

   - **Filesystem restrictions** : file access by the sandboxed code is limited to an allowlist of directories (the `allowed_directories` field of `SandboxConfig` ). These are paths on the filesystem the sandbox process itself sees, evaluated inside the sandbox, not host-only paths: any directory the code must reach has to be in the allowlist. Several entries are allowed so you can keep the task workspace (e.g., `/testbed` ) separate from a writable scratch/runtime area (e.g., `/tmp/agent` ); anything outside the allowlist is denied. 

   - **No network access** : Prevent any outbound or inbound network connections 

   - **Execution timeout** : Terminate code exceeding the configured timeout (applies only to sandboxed code) 

   - **Memory limits** : Terminate code exceeding allowed RAM usage 

   - **Restricted builtins** : Remove or override dangerous builtins to prevent privilege escalation 

4. Integrate an **MCP server** 

   - Mandatory tools must be integrated into the agent 

   - MCP tools, resources, and prompts must be exposed 

   - MCP tools must be callable as Python functions from the sandbox 

   - The system will be tested with an **unknown MCP server** 

   - The MCP tool files (mcp_tools_mbpp.py, mcp_tools_swebench.py) should be located at the root of your repository 

   - Both stdio and streamable HTTP transports must be supported for MCP server connections 

5. Generate a sandbox manual to be fed to the LLM prompt, which must include the MCP tools doc, or how to access it. 



```
Thesandboxmanualshouldbedynamicallygeneratedfromtheconnected
MCPserver’stoolschemas—toolnames,descriptions,andparameter
types.WhenadifferentMCPserverisconnected,themanualshould
automaticallyreflectthatserver’stools.
ThemanualiswhattheLLMreadstounderstandwhattoolsare
availableandhowtocallthem.
```

Sandbox limits and behavior must be configurable using **Pydantic models and JSON configuration files** . 

15 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

```
classSandboxConfig(BaseModel):
"""Sandboxconfigurationforstudentsolutions.
```

```
Usesallowlistapproach:onlyimportsinauthorized_importsareallowed.
Everythingelseisblockedbydefault.
"""
authorized_imports:List[str]=Field(default_factory=lambda:[
"math","math.*",
"collections","collections.*",
"itertools","re","json",
"typing","typing.*",
"functools","operator",
"heapq","bisect","copy",
"string","random",
"datetime","datetime.*",
"array","cmath",
])
allowed_directories:List[str]=Field(default_factory=lambda:[
"/testbed","/tmp/agent"
])
max_execution_time_seconds:int=30
max_memory_mb:int=512
```

An entry ending in `.*` also allows importing that module’s submodules (e.g. `collections.*` permits `collections.abc` ). 

When a different MCP server is connected, the sandbox should dynamically discover and expose that server’s tools. Your mandatory tools are only present when your own MCP server is connected. 



```
Thesandboxisthecentralexecutionlayer.ItconnectstoanMCP
serverandexposesitstoolsascallablePythonfunctionswithin
thesandboxnamespace.ThesandboxwrapstheMCPclient,notthe
otherwayaround.ThesandboxandMCPtoolsareindependentsecurity
domains:thesandboxrestrictswhatLLM-generatedPythoncodecan
do(imports,paths,timeout,memory),whileMCPtoolactionshappen
outsidethesandboxandarenotsubjecttothesandboxtimeout(e.g.
atoolspawninganexternalprocess).
```



```
Youareexpectedtoimplementthesecuritymechanismsusingonly
standardPythonlibrariesandbuiltins.Noexternalpackageslike
RestrictedPythonareallowed.
```

16 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

### **Sandbox isolation approaches** 



```
Thinkaboutit:untrustedcodeinsideyourownprocessorina
separateone?Eachchoicetradesoffsecurityboundaries,timeout
handling(howdoyoukillrunawaycode?),andcommunication(howdo
yougetresultsback?).Multiplevalidapproachesexist,pickwhat
fitsyourarchitecture.
```

## **V.3 MBPP Agent** 

In this part, you will implement an autonomous agent dedicated to solving **MBPP (Mostly Basic Python Problems)** tasks. 

1. Implement an **agent CLI interface** 

```
#1.Dumpatask
cdmoulinette
uvrunmoulinette_evaldumpmbpp--output../cache/mbpp_task.json
#2.Runyouragent
cd../student
uvrunpython-magent_mbpp--task-file../cache/mbpp_task.json\
--output../cache/mbpp_solution.json\
--model-name"model/name"--provider-url"https://provider.api/v1"
#3.Validatesolution
cd../moulinette
uvrunmoulinette_evalvalidatembpp../cache/mbpp_task.json\
../cache/mbpp_solution.json
```

   - Task loading 

   - Agent execution 

2. Implement **MBPP MCP tools** 

   - `run_tests(code, test_list)` 

Run a candidate solution against the given test assertions. It returns a JSON string with a `success` boolean (whether all assertions passed) and an `output` field. 

   - You may implement any additional tools you consider useful 

3. Define **Pydantic models** for: 

   - Task input 

17 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

```
classMBPPTaskInput(BaseModel):
"""InputforMBPPtaskevaluation."""
task_id:int
task_definition:str
function_definition:str
test_imports:List[str]=Field(default_factory=list)
test_list:List[str]=Field(default_factory=list)
```

   - Agent output: same `StepMetrics` / `SolutionOutput` models as in Section 5.1 ( `benchmark="mbpp"` , `solution` = your function code) 

4. Design your agent to operate within the limits defined in Section 6.1 (iterations, tokens, time). The evaluation validates that your agent’s output stays within these limits. `max_iterations` should be a configurable parameter of your agent loop. 

External LLM providers are allowed, provided the interface remains compliant with the project constraints. 

## **V.4 SWE-bench Agent** 

This part focuses on implementing an autonomous agent capable of solving **SWE-bench** tasks inside Dockerized environments. 

For SWE-bench, both approaches are valid: 

- (a) deploy the sandbox inside the Docker container, or 

- (b) run the sandbox on the host with MCP tools bridging into Docker. 

Regardless of choice, sandbox security constraints must be enforced. 

- Fix real bugs or implement features in real repositories 

- Explore codebases inside Docker containers, you are responsible to clean it after your program execution 

- Generate and submit valid patches using ’git -c core.fileMode=false diff’ 



```
WhentestingyourSWE-benchtoolsinisolation,themoulinettesets
theenvironmentvariableTESTBED_PATHtotherepositoryrootbefore
startingyourMCPserver.Yourtoolsmustreadthisexactvariable
nametolocatetherepository.
```

You may install additional dependencies inside the Docker container (e.g., ruff, jedi, tree) to enhance your tools. 

18 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



```
Forinitialtesting,trythesimplesttaskfirst:
sympy__sympy-14711,sympy__sympy-13480,pydata__xarray-4629.What
happenswhenyouremoveunusedtoolsfromyoursetup?
```

1. Implement an **agent CLI interface** 

```
#1.Dumpatask
cdmoulinette
uvrunmoulinette_evaldumpswebench--output../cache/swebench_task.json
#2.Runyouragent
cd../student
uvrunpython-magent_swebench--task-file../cache/swebench_task.json\
--output../cache/swebench_solution.json\
--model-name"model/name"--provider-url"https://provider.api/v1"
#3.Validatesolution
cd../moulinette
uvrunmoulinette_evalvalidateswebench../cache/swebench_task.json\
../cache/swebench_solution.json
```

2. Implement **SWE-bench MCP tools** 

   - Tools must follow the specification defined in Mandatory Tools 

   - You may implement any additional tools you consider useful 

3. Define **Pydantic models** for: 

   - Task input 

```
classSWEBenchTaskInput(BaseModel):
```

```
"""InputforaSWE-benchtask,providedbythemoulinette.
```

```
Youragentreceivesthisandmustproduceagitpatchthatfixes
theissue.
"""
instance_id:str=Field(...,description="SWE-benchinstance
identifier(e.g.,'sympy__sympy-23534')")
problem_statement:str=Field(...,description="TheGitHubissue
description,whatneedstobefixed")
docker_image:str=Field(...,description="FullDockerimage
nametopull(e.g.,'swebench/sweb.eval.x86_64.
sympy_1776_sympy-23534:latest')")
eval_script:str=Field(...,description="Bashscripttorun
insidethecontainertoevaluatethepatch")
```

19 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

```
hints_text:str=Field(default="",description="Optionalhints
abouttheissue(maybeempty)")
repo:str=Field(default="",description="Repositoryname(e.g.,
'sympy/sympy')")
```

   - Agent output (patch): same `StepMetrics` / `SolutionOutput` models as in Section 5.1 ( `benchmark="swebench"` , `solution` = your git patch) 

4. Enforce **hard limits** as defined in Section 6.1 

External LLM providers are allowed, provided the agent remains fully compatible with the evaluation infrastructure. 

`SolutionOutput` must include a `system_prompt` field containing the full system prompt sent to the LLM. Each step in `steps` must include `llm_output` , `sandbox_input` , and `sandbox_output` fields logging the raw LLM response, the Python code sent to the sandbox, and the execution result. A `retries` field tracks how many LLM API retries were needed for the step. 

```
{
"steps":[
{
"step":1,
"llm_output":"I'llreadthefiletounderstandthemodule.\n```python\
nresult=read_file(filepath=\"/testbed/src/module.py\")\n```",
"sandbox_input":"result=read_file(filepath=\"/testbed/src/module.py\")
",
"sandbox_output":"defsolve(x):\nreturnx+1\n...",
"retries":0,
"input_tokens":1234,
"output_tokens":567,
"..."
}
]
}
```

This metadata is inspected during evaluation to verify the agent solved tasks through legitimate code exploration and reasoning, not by looking up solutions from pull requests, issues, or external sources. 

## **V.5 Mandatory Tools** 

You must implement all the following tools. Each tool is exposed by the MCP (Model Context Protocol) server and will be tested independently in the context of the SWEbench benchmark. 

20 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

### **V.5.1 File System Tools** 

- `read_file(filepath, start_line, end_line)` Read the content of a file with line numbers. The output format must be similar to `cat -n` : 

```
<line_number>:<line_content>
<line_number>:<line_content>
...
```

- `edit_file(filepath, old_str, new_str)` Replace an exact string in a file with a new string. 

- `list_files(directory, pattern)` List files in a directory matching a given pattern. 

### **V.5.2 Code Search Tools** 

- `search_code(pattern, file_pattern)` Perform a grep-like search in the codebase. The output must follow this format: 

```
/absolute/path_to_file.py:<line_number><line_content>
/absolute/path_to_other_file.py:<line_number><line_content>
...
```

- `search_function_or_class_definition_in_code(name)` Find the definition of a function or a class. The output format must be similar to search_code format. 

- `find_references(name, filepath, line)` Find all usages of a symbol (function or class). The output format must be similar to search_code format. 

### **V.5.3 Execution Tools** 

- `run_tests()` Execute the evaluation script. 

_•_ `get_patch()` Retrieve the unified `git diff` of all changes made to the repository, depending on the implementation. 

- `run_command(command, workdir)` Execute a shell command in the specified working directory. Returns the command’s stdout, stderr, and exit code. 

21 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

## **V.6 LLM API Providers** 

To implement your agent, you will need to perform calls to **Large Language Model (LLM) APIs** . Several providers offer free tiers or usage quotas that are sufficient for development and experimentation. 

The list below is provided for **illustrative purposes only** . It is based on publicly available resources and may evolve over time. 

**You are free to use other providers** as long as your system complies with the project requirements (free tier, multiple API tokens per provider). 

The dataset your agent is evaluated on is called SWE-bench Verified. Knowing this, you can find: 

- **Model leaderboards** : which LLMs perform best on real-world coding tasks? 

- **Agent system descriptions** : how do the top-performing systems design their agent loop, tools, and prompts? 

- **Per-task traces and evaluations** — how does a specific model perform on the exact task you’re iterating on? This can help you choose the right model for your first debugging cycles. 



```
Whathappensifthemodelkeepsgeneratingafteratoolcallinstead
ofwaitingforrealexecutionoutput?Useastop_sequences(orstop)
APIparameter(e.g.<end_code>,</tool_call>)tostopgenerationat
thetokenthatendsacodeblock,otherwisethemodelmayhallucinate
fictionaltooloutputinsteadofwaitingfortherealone.
```

### **V.6.1 Examples of Free Providers** 

Examples include OpenRouter, Together AI, Groq, Google AI Studio (Gemini), Mistral AI, Cohere, Fireworks AI, Perplexity AI, and Anyscale (non-exhaustive). Ensure your implementation supports **multiple API keys per provider** and consider implementing provider fallback. Rate limits and quotas may vary, especially under load during evaluation. 

#### **Important:** 

- This list is **not exhaustive and not contractual** . 

- Access conditions, quotas, and available models may change over time. 

- Learners are encouraged to explore additional providers or to use self-hosted models if needed. 

- **The entire solution must rely exclusively on free tiers.** 

   - No paid plans, purchased credits, or billing-enabled accounts are allowed. 

   - The project must be fully executable using only free quotas at evaluation time. 

22 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

- **Multi-token management is mandatory.** 

   - Your system must support **multiple API tokens per provider** . 

   - Token rotation must be implemented to handle rate limits and quota exhaustion. 

- Your implementation must be sufficiently **abstract** to allow switching providers without major refactoring. 



<!-- Start of picture text -->
i<br><!-- End of picture text -->

```
Thechoiceofproviderisnotgraded.Thequalityofyour
abstraction,errorhandling,andoverallarchitectureis.
```

## **V.7 Model Benchmark Report** 

Raw solve rate only tells part of the story of which model is best for your agent, exploration efficiency, token cost, provider reliability, and iteration discipline matter too. You must produce a benchmark report ( `BENCHMARK_REPORT.md` at the root of your repository) comparing at least **5 models** across at least **2 providers** on the same set of at least **3 SWE-bench tasks** . 



<!-- Start of picture text -->
g<br><!-- End of picture text -->

```
Free-tierprovidersenforcedailytoken/requestquotas,andrunning
5modelscanexhaustonebeforeyou’redone.Sincemoreproviders
meansmoreindependentquotastodrawfrom,werecommendkeeping
morethan2providersreadyratherthanthebareminimum,soasingle
quotawalldoesn’tstallyourbenchmarkrun.
```

Your report must include: 

1. **Setup** : Which models/providers were compared, which tasks were used, and why those tasks were selected 

2. **Results table** : For each model × task combination: 

   - Pass/Fail 

   - Iterations used 

   - Total input tokens 

   - Total output tokens 

   - Wall-clock time 

3. **Provider reliability** : For each model/provider: 

   - Average response time per request 

   - Number of retries needed (rate limits, timeouts, errors) 

23 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

   - Overall availability during benchmark runs 

4. **Intermediary metrics** (at least 2 of the following): 

   - Step at which the agent first reads/edits the file that appears in the final patch (exploration efficiency) 

   - Step at which test failures first decrease vs baseline (partial progress) 

   - Iterations between “tests first pass” and `final_answer` (submission discipline — zero is ideal) 

These metrics can be measured manually by inspecting your `solution.json` files — automation is not required. What matters is the analysis, not the tooling. 

5. **Ablation study** : At least one before/after comparison of a change to your agent (prompt, tools, parameters) on the same tasks with the same model 

6. **Conclusions** : Which model(s) you selected for your final pipeline and why. Which models can be disregarded and why. Based on your data. 

The backing `solution.json` files must be present in your repository. 

24 

# **Chapter VI** 

# **Evaluation** 

During evaluation, API keys and configuration are provided via a ‘.env‘ file passed as a required argument to evaluation scripts: 

```
./exam_TYPE.sh--student-path./student--moulinette-path./moulinette--env-
file/path/to/.env
```

Your CLI must support loading API keys from environment variables. Students should use standard environment variables (e.g., ‘OPENROUTER_API_KEY‘). 

|**exam_mbpp.sh**|**exam_swebench.sh**|**exam_sandbox.sh**|
|---|---|---|
|5 random tasks|3 random tasks|Security tests|
|Pass: 4/5|Pass: 2/3|Pass: ALL|
|For each task:|For each task:|Tests:|
|1. dump task<br>2. run agent|1. dump task<br>2. run agent|- import block<br>- builtin block|
|3. validate|3. validate<br>4. container cleanup|- network block<br>- path restrict<br>- timeout<br>- memory limit<br>- MCP protocol|



Table VI.1: Summary of exam scripts and tasks. Iteration/token/timeout limits are detailed in Section 6.1. 

25 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



## **VI.1 Hard Requirements and Limits** 

Your implementation must strictly respect the following execution limits. Exceeding any of these limits will result in a failure of the corresponding task. 

### **VI.1.1 MBPP Limits** 

|**Metric**|**Limit**|
|---|---|
|Maximum iterations|10|
|Maximum input tokens|6,000|
|Maximum output tokens|1,500|
|Timeout|120 seconds|



### **VI.1.2 SWE-bench Limits** 

|**Metric**|**Limit**|
|---|---|
|Maximum iterations|30|
|Maximum input tokens|300,000|
|Maximum output tokens|10,000|
|Timeout|900 seconds|



- Token limits are **cumulative** across all iterations of a single task (all Thought → Code →Observation cycles combined). 

- Thinking/reasoning tokens (when used by reasoning models) count toward the limit just like all other tokens. 

- If your chosen model’s reasoning tokens make limits tight, consider using a nonreasoning model. 

26 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 

- The timeout is enforced by force-killing your agent’s process (and any process it spawned) with `SIGTERM` then `SIGKILL` if it hasn’t returned in time, not just checked after the fact. For SWE-bench, make sure your Docker container cleanup can still run in that case (e.g. a signal handler), or complete quickly enough that it usually isn’t reached. 

## **VI.2 Pass Criteria** 

|**Benchmark**|**Tasks**|**Pass Threshold**|
|---|---|---|
|MBPP|5 random tasks|4 out of 5|
|SWE-bench|3 random tasks|2 out of 3|



**No retries are allowed during examination** : a failed task is not re-run. This does not restrict your own agent’s internal LLM-call retry logic, tracked by `StepMetrics.retries` . 

## **VI.3 Grading Criteria** 

To pass the project, you must satisfy **all** of the following conditions: 

- Meet the pass criteria for both MBPP and SWE-bench 

- Respect all iteration, token, and timeout limits 

- All mandatory tools pass independent tests 

- The sandbox passes isolation and security tests 



```
HardcodedAPIkeysinyourcodeareasecurityfailure.AllAPI
keysmustbeloadedfromenvironmentvariablesorconfigurationfiles
(.env).AnyAPIkeyfoundinyoursourcecodewillbeflaggedduring
evaluation.
```

## **VI.4 What We Will Test in the Review** 

- Correctness of mandatory tools 

- Correct implementation of the agent reasoning loop 

- Sandbox security and isolation guarantees 

- Model benchmarking results and token statistics 

- Code quality, robustness, and overall architecture 

27 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



```
Duringtheevaluation,youwillbeaskedtomakesmalllive
modificationstoyouragentandre-runitonanMBPPtask.This
teststhatyouunderstandyourowncodebaseandthatthedatain
solution.jsoncomesfromrealexecution,notfabricatedvalues.Each
modificationshouldtake2–5minutes.Ifyoucannotfindwhereto
makeachange,itindicatesyoudonotunderstandyourowncodebase.
Youwillbeaskedtorevertallchangesaftertheexercise(e.g.,git
checkout).
```

### **VI.4.1 AI Safety in Evaluation** 

Building an autonomous code agent raises important safety considerations beyond just sandbox security. During evaluation, we verify that your agent solves tasks through legitimate reasoning and code exploration — not by exploiting shortcuts. 

Your agent must **not** : 

- Fetch solutions from pull requests, issues, or external sources 

- Use memorized patches from its training data without genuine exploration 

- Bypass the sandbox security constraints 

- Access resources outside the provided task context 

The `SolutionOutput` includes `system_prompt` , `llm_output` , `sandbox_input` , and `sandbox_output` fields precisely so that evaluators can trace the agent’s reasoning process. This transparency is a core part of responsible AI development. 

**Violations will result in a grade of 0.** 

## **VI.5 Evaluation logging structure** 

Evaluation results are stored in: 

- <mark>`./evaluations/EVAL_TYPE/YYYY-MM-DD_HH-MM-SS/task_id/task.json, solution.json, stdout.log, stderr.log`</mark> 

28 

# **Chapter VII** 

# **Readme Requirements** 

A `README.md` file must be provided at the root of your Git repository. Its purpose is to allow anyone unfamiliar with the project (peers, staff, recruiters, etc.) to quickly understand what the project is about, how to run it, and where to find more information on the topic. 

The `README.md` must include at least: 

- The very first line must be italicized and read: _This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]]._ 

- A “ **Description** ” section that clearly presents the project, including its goal and a brief overview. 

- An “ **Instructions** ” section containing any relevant information about compilation, installation, and/or execution. 

- A “ **Resources** ” section listing classic references related to the topic (documentation, articles, tutorials, etc.), as well as a description of how AI was used — specifying for which tasks and which parts of the project. 

- ➠ **Additional sections may be required depending on the project** (e.g., usage examples, feature list, technical choices, etc.). 

_Any required additions will be explicitly listed below._ 

Your `README.md` must include: 

- System architecture 

- Agent loop explanation 

- Sandbox design 

- Tool implementation details 

- Benchmark results and analysis 

29 

Agent Smith 

Autonomous reasoning, code <u>generation,</u> and execution 



```
YourREADMEmustbewritteninEnglish.
```



<!-- Start of picture text -->
30<br><!-- End of picture text -->

# **Chapter VIII Submission** 

Submit your project in your Git repository. Your repository must contain: 

- The internal architecture and directory structure of your submission are left to you. 

- Configuration files for sandbox and models 

- `README.md` 



```
DonotincludeDockerimages,largemodelweights,orgenerated
outputs.
```

31 


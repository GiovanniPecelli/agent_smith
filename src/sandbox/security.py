import ast
import builtins
import io
import resource
import signal
import socket
import time
from collections.abc import Callable
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.models import SandboxConfig


class FinalAnswerException(Exception):
    """Special exception raised when the agent calls final_answer().
    
    Used to immediately interrupt Python code execution and deliver
    the final solution back to the agent orchestrator.
    """
    def __init__(self, answer: Any):
        self.answer = answer
        super().__init__(str(answer))


class SecurityError(Exception):
    """Base exception raised when sandboxed code attempts to violate safety rules."""


@dataclass
class SandboxExecutionResult:
    """Result of executing a code snippet inside the sandbox.
    
    Collects standard output (stdout), errors, execution time,
    and whether the agent finished the task by calling final_answer().
    """
    stdout: str = ""
    stderr: str = ""
    error: str | None = None
    is_final: bool = False
    final_answer: str | None = None
    execution_time_seconds: float = 0.0


class Sandbox:
    """Secure execution environment for LLM-generated Python code.
    
    Enforces:
    - Import restrictions (allowlist configured in SandboxConfig)
    - Filesystem path restrictions (allowed_directories only)
    - Total block on outbound/inbound network connections
    - Memory usage limits and execution timeout
    - Native injection of final_answer(...) and external MCP tool wrappers
    - Persistent namespace variables between consecutive steps of a task
    """

    _BLOCKED_ATTRS = frozenset({
        "__subclasses__",
        "__bases__",
        "__base__",
        "__mro__",
        "__globals__",
        "__builtins__",
        "__code__",
        "__closure__",
        "__func__",
        "__self__",
        "__dict__",
        "__loader__",
        "__spec__",
        "__import__",
    })

    def __init__(self, config: SandboxConfig):
        """Initialize the sandbox with security limits and configuration."""
        self.config = config

        # native functions
        self._orig_open = builtins.open
        self._orig_import = builtins.__import__
        self._orig_socket = socket.socket

        # self.namespace is the persistent globals() for exec():
        # - safe builtins (open, __import__), final_answer, MCP tools
        # - variables created by LLM that persist across execute() calls
        # Populated by _setup_namespace() below
        self.namespace: dict[str, Any] = {}
        self._setup_namespace()

        # saving the original memory limit
        self._orig_rlimit = resource.getrlimit(resource.RLIMIT_AS)

    def _setup_namespace(self) -> None:
        """Prepare the execution global namespace.
        
        Injects:
        - Guarded builtins (safe_open, safe_import)
        - The native final_answer function
        - Disables or removes dangerous builtins
        """
        # NOTE: copy the built-in python dict: have all the built-in python
        # function as: open, print, len, sum, int, str, __import__, ecc.
        safe_builtins = builtins.__dict__.copy()

        # remove dangerous builtins functions
        for name in ("eval", "exec", "compile", "breakpoint"):
            safe_builtins.pop(name, None)

        def _blocked_input(*args: Any, **kwargs: Any) -> Any:
            raise PermissionError(
                "Interactive input() is blocked by sandbox policy."
            )

        safe_builtins["open"] = self._safe_open
        safe_builtins["__import__"] = self._safe_import
        safe_builtins["input"] = _blocked_input

        self.namespace = {
            "__name__": "__sandbox__",
            "__doc__": None,
            "__builtins__": safe_builtins,
            "final_answer": self._final_answer,
        }

    def _validate_ast(self, code: str) -> None:
        """
        Inspect AST before execution to block dunder attribute introspection.
        """
        tree = ast.parse(code, mode="exec")
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr in self._BLOCKED_ATTRS
            ):
                raise SecurityError(
                    f"Access to attribute '{node.attr}' "
                    "is blocked by sandbox policy."
                )

    def _is_import_authorized(self, module_name: str) -> bool:
        """
        Check if a module is authorized by the authorized_imports allowlist
        
        Supports wildcards such as 'math.*', 'collections.*', 'typing.*'.
        Returns True if permitted, False otherwise.
        """
        if not module_name:
            return False

        for pattern in self.config.authorized_imports:
            if pattern.endswith(".*"):
                prefix = pattern[:-2]
                if module_name == prefix or module_name.startswith(prefix + "."):
                    return True
            else:
                if module_name == pattern:
                    return True
        
        return False

    def _safe_import(
        self,
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple = (),
        level: int = 0,
    ) -> Any:
        """Guarded replacement for the built-in __import__.
        
        Verifies that the requested module is present in authorized_imports.
        If unauthorized, raises an explicit ImportError.
        """
        if self._is_import_authorized(name):
            return self._orig_import(name, globals, locals, fromlist, level)
        else:
            raise ImportError(
                f"Import of module '{name}' is blocked by sandbox policy."
            )


    def _is_path_allowed(self, filepath: str | Path) -> bool:
        """Check if a file path is within one of the allowed_directories.
        
        Resolves absolute paths and symbolic links to prevent path traversal
        attacks (e.g., '../../etc/passwd').
        Returns True if permitted, False otherwise.
        """
        if not filepath:
            return False

        try:
            target_path = Path(filepath).resolve()
            for allowed_str in self.config.allowed_directories:
                allowed_path = Path(allowed_str).resolve()
                if target_path.is_relative_to(allowed_path):
                    return True
        except Exception:
            return False

        return False

    def _safe_open(self, file: Any, *args: Any, **kwargs: Any) -> Any:
        """Guarded replacement for the built-in open() function.
        
        Intercepts file open operations: if the target path is outside
        allowed directories, access is blocked by raising a PermissionError.
        """
        if isinstance(file, int):
            raise PermissionError(
                "Opening raw file descriptors is blocked by sandbox policy"
            )

        if not self._is_path_allowed(file):
            raise PermissionError(
                f"Access to path '{file}' is blocked by sandbox policy"
            )

        # _orig_open call the original open() function
        return self._orig_open(file, *args, **kwargs)

    def _block_network(self) -> None:
        """Disable socket creation to prevent all network communication."""
        def blocked_socket(*args: Any, **kwargs: Any) -> Any:
            raise PermissionError(
                "Network access is blocked by sandbox policy"
            )

        socket.socket = blocked_socket

    def _apply_memory_limit(self) -> None:
        """Set virtual memory limit (RLIMIT_AS) as defined in config.max_memory_mb."""
        limit_bytes = self.config.max_memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))

    def _final_answer(self, answer: Any) -> None:
        """Native function injected directly into the sandbox namespace.
        
        Captures the solution value and raises FinalAnswerException to signal
        to the orchestrator loop that the task has been solved.
        """
        raise FinalAnswerException(answer)

    def register_tool(self, name: str, func: Callable) -> None:
        """Register an external MCP tool inside the sandbox namespace.
        
        Allows the LLM to call tools such as read_file(...), edit_file(...),
        run_tests() as standard Python functions.
        """
        self.namespace[name] = func

    def execute(self, code: str) -> SandboxExecutionResult:
        """Execute a Python code snippet inside the secure sandbox.
        
        Workflow:
        1. Set execution timeout using signal.alarm(max_execution_time_seconds)
        2. Redirect stdout and stderr to memory buffers to capture output
        3. Execute the code using exec(code, self.namespace)
        4. Catch FinalAnswerException, syntax errors, and timeout events
        5. Propagate KeyboardInterrupt and SystemExit uncaught for clean shutdown
        6. Return a structured SandboxExecutionResult
        """
        result = SandboxExecutionResult()
        start_time = time.perf_counter()
        
        # apply the memory and network control
        self._apply_memory_limit()
        self._block_network()

        # Setup timeout con signal.alarm
        def timeout_handler(signum, frame):
            raise TimeoutError(
                "Execution exceeded "
                f"{self.config.max_execution_time_seconds}s limit"
            )
        
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        # TIME START: send a signal in "max_execution_time_seconds"
        signal.alarm(self.config.max_execution_time_seconds)

        # stdout/stderr catching - io. create a file in the memory, is like
        # a text file but live only in the ram memory (in the heap)
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        
        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                self._validate_ast(code)
                # exec(code, self.namespace) is like execute python in REPL
                # >>python ...
                # the result is saved in the namespace dict to let persistence
                # NOTE: 
                # Normalmente exec(code) userebbe le variabili globali del tuo
                # file security.py. Passandogli self.namespace, dici a Python:
                # "Esegui questo codice dentro questo dizionario chiuso,
                # facendogli credere che siano le sue variabili globali"
                exec(code, self.namespace)
            
            result.stdout = stdout_buf.getvalue()
            result.stderr = stderr_buf.getvalue()
        except FinalAnswerException as e:
            # agent called final_answer() - completed task
            result.stdout = stdout_buf.getvalue()
            result.stderr = stderr_buf.getvalue()
            result.is_final = True
            result.final_answer = str(e.answer)

        except SyntaxError as e:
            result.error = f"SyntaxError: {e.msg} at line {e.lineno}"
            result.stderr = stderr_buf.getvalue()

        except TimeoutError as e:
            result.stdout = stdout_buf.getvalue()
            result.stderr = stderr_buf.getvalue()
            result.error = f"{e} (partial output captured)"

        except MemoryError:
            result.stdout = stdout_buf.getvalue()
            result.stderr = stderr_buf.getvalue()
            result.error = (
                "MemoryError: Exceeded "
                f"{self.config.max_memory_mb}MB limit"
            )

        except Exception as e:
            result.stdout = stdout_buf.getvalue()
            result.stderr = stderr_buf.getvalue()
            result.error = f"{type(e).__name__}: {e}"
            
        finally:
            # ALWAYS: alarm deactivation and restore the orignial handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
            socket.socket = self._orig_socket

        # CHECK the time started in line 235
        result.execution_time_seconds = time.perf_counter() - start_time
        return result

    def reset(self) -> None:
        """
        Reset the sandbox namespace back to its initial state for a new task.
        """
        if self._orig_socket is not None:
            socket.socket = self._orig_socket

        self._setup_namespace()
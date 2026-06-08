"""Minimal MCP (Model Context Protocol) JSON-RPC client over stdio.

Used by minimax-web-search and minimax-image-understand skills to talk to
the upstream ``minimax-coding-plan-mcp`` server.

This is a self-contained client (Python 3.9+ stdlib only). It spawns the
server, performs the JSON-RPC handshake, makes one tool call, and exits.

Protocol: line-delimited JSON (one JSON object per line, terminated by ``\\n``).
This is what FastMCP (which the upstream server uses) accepts. The MCP
spec also allows LSP-style Content-Length headers, but FastMCP is line-based.

Reference: https://modelcontextprotocol.io
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from typing import Any

# Default command to spawn the upstream MCP server.
# Override by passing ``cmd=[...]`` to McpClient.
DEFAULT_MCP_CMD = ["uvx", "minimax-coding-plan-mcp", "-y"]

# Env vars that, if set in our parent, would cause the child to import the
# wrong modules (e.g. shadowing the upstream ``minimax_mcp`` package).
_PYTHON_ENV_VARS = (
    "PYTHONPATH",
    "PYTHONHOME",
    "PYTHONSTARTUP",
    "PYTHONUSERBASE",
    "PYTHONBREAKPOINT",
)


class McpError(RuntimeError):
    """Raised when the MCP server returns an error or our I/O fails."""


def _scrub_python_env(env: dict[str, str]) -> dict[str, str]:
    """Remove vars that would shadow the child's own Python site-packages."""
    return {k: v for k, v in env.items() if k not in _PYTHON_ENV_VARS}


class McpClient:
    """One-shot JSON-RPC client for one MCP server.

    Use as a context manager:

        with McpClient(env) as c:
            tools = c.list_tools()
            result = c.call_tool("web_search", {"query": "..."})
    """

    def __init__(
        self,
        env: dict[str, str],
        cmd: list[str] | None = None,
        startup_timeout_s: float = 30.0,
    ):
        self.env = env
        self.cmd = cmd or list(DEFAULT_MCP_CMD)
        self.startup_timeout_s = startup_timeout_s
        self._proc: subprocess.Popen | None = None
        self._stderr_thread: threading.Thread | None = None
        self._stderr_lines: list[str] = []
        self._next_id = 1
        self._initialized = False

    # ---- context manager ---------------------------------------------------

    def __enter__(self) -> "McpClient":
        self._start()
        return self

    def __exit__(self, *exc: Any) -> None:
        self._stop()

    # ---- lifecycle ---------------------------------------------------------

    def _start(self) -> None:
        # Merge user env on top of a cleaned parent env (no PYTHONPATH leakage
        # into the child, which would shadow upstream ``minimax_mcp``).
        merged_env = _scrub_python_env({**os.environ, **self.env})
        try:
            self._proc = subprocess.Popen(
                self.cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=merged_env,
                bufsize=0,
            )
        except FileNotFoundError as e:
            raise McpError(
                f"failed to spawn {self.cmd[0]!r}: {e}. "
                f"Is `uv`/`uvx` installed? (`brew install uv` or `pip install uv`)"
            ) from e
        # Drain stderr in the background so the child doesn't block on a full pipe.
        self._stderr_thread = threading.Thread(
            target=self._drain_stderr, daemon=True
        )
        self._stderr_thread.start()
        # MCP requires initialize handshake before any other call.
        self._initialize()

    def _stop(self) -> None:
        if self._proc is None:
            return
        if self._proc.poll() is None:
            try:
                self._proc.terminate()
                self._proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._proc.kill()
                self._proc.wait(timeout=2)
        self._proc = None
        self._initialized = False

    def _drain_stderr(self) -> None:
        if self._proc is None or self._proc.stderr is None:
            return
        for line in iter(self._proc.stderr.readline, b""):
            try:
                self._stderr_lines.append(line.decode("utf-8", "replace").rstrip())
            except Exception:
                pass

    def _stderr_text(self, max_lines: int = 20) -> str:
        return "\n".join(self._stderr_lines[-max_lines:])

    # ---- protocol: line-delimited JSON -------------------------------------

    def _send(self, payload: dict[str, Any]) -> None:
        assert self._proc and self._proc.stdin
        line = json.dumps(payload, ensure_ascii=False) + "\n"
        try:
            self._proc.stdin.write(line.encode("utf-8"))
            self._proc.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            raise McpError(
                f"MCP server closed stdin unexpectedly: {e}. stderr:\n{self._stderr_text()}"
            ) from e

    def _recv(self, timeout_s: float = 60.0) -> dict[str, Any]:
        """Read one JSON object from the server (line-delimited)."""
        assert self._proc and self._proc.stdout
        deadline = time.time() + timeout_s
        line = b""
        while True:
            if time.time() > deadline:
                raise McpError(
                    f"timeout ({timeout_s}s) waiting for JSON line. stderr:\n{self._stderr_text()}"
                )
            chunk = self._proc.stdout.readline()
            if not chunk:
                raise McpError(
                    f"MCP server closed stdout. stderr:\n{self._stderr_text()}"
                )
            line += chunk
            if chunk.endswith(b"\n"):
                break
        try:
            return json.loads(line.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise McpError(
                f"non-JSON from MCP: {line[:200]!r}. stderr:\n{self._stderr_text()}"
            ) from e

    def _request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        timeout_s: float = 60.0,
    ) -> dict[str, Any]:
        if not self._initialized and method != "initialize":
            raise McpError(f"must call initialize() before {method}()")
        msg_id = self._next_id
        self._next_id += 1
        req: dict[str, Any] = {"jsonrpc": "2.0", "id": msg_id, "method": method}
        if params is not None:
            req["params"] = params
        self._send(req)
        resp = self._recv(timeout_s=timeout_s)
        if "error" in resp:
            err = resp["error"]
            raise McpError(
                f"MCP error {err.get('code')}: {err.get('message')} "
                f"(data={err.get('data')!r})"
            )
        return resp.get("result", {})

    # ---- high-level MCP methods -------------------------------------------

    def _initialize(self) -> None:
        result = self._request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "minimax-skill-wrapper",
                    "version": "0.1.0",
                },
            },
            timeout_s=self.startup_timeout_s,
        )
        server_info = result.get("serverInfo", {})
        if server_info:
            # Note: this is the MCP *server* name and version, not the model.
            # The actual model (M3) lives behind the API the server wraps.
            print(
                f"[minimax-skill] MCP server "
                f"{server_info.get('name')} v{server_info.get('version', '?')} "
                f"(backed by MiniMax-M3)",
                file=sys.stderr,
            )
        # Send initialized notification (no response expected)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self._initialized = True

    def list_tools(self) -> list[dict[str, Any]]:
        result = self._request("tools/list", {})
        return result.get("tools", [])

    def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        timeout_s: float = 60.0,
    ) -> dict[str, Any]:
        result = self._request(
            "tools/call",
            {"name": name, "arguments": arguments},
            timeout_s=timeout_s,
        )
        if result.get("isError"):
            raise McpError(
                f"tool {name!r} returned isError: "
                f"{self._extract_text(result)[:300]}"
            )
        return result

    @staticmethod
    def _extract_text(result: dict[str, Any]) -> str:
        """Concatenate all text fields from a tool result."""
        chunks: list[str] = []
        for item in result.get("content", []):
            if isinstance(item, dict) and item.get("type") == "text":
                chunks.append(item.get("text", ""))
        if chunks:
            return "\n".join(chunks)
        sc = result.get("structuredContent")
        if isinstance(sc, dict) and sc.get("type") == "text":
            return sc.get("text", "")
        return json.dumps(result, ensure_ascii=False)

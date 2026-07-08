"""Abstract base agent and supporting types for the Meridian agent framework."""

from __future__ import annotations

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class AgentState(str, Enum):
    IDLE       = "idle"
    RUNNING    = "running"
    WAITING    = "waiting"
    COMPLETED  = "completed"
    FAILED     = "failed"
    CANCELLED  = "cancelled"


@dataclass
class Tool:
    """A callable tool that an agent can invoke during reasoning."""
    name: str
    description: str
    parameters: Dict[str, Any]          # JSON Schema for tool input
    handler: Callable[..., Any]         # async or sync callable

    def to_anthropic_spec(self) -> Dict[str, Any]:
        """Convert to Anthropic tool-use API format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": self.parameters,
            },
        }


@dataclass
class RunContext:
    """Immutable context passed into every agent run."""
    run_id: str          = field(default_factory=lambda: str(uuid.uuid4()))
    org_id: str          = ""
    trigger: str         = "scheduled"   # "scheduled" | "manual" | "anomaly"
    metadata: Dict[str, Any] = field(default_factory=dict)
    started_at: float    = field(default_factory=time.time)


@dataclass
class AgentResult:
    """Structured output returned by an agent run."""
    run_id: str
    agent_id: str
    success: bool
    output: Dict[str, Any]
    reasoning_trace: List[str]    = field(default_factory=list)
    tokens_used: int              = 0
    duration_ms: float            = 0.0
    error: Optional[str]         = None


class BaseAgent(ABC):
    """
    Abstract base class for all Meridian AI agents.

    Subclasses must implement:
        - run(context)       — the agent's primary execution logic
        - _register_tools()  — return the list of Tools this agent can call
        - _system_prompt()   — the persona / instructions for the LLM
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        llm_service,          # LLMService injected at construction
        config: Dict[str, Any] = None,
    ) -> None:
        self.agent_id   = agent_id
        self.name       = name
        self._llm       = llm_service
        self.config     = config or {}
        self._state     = AgentState.IDLE
        self._tools     = self._register_tools()
        self._trace: List[str] = []

    # ── abstract interface ─────────────────────────────────────────────────

    @abstractmethod
    async def run(self, context: RunContext) -> AgentResult:
        """Execute the agent's primary task and return a structured result."""
        ...

    @abstractmethod
    def _register_tools(self) -> List[Tool]:
        """Return the tools available to this agent during LLM reasoning."""
        ...

    @abstractmethod
    def _system_prompt(self) -> str:
        """Return the system prompt that shapes this agent's behavior."""
        ...

    # ── shared utilities ───────────────────────────────────────────────────

    async def think(
        self,
        user_prompt: str,
        tools: Optional[List[Tool]] = None,
        max_rounds: int = 5,
    ) -> str:
        """
        Run an agentic reasoning loop:
          1. Send prompt + tools to the LLM
          2. If the LLM calls a tool, execute it and feed the result back
          3. Repeat until the LLM returns a final text response
        """
        messages = [{"role": "user", "content": user_prompt}]
        effective_tools = tools or self._tools

        for _ in range(max_rounds):
            response = await self._llm.chat(
                system=self._system_prompt(),
                messages=messages,
                tools=[t.to_anthropic_spec() for t in effective_tools],
            )

            # Final text answer
            if response.stop_reason == "end_turn":
                text = next(
                    (b.text for b in response.content if hasattr(b, "text")), ""
                )
                self._trace.append(f"LLM: {text[:200]}...")
                return text

            # Tool call(s) — execute and loop
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    tool = next((t for t in effective_tools if t.name == block.name), None)
                    if tool is None:
                        result_content = f"Error: unknown tool '{block.name}'"
                    else:
                        try:
                            result = tool.handler(**block.input)
                            if asyncio.iscoroutine(result):
                                result = await result
                            result_content = str(result)
                        except Exception as exc:
                            result_content = f"Error: {exc}"
                    self._trace.append(f"TOOL {block.name}: {result_content[:100]}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_content,
                    })

                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

        return "Max reasoning rounds reached without a final answer."

    @property
    def state(self) -> AgentState:
        return self._state

    def _set_state(self, state: AgentState) -> None:
        self._state = state
        self._trace.append(f"STATE -> {state.value}")
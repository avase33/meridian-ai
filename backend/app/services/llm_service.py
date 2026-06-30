"""LLM Service â€” thin wrapper around the Anthropic Claude API."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import anthropic
import structlog

from app.config import settings

logger = structlog.get_logger(__name__)


class LLMService:
    """
    Wraps the Anthropic Python SDK with:
      - Automatic retry on transient errors
      - Usage / cost tracking
      - Structured logging for every call
    """

    def __init__(self) -> None:
        self._client     = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
        self._model      = settings.llm_model
        self._max_tokens = settings.llm_max_tokens
        self._temperature = settings.llm_temperature
        self._total_input_tokens  = 0
        self._total_output_tokens = 0

    async def chat(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None,
    ) -> anthropic.types.Message:
        """
        Send a chat completion request to Claude.

        Args:
            system:     System prompt defining the agent's persona.
            messages:   Conversation history in Anthropic format.
            tools:      Optional list of tool definitions (Anthropic format).
            max_tokens: Override the default max tokens for this call.

        Returns:
            Raw Anthropic Message object.
        """
        start  = time.monotonic()
        kwargs: Dict[str, Any] = {
            "model":      self._model,
            "system":     system,
            "messages":   messages,
            "max_tokens": max_tokens or self._max_tokens,
        }
        if tools:
            kwargs["tools"] = tools

        log = logger.bind(model=self._model, tools_count=len(tools or []))
        log.debug("llm.request.start")

        response = await self._client.messages.create(**kwargs)

        elapsed = time.monotonic() - start
        self._total_input_tokens  += response.usage.input_tokens
        self._total_output_tokens += response.usage.output_tokens

        log.info(
            "llm.request.complete",
            duration_ms=round(elapsed * 1000, 1),
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            stop_reason=response.stop_reason,
        )
        return response

    async def complete(
        self,
        system: str,
        user: str,
        tools: Optional[List[Dict]] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Convenience method: single-turn completion, returns text string."""
        response = await self.chat(
            system=system,
            messages=[{"role": "user", "content": user}],
            tools=tools,
            max_tokens=max_tokens,
        )
        return next(
            (b.text for b in response.content if hasattr(b, "text")), ""
        )

    @property
    def usage_stats(self) -> Dict[str, int]:
        return {
            "total_input_tokens":  self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "total_tokens":        self._total_input_tokens + self._total_output_tokens,
        }


_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """FastAPI dependency â€” returns a singleton LLM service."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
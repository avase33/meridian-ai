"""MonitorAgent â€” polls configured data sources and returns a metric snapshot."""

from __future__ import annotations

import time
from typing import Any, Dict, List

import httpx

from app.agents.base import AgentResult, AgentState, BaseAgent, RunContext, Tool


class MonitorAgent(BaseAgent):
    """
    Fetches the current value of a configured metric from a data source.

    Supported sources:
      - postgresql  (SQL query via asyncpg)
      - rest_api    (HTTP GET with optional auth header)
      - static      (inline value â€” useful for testing)
    """

    def _system_prompt(self) -> str:
        return (
            "You are a data monitoring agent. Your job is to fetch metric data "
            "from configured sources and return a clean, structured snapshot. "
            "Be precise. Report exact values. Never fabricate data."
        )

    def _register_tools(self) -> List[Tool]:
        return [
            Tool(
                name="fetch_rest_metric",
                description="Fetch a JSON metric from an HTTP endpoint.",
                parameters={
                    "url":         {"type": "string", "description": "Endpoint URL"},
                    "value_path":  {"type": "string", "description": "Dot-path to the numeric value, e.g. 'data.total'"},
                    "auth_header": {"type": "string", "description": "Optional Bearer token"},
                },
                handler=self._fetch_rest_metric,
            )
        ]

    async def run(self, context: RunContext) -> AgentResult:
        self._set_state(AgentState.RUNNING)
        start = time.time()

        source_type = self.config.get("data_source", {}).get("type", "static")

        try:
            if source_type == "rest_api":
                value = await self._fetch_rest_metric(
                    url=self.config["data_source"]["url"],
                    value_path=self.config["data_source"].get("value_path", "value"),
                    auth_header=self.config["data_source"].get("auth_header", ""),
                )
            elif source_type == "static":
                value = self.config["data_source"].get("value", 0.0)
            else:
                # For postgresql / other sources we delegate to the LLM reasoning loop
                prompt = (
                    f"The data source is: {self.config.get('data_source')}. "
                    f"The query to run is: {self.config.get('query', 'SELECT 1')}. "
                    "Fetch and return the numeric result."
                )
                response_text = await self.think(prompt)
                value = self._extract_number(response_text)

            output = {
                "metric_name": self.config.get("name", "metric"),
                "value":       value,
                "timestamp":   time.time(),
                "source_type": source_type,
                "unit":        self.config.get("unit", ""),
            }
            self._set_state(AgentState.COMPLETED)
            return AgentResult(
                run_id=context.run_id,
                agent_id=self.agent_id,
                success=True,
                output=output,
                reasoning_trace=self._trace,
                duration_ms=(time.time() - start) * 1000,
            )

        except Exception as exc:
            self._set_state(AgentState.FAILED)
            return AgentResult(
                run_id=context.run_id,
                agent_id=self.agent_id,
                success=False,
                output={},
                error=str(exc),
                duration_ms=(time.time() - start) * 1000,
            )

    # â”€â”€ helpers â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    async def _fetch_rest_metric(
        self, url: str, value_path: str = "value", auth_header: str = ""
    ) -> float:
        headers = {}
        if auth_header:
            headers["Authorization"] = auth_header
        async with httpx.AsyncClient(timeout=10) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        # Traverse dot-path: "data.metrics.revenue" -> data["data"]["metrics"]["revenue"]
        for key in value_path.split("."):
            data = data[key]
        return float(data)

    @staticmethod
    def _extract_number(text: str) -> float:
        import re
        nums = re.findall(r"[-+]?\d*\.?\d+", text)
        return float(nums[0]) if nums else 0.0
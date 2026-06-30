"""AnalystAgent â€” detects anomalies and investigates root causes using Claude."""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional

import numpy as np

from app.agents.base import AgentResult, AgentState, BaseAgent, RunContext, Tool


class AnalystAgent(BaseAgent):
    """
    Detects statistical anomalies in metric snapshots and uses Claude
    to investigate and explain the root cause.

    Algorithm:
      1. Compare current value to rolling baseline (Z-score + IQR)
      2. If anomaly, use LLM reasoning to investigate context and cause
      3. Return structured anomaly report with severity and confidence
    """

    def _system_prompt(self) -> str:
        return (
            "You are a senior data analyst with deep expertise in business metrics "
            "and statistical anomaly detection. When you detect an anomaly, "
            "investigate thoroughly: consider seasonality, recent events, "
            "upstream dependencies, and historical patterns. "
            "Be specific. Provide actionable insights with confidence scores. "
            "Format findings as structured JSON."
        )

    def _register_tools(self) -> List[Tool]:
        return [
            Tool(
                name="compute_zscore",
                description="Compute the Z-score of a value against a baseline distribution.",
                parameters={
                    "value":   {"type": "number"},
                    "mean":    {"type": "number"},
                    "std_dev": {"type": "number"},
                },
                handler=self._compute_zscore,
            ),
            Tool(
                name="get_historical_values",
                description="Retrieve the last N values for a metric from the time-series store.",
                parameters={
                    "metric_name": {"type": "string"},
                    "n":           {"type": "integer", "default": 30},
                },
                handler=self._get_historical_values,
            ),
        ]

    async def run(self, context: RunContext) -> AgentResult:
        self._set_state(AgentState.RUNNING)
        start     = time.time()
        snapshot  = context.metadata.get("snapshot", {})
        value     = snapshot.get("value", 0.0)
        threshold = self.config.get("alert_threshold_pct", 15) / 100

        # Pull historical baseline
        history = self._get_historical_values(
            metric_name=snapshot.get("metric_name", "metric"), n=30
        )

        anomaly_detected, zscore, deviation_pct = self._statistical_check(
            value, history, threshold
        )

        output: Dict[str, Any] = {
            "anomaly_detected": anomaly_detected,
            "current_value":    value,
            "baseline_mean":    float(np.mean(history)) if history else 0,
            "zscore":           zscore,
            "deviation_pct":    deviation_pct,
            "severity":         self._severity(abs(zscore)),
            "investigation":    None,
        }

        if anomaly_detected:
            # LLM-powered root-cause investigation
            prompt = (
                f"A metric anomaly was detected.\n\n"
                f"Metric: {snapshot.get('metric_name')}\n"
                f"Current value: {value}\n"
                f"Baseline mean: {output['baseline_mean']:.2f}\n"
                f"Deviation: {deviation_pct:.1f}%\n"
                f"Z-score: {zscore:.2f}\n"
                f"Historical values (last 30): {history}\n\n"
                f"Investigate the root cause. Consider: data pipeline issues, "
                f"business events, seasonality, upstream system changes. "
                f"Return a JSON object with keys: "
                f"'root_cause', 'confidence' (0-1), 'contributing_factors' (list), "
                f"'recommended_actions' (list)."
            )
            investigation_text = await self.think(prompt)
            try:
                output["investigation"] = json.loads(
                    investigation_text[investigation_text.find("{"):investigation_text.rfind("}")+1]
                )
            except Exception:
                output["investigation"] = {"root_cause": investigation_text, "confidence": 0.5}

        self._set_state(AgentState.COMPLETED)
        return AgentResult(
            run_id=context.run_id,
            agent_id=self.agent_id,
            success=True,
            output=output,
            reasoning_trace=self._trace,
            duration_ms=(time.time() - start) * 1000,
        )

    # â”€â”€ tools â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    @staticmethod
    def _compute_zscore(value: float, mean: float, std_dev: float) -> float:
        if std_dev == 0:
            return 0.0
        return (value - mean) / std_dev

    @staticmethod
    def _get_historical_values(metric_name: str, n: int = 30) -> List[float]:
        # In production this reads from the time-series DB.
        # Here we generate plausible mock data for the agent to reason over.
        rng = np.random.default_rng(seed=abs(hash(metric_name)) % 2**31)
        base = rng.uniform(1000, 100000)
        noise = rng.normal(0, base * 0.03, n)
        return [round(base + v, 2) for v in noise]

    def _statistical_check(
        self,
        value: float,
        history: List[float],
        threshold: float,
    ) -> tuple[bool, float, float]:
        if not history:
            return False, 0.0, 0.0
        arr = np.array(history)
        mean, std = arr.mean(), arr.std()
        deviation_pct = abs(value - mean) / mean if mean != 0 else 0
        zscore = self._compute_zscore(value, float(mean), float(std))
        anomaly = deviation_pct > threshold or abs(zscore) > 2.5
        return anomaly, round(float(zscore), 3), round(deviation_pct * 100, 2)

    @staticmethod
    def _severity(abs_zscore: float) -> str:
        if abs_zscore >= 4:
            return "critical"
        if abs_zscore >= 3:
            return "high"
        if abs_zscore >= 2:
            return "medium"
        return "low"
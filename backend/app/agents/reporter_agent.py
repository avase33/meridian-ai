"""ReporterAgent � synthesizes analysis into executive-ready briefings."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Dict, List

from app.agents.base import AgentResult, AgentState, BaseAgent, RunContext, Tool


class ReporterAgent(BaseAgent):
    """
    Takes the anomaly analysis and generates a structured executive briefing:
      - Plain-English summary
      - Impact assessment
      - Root-cause explanation
      - Recommended actions (prioritized)
      - Markdown report for email / Slack delivery
    """

    def _system_prompt(self) -> str:
        return (
            "You are an expert business analyst and executive communicator. "
            "Your job is to translate technical metric anomalies into clear, "
            "concise executive briefings. Write in plain English. "
            "Lead with the business impact, not the technical details. "
            "Use bullet points for clarity. Be direct and actionable. "
            "Prioritize recommendations by urgency."
        )

    def _register_tools(self) -> List[Tool]:
        return []  # Reporter relies on pure LLM synthesis, no external tools

    async def run(self, context: RunContext) -> AgentResult:
        self._set_state(AgentState.RUNNING)
        start    = time.time()
        snapshot = context.metadata.get("snapshot", {})
        analysis = context.metadata.get("analysis", {})
        config   = self.config

        investigation = analysis.get("investigation") or {}
        actions       = investigation.get("recommended_actions", [])
        factors       = investigation.get("contributing_factors", [])
        root_cause    = investigation.get("root_cause", "Under investigation")
        confidence    = investigation.get("confidence", 0.5)

        prompt = f"""
Generate a concise executive briefing for the following business metric anomaly.

=== Anomaly Details ===
Metric:          {snapshot.get('metric_name', config.get('name', 'metric'))}
Severity:        {analysis.get('severity', 'medium').upper()}
Current Value:   {snapshot.get('value')}
Expected Range:  ~{analysis.get('baseline_mean', 'N/A')}
Deviation:       {analysis.get('deviation_pct', 0):.1f}% from baseline
Z-Score:         {analysis.get('zscore', 0):.2f}
Detected At:     {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

=== Root Cause (AI Analysis) ===
{root_cause}
Confidence: {confidence * 100:.0f}%

Contributing Factors: {', '.join(factors) or 'None identified'}

=== Recommended Actions ===
{chr(10).join(f"- {a}" for a in actions) or "- Continue monitoring"}

Write a briefing with these sections:
1. **TL;DR** (1 sentence � the most important thing to know)
2. **What Happened** (2�3 sentences)
3. **Business Impact** (quantified if possible)
4. **Root Cause** (clear explanation)
5. **Immediate Actions** (numbered, prioritized)
6. **Monitoring** (what to watch next)
"""
        briefing_text = await self.think(prompt)

        output = {
            "briefing_markdown": briefing_text,
            "metric_name":       snapshot.get("metric_name"),
            "severity":          analysis.get("severity", "medium"),
            "deviation_pct":     analysis.get("deviation_pct"),
            "zscore":            analysis.get("zscore"),
            "root_cause":        root_cause,
            "actions":           actions,
            "confidence":        confidence,
            "generated_at":      datetime.now(timezone.utc).isoformat(),
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
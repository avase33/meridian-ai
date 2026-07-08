"""Agent Orchestrator — routes tasks to the right agent and manages lifecycle."""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Dict, List, Optional

import structlog

from app.agents.base import AgentResult, AgentState, RunContext
from app.agents.monitor_agent import MonitorAgent
from app.agents.analyst_agent import AnalystAgent
from app.agents.reporter_agent import ReporterAgent
from app.services.llm_service import LLMService

logger = structlog.get_logger(__name__)


class AgentOrchestrator:
    """
    Coordinates multiple agents to handle a full monitoring workflow:

        MonitorAgent  →  AnomalyAgent  →  InvestigatorAgent  →  ReporterAgent
             ↓                ↓                   ↓                    ↓
         raw data       anomaly flag         root cause           executive brief
    """

    def __init__(self, llm_service: LLMService) -> None:
        self._llm      = llm_service
        self._running: Dict[str, asyncio.Task] = {}
        self._results:  Dict[str, AgentResult] = {}

    # ── public API ─────────────────────────────────────────────────────────

    async def run_monitor_pipeline(
        self,
        agent_config: Dict,
        org_id: str,
        trigger: str = "scheduled",
    ) -> AgentResult:
        """
        Execute the full monitoring pipeline for one configured agent.
        Returns the final ReporterAgent result (or an intermediate result on
        early exit if no anomaly is detected).
        """
        ctx = RunContext(org_id=org_id, trigger=trigger, metadata={"config": agent_config})
        start = time.time()
        log   = logger.bind(run_id=ctx.run_id, org_id=org_id)

        # 1. MonitorAgent — fetch current metric value(s)
        log.info("orchestrator.monitor.start")
        monitor = self._make_agent("monitor", agent_config)
        monitor_result = await monitor.run(ctx)

        if not monitor_result.success:
            log.error("orchestrator.monitor.failed", error=monitor_result.error)
            return monitor_result

        metric_snapshot = monitor_result.output

        # 2. AnalystAgent — detect anomaly
        log.info("orchestrator.analyst.start")
        analyst = self._make_agent("analyst", agent_config)
        analyst_ctx = RunContext(
            run_id=ctx.run_id, org_id=org_id, trigger=trigger,
            metadata={**ctx.metadata, "snapshot": metric_snapshot},
        )
        analyst_result = await analyst.run(analyst_ctx)

        if not analyst_result.output.get("anomaly_detected"):
            log.info("orchestrator.no_anomaly")
            return analyst_result  # nothing to report

        # 3. ReporterAgent — synthesize executive briefing
        log.info("orchestrator.reporter.start")
        reporter = self._make_agent("reporter", agent_config)
        reporter_ctx = RunContext(
            run_id=ctx.run_id, org_id=org_id, trigger=trigger,
            metadata={
                **ctx.metadata,
                "snapshot": metric_snapshot,
                "analysis": analyst_result.output,
            },
        )
        report_result = await reporter.run(reporter_ctx)
        report_result.duration_ms = (time.time() - start) * 1000
        log.info("orchestrator.complete", duration_ms=report_result.duration_ms)
        return report_result

    async def run_many(
        self,
        agent_configs: List[Dict],
        org_id: str,
        max_concurrent: int = 5,
    ) -> List[AgentResult]:
        """Run multiple agents concurrently with a semaphore cap."""
        sem = asyncio.Semaphore(max_concurrent)

        async def _guarded(cfg: Dict) -> AgentResult:
            async with sem:
                return await self.run_monitor_pipeline(cfg, org_id)

        return await asyncio.gather(*[_guarded(c) for c in agent_configs])

    # ── private ────────────────────────────────────────────────────────────

    def _make_agent(self, agent_type: str, config: Dict):
        cls_map = {
            "monitor":  MonitorAgent,
            "analyst":  AnalystAgent,
            "reporter": ReporterAgent,
        }
        cls = cls_map.get(agent_type)
        if cls is None:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls(
            agent_id=f"{agent_type}-{id(config)}",
            name=config.get("name", agent_type),
            llm_service=self._llm,
            config=config,
        )
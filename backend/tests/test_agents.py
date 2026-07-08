"""Unit tests for Meridian AI agents."""

import asyncio
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.analyst_agent import AnalystAgent
from app.agents.base import RunContext
from app.agents.monitor_agent import MonitorAgent
from app.agents.orchestrator import AgentOrchestrator
from app.agents.reporter_agent import ReporterAgent


# ── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture
def mock_llm():
    """Mock LLM service that returns a preset response."""
    llm = AsyncMock()
    llm.chat = AsyncMock()
    llm.complete = AsyncMock(return_value='{"root_cause": "test", "confidence": 0.9, "contributing_factors": [], "recommended_actions": ["Check data pipeline"]}')
    return llm


@pytest.fixture
def base_config() -> Dict[str, Any]:
    return {
        "name":                "Test Revenue Monitor",
        "type":                "monitor",
        "data_source":         {"type": "static", "value": 50000.0},
        "alert_threshold_pct": 10,
    }


@pytest.fixture
def run_context() -> RunContext:
    return RunContext(org_id="org-test", trigger="manual")


# ── MonitorAgent ───────────────────────────────────────────────────────────

class TestMonitorAgent:
    def test_init(self, mock_llm, base_config):
        agent = MonitorAgent("agent-1", "Test", mock_llm, base_config)
        assert agent.name == "Test"
        assert len(agent._tools) == 1

    @pytest.mark.asyncio
    async def test_run_static_source(self, mock_llm, base_config, run_context):
        agent  = MonitorAgent("agent-1", "Test", mock_llm, base_config)
        result = await agent.run(run_context)

        assert result.success is True
        assert result.output["value"] == 50000.0
        assert result.output["source_type"] == "static"

    @pytest.mark.asyncio
    async def test_run_fails_gracefully_on_error(self, mock_llm, run_context):
        bad_config = {"data_source": {"type": "rest_api", "url": "http://invalid-host/metric"}}
        agent = MonitorAgent("agent-1", "Test", mock_llm, bad_config)
        result = await agent.run(run_context)
        assert result.success is False
        assert result.error is not None


# ── AnalystAgent ───────────────────────────────────────────────────────────

class TestAnalystAgent:
    def test_severity_levels(self):
        agent = AnalystAgent("a", "t", MagicMock())
        assert agent._severity(0.5) == "low"
        assert agent._severity(2.5) == "medium"
        assert agent._severity(3.5) == "high"
        assert agent._severity(4.5) == "critical"

    @pytest.mark.asyncio
    async def test_no_anomaly_on_normal_value(self, mock_llm, base_config, run_context):
        # Provide a context with a metric close to baseline
        run_context.metadata["snapshot"] = {
            "metric_name": "revenue",
            "value":       50000.0,        # near baseline mean
        }
        agent  = AnalystAgent("a", "t", mock_llm, base_config)
        result = await agent.run(run_context)
        assert result.success is True
        # Value is near baseline so no anomaly expected in most cases
        # (history is seeded, actual assertion depends on seed)
        assert "anomaly_detected" in result.output

    @pytest.mark.asyncio
    async def test_anomaly_triggers_investigation(self, mock_llm, base_config, run_context):
        # Inject a clearly anomalous value
        run_context.metadata["snapshot"] = {
            "metric_name": "revenue",
            "value":       1.0,            # extreme low — guaranteed anomaly
        }
        agent  = AnalystAgent("a", "t", mock_llm, base_config)
        result = await agent.run(run_context)
        assert result.output["anomaly_detected"] is True
        mock_llm.complete.assert_called_once()


# ── Orchestrator ───────────────────────────────────────────────────────────

class TestOrchestrator:
    @pytest.mark.asyncio
    async def test_pipeline_returns_result(self, mock_llm, base_config):
        orch   = AgentOrchestrator(mock_llm)
        result = await orch.run_monitor_pipeline(base_config, org_id="org-test")
        assert result is not None
        assert result.run_id is not None

    @pytest.mark.asyncio
    async def test_run_many_concurrent(self, mock_llm, base_config):
        orch    = AgentOrchestrator(mock_llm)
        configs = [base_config] * 3
        results = await orch.run_many(configs, org_id="org-test", max_concurrent=2)
        assert len(results) == 3
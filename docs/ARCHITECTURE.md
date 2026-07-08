# Meridian AI — Architecture

## Overview

Meridian is built as a **multi-agent system** backed by a production-grade
FastAPI service. Each component is stateless and independently scalable.

## Component Map

```
Client (React)
    │  REST + WebSocket
    ▼
FastAPI Application (uvicorn)
    │  JWT validated on every request
    │  Prometheus metrics exposed at /metrics
    ▼
Agent Orchestrator
    │  Routes tasks based on agent type
    │  Manages concurrency with asyncio Semaphore
    │
    ├──► MonitorAgent    — fetch metric from data source
    ├──► AnalystAgent    — statistical + LLM anomaly detection
    └──► ReporterAgent   — executive briefing generation
                │
                ▼
           LLM Service (Claude API)
                │
                ▼
         anthropic.AsyncAnthropic
```

## Agent Lifecycle

```
IDLE → RUNNING → COMPLETED
                → FAILED
         ↑
     WAITING (tool execution)
```

## Data Flow

```
Data Source (DB / API)
    │
    ▼
MonitorAgent.run()
    │  returns: { value, timestamp, metric_name }
    ▼
AnalystAgent.run()
    │  Z-score + IQR statistical check
    │  If anomaly → Claude chain-of-thought investigation
    │  returns: { anomaly_detected, severity, root_cause, confidence }
    ▼
ReporterAgent.run()       (only if anomaly_detected = true)
    │  Claude synthesis → executive briefing markdown
    │  returns: { briefing_markdown, recommended_actions }
    ▼
Insight saved to PostgreSQL
    │
    ▼
WebSocket push to connected clients
```

## Database Schema

```
organizations ─── 1:N ─── users
      │
      └──── 1:N ─── agents ─── 1:N ─── insights
```

## Scaling

| Component | Horizontal scale strategy |
|---|---|
| FastAPI API | Multiple replicas behind load balancer |
| Celery Workers | Add worker containers (stateless) |
| PostgreSQL | Read replicas for query load |
| Redis | Redis Cluster for queue throughput |
| LLM calls | Anthropic rate limits — use `tenacity` retries |

## Security

- All API endpoints require JWT (OAuth2 Bearer)
- Row-level org isolation (every query scoped to `org_id`)
- Secrets via environment variables (never in code or DB)
- Bcrypt password hashing (passlib)
- Rate limiting via Redis sliding window (middleware)
- TLS termination at load balancer / ingress

## Observability Stack

- **Logs**: structlog → JSON → stdout → aggregator (Datadog / CloudWatch)
- **Metrics**: Prometheus scrape at `/metrics` → Grafana dashboards
- **Traces**: OpenTelemetry SDK → OTLP exporter → Jaeger / Tempo
- **Alerts**: Prometheus AlertManager rules for queue lag, error rates, LLM latency
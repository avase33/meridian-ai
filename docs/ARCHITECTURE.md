# Meridian AI â€” Architecture

## Overview

Meridian is built as a **multi-agent system** backed by a production-grade
FastAPI service. Each component is stateless and independently scalable.

## Component Map

```
Client (React)
    â”‚  REST + WebSocket
    â–¼
FastAPI Application (uvicorn)
    â”‚  JWT validated on every request
    â”‚  Prometheus metrics exposed at /metrics
    â–¼
Agent Orchestrator
    â”‚  Routes tasks based on agent type
    â”‚  Manages concurrency with asyncio Semaphore
    â”‚
    â”œâ”€â”€â–º MonitorAgent    â€” fetch metric from data source
    â”œâ”€â”€â–º AnalystAgent    â€” statistical + LLM anomaly detection
    â””â”€â”€â–º ReporterAgent   â€” executive briefing generation
                â”‚
                â–¼
           LLM Service (Claude API)
                â”‚
                â–¼
         anthropic.AsyncAnthropic
```

## Agent Lifecycle

```
IDLE â†’ RUNNING â†’ COMPLETED
                â†’ FAILED
         â†‘
     WAITING (tool execution)
```

## Data Flow

```
Data Source (DB / API)
    â”‚
    â–¼
MonitorAgent.run()
    â”‚  returns: { value, timestamp, metric_name }
    â–¼
AnalystAgent.run()
    â”‚  Z-score + IQR statistical check
    â”‚  If anomaly â†’ Claude chain-of-thought investigation
    â”‚  returns: { anomaly_detected, severity, root_cause, confidence }
    â–¼
ReporterAgent.run()       (only if anomaly_detected = true)
    â”‚  Claude synthesis â†’ executive briefing markdown
    â”‚  returns: { briefing_markdown, recommended_actions }
    â–¼
Insight saved to PostgreSQL
    â”‚
    â–¼
WebSocket push to connected clients
```

## Database Schema

```
organizations â”€â”€â”€ 1:N â”€â”€â”€ users
      â”‚
      â””â”€â”€â”€â”€ 1:N â”€â”€â”€ agents â”€â”€â”€ 1:N â”€â”€â”€ insights
```

## Scaling

| Component | Horizontal scale strategy |
|---|---|
| FastAPI API | Multiple replicas behind load balancer |
| Celery Workers | Add worker containers (stateless) |
| PostgreSQL | Read replicas for query load |
| Redis | Redis Cluster for queue throughput |
| LLM calls | Anthropic rate limits â€” use `tenacity` retries |

## Security

- All API endpoints require JWT (OAuth2 Bearer)
- Row-level org isolation (every query scoped to `org_id`)
- Secrets via environment variables (never in code or DB)
- Bcrypt password hashing (passlib)
- Rate limiting via Redis sliding window (middleware)
- TLS termination at load balancer / ingress

## Observability Stack

- **Logs**: structlog â†’ JSON â†’ stdout â†’ aggregator (Datadog / CloudWatch)
- **Metrics**: Prometheus scrape at `/metrics` â†’ Grafana dashboards
- **Traces**: OpenTelemetry SDK â†’ OTLP exporter â†’ Jaeger / Tempo
- **Alerts**: Prometheus AlertManager rules for queue lag, error rates, LLM latency
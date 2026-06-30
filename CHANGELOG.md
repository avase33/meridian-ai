# Changelog

All notable changes to Meridian AI are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Planned
- Slack / Teams native integration
- Snowflake + BigQuery connector plugins
- Agent marketplace (publish & share custom agents)
- SOC2 Type II audit package

---

## [1.0.0] â€” 2026-06-30

### Added
- **Multi-agent orchestration** â€” MonitorAgent, AnalystAgent, ReporterAgent with shared LLM service
- **Anomaly detection** â€” Z-score + IQR statistical analysis with configurable sensitivity
- **Root-cause investigation** â€” Autonomous Claude chain-of-thought reasoning per anomaly
- **Executive briefing generator** â€” Structured markdown reports with severity, impact, and recommended actions
- **REST API v1** â€” Full CRUD for agents and insights, JWT authentication, RBAC
- **Multi-tenancy** â€” Organization-scoped data isolation
- **Audit logging** â€” Immutable per-action audit trail
- **WebSocket feed** â€” Real-time insight streaming to dashboard
- **Celery worker** â€” Background agent scheduling and execution
- **pgvector RAG** â€” Historical context retrieval for smarter analysis
- **OpenTelemetry** â€” Distributed tracing for every agent span
- **Docker Compose** â€” Full production stack in one command
- **GitHub Actions CI** â€” Lint, test, security scan on every PR

---

## [0.1.0] â€” 2026-05-01

### Added
- Initial project scaffold
- Proof-of-concept MonitorAgent
- Basic FastAPI skeleton
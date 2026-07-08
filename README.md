<div align="center">

# Meridian AI

**Enterprise Autonomous Business Intelligence Agent Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](docker-compose.yml)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange.svg)](https://anthropic.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **The AI that watches your business 24/7 — so you don't have to.**

[Quick Start](#-quick-start) · [Architecture](#-architecture) · [Features](#-features) · [API Docs](#-api-reference) · [Contributing](#-contributing)

</div>

---

## 🎯 What is Meridian?

Meridian is an **enterprise-grade autonomous AI agent platform** that continuously monitors your
business metrics, detects anomalies in real-time, investigates root causes using a fleet of
specialized AI agents, and delivers executive-ready insights before your team even notices
something is wrong.

**Traditional BI tools are reactive** — you open a dashboard and ask questions.

**Meridian is proactive** — it watches everything, understands context, and tells you what
matters — automatically.

| | Traditional BI | **Meridian** |
|---|---|---|
| Anomaly Detection | Manual threshold alerts | AI-powered contextual detection |
| Root Cause Analysis | You investigate for hours | Autonomous multi-agent investigation |
| Reporting | Manual dashboard creation | Auto-generated executive briefings |
| Response Time | Hours to days | Under 5 minutes |
| Learning | Static rules | Continuously learns from feedback |

---

## ✨ Features

### 🤖 Multi-Agent Architecture
- **MonitorAgent** — Continuously polls data sources (PostgreSQL, REST APIs, webhooks)
- **AnomalyAgent** — Statistical + ML-based deviation detection with Z-score and IQR analysis
- **InvestigatorAgent** — Autonomous root-cause analysis using Claude chain-of-thought reasoning
- **ReporterAgent** — Synthesizes findings into executive-ready briefings with recommendations
- **ActionAgent** — Optional automated responses (PagerDuty alerts, Jira tickets, Slack DMs)

### 🏢 Enterprise Ready
- **Multi-tenant** — Complete data isolation per organization with row-level security
- **RBAC** — Admin, Analyst, Viewer, and fully custom roles
- **Audit Logging** — Immutable trail of every agent decision and API call
- **SSO** — OAuth2 / JWT with SAML 2.0 extension points
- **SOC2-Ready** — Compliance-first design with encryption at rest and in transit
- **High Availability** — Stateless API + Redis queues = horizontal scaling

### 📊 Integrations
- **Databases**: PostgreSQL, MySQL, Snowflake, BigQuery, Redshift
- **APIs**: REST, GraphQL (bring your own connector)
- **Alerting**: PagerDuty, Slack, Microsoft Teams, Email
- **Ticketing**: Jira, Linear, GitHub Issues

### 🔍 Observability
- OpenTelemetry distributed tracing (every agent span tracked)
- Agent decision transparency — see the full reasoning chain per insight
- LLM cost tracking per tenant / per agent / per workflow
- Prometheus metrics endpoint + Grafana dashboard templates

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       Meridian Platform                      │
│                                                              │
│  ┌──────────┐     ┌────────────────────────────────────┐    │
│  │  React   │◄───►│     REST API  /  WebSocket          │    │
│  │Dashboard │     │     (FastAPI + JWT Auth)            │    │
│  └──────────┘     └─────────────────┬──────────────────┘    │
│                                     │                        │
│               ┌─────────────────────▼──────────────┐        │
│               │        Agent Orchestrator           │        │
│               │   (Task routing + State machine)    │        │
│               └──┬──────────┬──────────┬───────────┘        │
│                  │          │          │                     │
│          ┌───────▼──┐ ┌─────▼───┐ ┌───▼──────┐             │
│          │ Monitor  │ │Analyst  │ │ Reporter │             │
│          │  Agent   │ │  Agent  │ │  Agent   │             │
│          └───┬──────┘ └────┬────┘ └────┬─────┘             │
│              └─────────────┼───────────┘                    │
│                     ┌──────▼──────┐                         │
│                     │ LLM Service │                         │
│                     │ (Claude API)│                         │
│                     └─────────────┘                         │
│                                                              │
│  ┌───────────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │  PostgreSQL   │  │  Redis   │  │   pgvector (RAG)     │  │
│  │  (primary DB) │  │ (queues) │  │   knowledge store    │  │
│  └───────────────┘  └──────────┘  └──────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose v2+
- Anthropic API key ([get one here](https://console.anthropic.com))

### 1. Clone & Configure

```bash
git clone https://github.com/avase33/meridian-ai.git
cd meridian-ai
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Start with Docker

```bash
docker-compose up -d
```

| Service | URL |
|---|---|
| API + Swagger Docs | http://localhost:8000/docs |
| Dashboard (React) | http://localhost:3000 |
| Grafana Metrics | http://localhost:3001 |

### 3. Create Your First Agent (Python SDK)

```python
import httpx

client = httpx.Client(base_url="http://localhost:8000/api/v1")

# Authenticate
resp  = client.post("/auth/login", json={"email": "admin@example.com", "password": "changeme"})
token = resp.json()["access_token"]
client.headers["Authorization"] = f"Bearer {token}"

# Create a Monitor Agent that watches daily revenue
agent = client.post("/agents", json={
    "name": "Revenue Monitor",
    "type": "monitor",
    "config": {
        "data_source": {
            "type": "postgresql",
            "dsn": "postgresql://user:pass@db/analytics"
        },
        "query": "SELECT SUM(revenue) AS total FROM sales WHERE date = CURRENT_DATE",
        "schedule": "*/15 * * * *",   # every 15 minutes
        "alert_threshold_pct": 15     # alert on >15% deviation from rolling avg
    }
}).json()

print(f"Agent created: {agent['id']}")
# Meridian will now autonomously watch revenue and alert you if it drops.
```

---

## 📦 Project Structure

```
meridian-ai/
├── backend/
│   ├── app/
│   │   ├── agents/              # AI agent implementations
│   │   │   ├── base.py          # Abstract BaseAgent + Tool definitions
│   │   │   ├── orchestrator.py  # Multi-agent task coordinator
│   │   │   ├── monitor_agent.py # Data polling & scheduling
│   │   │   ├── analyst_agent.py # Anomaly detection & investigation
│   │   │   └── reporter_agent.py# Executive report generation
│   │   ├── api/v1/              # Versioned REST API
│   │   │   ├── agents.py        # Agent CRUD + trigger endpoints
│   │   │   ├── insights.py      # Insight feed + feedback
│   │   │   └── auth.py          # JWT auth endpoints
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── services/            # LLM, scheduler, vector store
│   │   ├── config.py            # Pydantic settings
│   │   ├── database.py          # Async DB sessions
│   │   └── main.py              # FastAPI app entry point
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                    # React + TypeScript dashboard
│   └── src/
│       ├── App.tsx
│       └── pages/Dashboard.tsx
├── docs/
│   └── ARCHITECTURE.md
├── docker-compose.yml
└── .env.example
```

---

## ⚙️ Configuration

| Variable | Description | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API key | ✅ |
| `DATABASE_URL` | PostgreSQL DSN | ✅ |
| `REDIS_URL` | Redis DSN | ✅ |
| `SECRET_KEY` | JWT signing secret (32+ chars) | ✅ |
| `LLM_MODEL` | Claude model (`claude-opus-4-8`) | Optional |
| `MAX_AGENTS_PER_ORG` | Hard cap per tenant | Optional |
| `ALLOWED_ORIGINS` | CORS origins | Optional |

---

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
# Development setup
cd backend && pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Tests
pytest tests/ -v --cov=app --cov-report=term-missing

# Lint
ruff check . && black --check .
```

---

## 📜 License

MIT © [avase33](https://github.com/avase33)

<div align="center">
  <br/>
  <strong>Built with Claude AI · FastAPI · React · PostgreSQL</strong>
  <br/>
  <a href="https://github.com/avase33/meridian-ai/stargazers">⭐ Star this repo</a> if Meridian helps you!
</div>

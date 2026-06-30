<div align="center">

# ðŸŒ Meridian AI

**Enterprise Autonomous Business Intelligence Agent Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED.svg)](docker-compose.yml)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange.svg)](https://anthropic.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **The AI that watches your business 24/7 â€” so you don't have to.**

[Quick Start](#-quick-start) Â· [Architecture](#-architecture) Â· [Features](#-features) Â· [API Docs](#-api-reference) Â· [Contributing](#-contributing)

</div>

---

## ðŸŽ¯ What is Meridian?

Meridian is an **enterprise-grade autonomous AI agent platform** that continuously monitors your
business metrics, detects anomalies in real-time, investigates root causes using a fleet of
specialized AI agents, and delivers executive-ready insights before your team even notices
something is wrong.

**Traditional BI tools are reactive** â€” you open a dashboard and ask questions.

**Meridian is proactive** â€” it watches everything, understands context, and tells you what
matters â€” automatically.

| | Traditional BI | **Meridian** |
|---|---|---|
| Anomaly Detection | Manual threshold alerts | AI-powered contextual detection |
| Root Cause Analysis | You investigate for hours | Autonomous multi-agent investigation |
| Reporting | Manual dashboard creation | Auto-generated executive briefings |
| Response Time | Hours to days | Under 5 minutes |
| Learning | Static rules | Continuously learns from feedback |

---

## âœ¨ Features

### ðŸ¤– Multi-Agent Architecture
- **MonitorAgent** â€” Continuously polls data sources (PostgreSQL, REST APIs, webhooks)
- **AnomalyAgent** â€” Statistical + ML-based deviation detection with Z-score and IQR analysis
- **InvestigatorAgent** â€” Autonomous root-cause analysis using Claude chain-of-thought reasoning
- **ReporterAgent** â€” Synthesizes findings into executive-ready briefings with recommendations
- **ActionAgent** â€” Optional automated responses (PagerDuty alerts, Jira tickets, Slack DMs)

### ðŸ¢ Enterprise Ready
- **Multi-tenant** â€” Complete data isolation per organization with row-level security
- **RBAC** â€” Admin, Analyst, Viewer, and fully custom roles
- **Audit Logging** â€” Immutable trail of every agent decision and API call
- **SSO** â€” OAuth2 / JWT with SAML 2.0 extension points
- **SOC2-Ready** â€” Compliance-first design with encryption at rest and in transit
- **High Availability** â€” Stateless API + Redis queues = horizontal scaling

### ðŸ“Š Integrations
- **Databases**: PostgreSQL, MySQL, Snowflake, BigQuery, Redshift
- **APIs**: REST, GraphQL (bring your own connector)
- **Alerting**: PagerDuty, Slack, Microsoft Teams, Email
- **Ticketing**: Jira, Linear, GitHub Issues

### ðŸ” Observability
- OpenTelemetry distributed tracing (every agent span tracked)
- Agent decision transparency â€” see the full reasoning chain per insight
- LLM cost tracking per tenant / per agent / per workflow
- Prometheus metrics endpoint + Grafana dashboard templates

---

## ðŸ— Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                       Meridian Platform                      â”‚
â”‚                                                              â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”     â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”‚
â”‚  â”‚  React   â”‚â—„â”€â”€â”€â–ºâ”‚     REST API  /  WebSocket          â”‚    â”‚
â”‚  â”‚Dashboard â”‚     â”‚     (FastAPI + JWT Auth)            â”‚    â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â”‚
â”‚                                     â”‚                        â”‚
â”‚               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”        â”‚
â”‚               â”‚        Agent Orchestrator           â”‚        â”‚
â”‚               â”‚   (Task routing + State machine)    â”‚        â”‚
â”‚               â””â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜        â”‚
â”‚                  â”‚          â”‚          â”‚                     â”‚
â”‚          â”Œâ”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â” â”Œâ”€â”€â”€â”€â”€â–¼â”€â”€â”€â” â”Œâ”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”             â”‚
â”‚          â”‚ Monitor  â”‚ â”‚Analyst  â”‚ â”‚ Reporter â”‚             â”‚
â”‚          â”‚  Agent   â”‚ â”‚  Agent  â”‚ â”‚  Agent   â”‚             â”‚
â”‚          â””â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜             â”‚
â”‚              â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                    â”‚
â”‚                     â”Œâ”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”                         â”‚
â”‚                     â”‚ LLM Service â”‚                         â”‚
â”‚                     â”‚ (Claude API)â”‚                         â”‚
â”‚                     â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                         â”‚
â”‚                                                              â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚  PostgreSQL   â”‚  â”‚  Redis   â”‚  â”‚   pgvector (RAG)     â”‚  â”‚
â”‚  â”‚  (primary DB) â”‚  â”‚ (queues) â”‚  â”‚   knowledge store    â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸš€ Quick Start

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

## ðŸ“¦ Project Structure

```
meridian-ai/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ agents/              # AI agent implementations
â”‚   â”‚   â”‚   â”œâ”€â”€ base.py          # Abstract BaseAgent + Tool definitions
â”‚   â”‚   â”‚   â”œâ”€â”€ orchestrator.py  # Multi-agent task coordinator
â”‚   â”‚   â”‚   â”œâ”€â”€ monitor_agent.py # Data polling & scheduling
â”‚   â”‚   â”‚   â”œâ”€â”€ analyst_agent.py # Anomaly detection & investigation
â”‚   â”‚   â”‚   â””â”€â”€ reporter_agent.py# Executive report generation
â”‚   â”‚   â”œâ”€â”€ api/v1/              # Versioned REST API
â”‚   â”‚   â”‚   â”œâ”€â”€ agents.py        # Agent CRUD + trigger endpoints
â”‚   â”‚   â”‚   â”œâ”€â”€ insights.py      # Insight feed + feedback
â”‚   â”‚   â”‚   â””â”€â”€ auth.py          # JWT auth endpoints
â”‚   â”‚   â”œâ”€â”€ models/              # SQLAlchemy ORM models
â”‚   â”‚   â”œâ”€â”€ services/            # LLM, scheduler, vector store
â”‚   â”‚   â”œâ”€â”€ config.py            # Pydantic settings
â”‚   â”‚   â”œâ”€â”€ database.py          # Async DB sessions
â”‚   â”‚   â””â”€â”€ main.py              # FastAPI app entry point
â”‚   â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ Dockerfile
â”‚   â””â”€â”€ requirements.txt
â”œâ”€â”€ frontend/                    # React + TypeScript dashboard
â”‚   â””â”€â”€ src/
â”‚       â”œâ”€â”€ App.tsx
â”‚       â””â”€â”€ pages/Dashboard.tsx
â”œâ”€â”€ docs/
â”‚   â””â”€â”€ ARCHITECTURE.md
â”œâ”€â”€ docker-compose.yml
â””â”€â”€ .env.example
```

---

## âš™ï¸ Configuration

| Variable | Description | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API key | âœ… |
| `DATABASE_URL` | PostgreSQL DSN | âœ… |
| `REDIS_URL` | Redis DSN | âœ… |
| `SECRET_KEY` | JWT signing secret (32+ chars) | âœ… |
| `LLM_MODEL` | Claude model (`claude-opus-4-8`) | Optional |
| `MAX_AGENTS_PER_ORG` | Hard cap per tenant | Optional |
| `ALLOWED_ORIGINS` | CORS origins | Optional |

---

## ðŸ¤ Contributing

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

## ðŸ“œ License

MIT Â© [avase33](https://github.com/avase33)

<div align="center">
  <br/>
  <strong>Built with Claude AI Â· FastAPI Â· React Â· PostgreSQL</strong>
  <br/>
  <a href="https://github.com/avase33/meridian-ai/stargazers">â­ Star this repo</a> if Meridian helps you!
</div>
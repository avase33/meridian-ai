<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=00D9FF&center=true&vCenter=true&width=600&lines=Meridian+AI;Enterprise+Autonomous+BI+Agent" alt="Meridian AI" />

<br/>

[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Claude AI](https://img.shields.io/badge/Claude_AI-Powered-D97706?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](docker-compose.yml)

<br/>

> ### **The AI that watches your business 24/7 â€” so you don't have to.**
>
> *Autonomous anomaly detection + root-cause analysis + executive briefings, all on autopilot.*

<br/>

[**Quick Start**](#-quick-start) &nbsp;|&nbsp; [**Architecture**](#-architecture) &nbsp;|&nbsp; [**Features**](#-features) &nbsp;|&nbsp; [**API**](#-api-reference) &nbsp;|&nbsp; [**Contributing**](#-contributing)

</div>

---

## ðŸŽ¯ The Problem Meridian Solves

Traditional BI is **reactive**. You open a dashboard. You ask questions. You find problems â€” after they've hurt you.

**Meridian is proactive.** It monitors everything, reasons about context, and delivers answers before your team even knows to ask.

<br/>

<div align="center">

| | Traditional BI | **Meridian AI** |
|:---|:---:|:---:|
| **Anomaly Detection** | Manual thresholds | AI-contextual detection |
| **Root Cause Analysis** | You investigate for hours | Autonomous agent investigation |
| **Reporting** | Manual dashboards | Auto-generated executive briefings |
| **Response Time** | Hours to days | **< 5 minutes** |
| **Learns Over Time** | Static rules | Continuous feedback loop |

</div>

---

## Architecture

```mermaid
flowchart TD
    User["User Dashboard\n(React + TypeScript)"]
    API["FastAPI Backend\nJWT Auth / REST / WebSocket"]
    Orch["Agent Orchestrator\nTask Routing + State Machine"]

    Monitor["Monitor Agent\nPolls data sources\nevery N minutes"]
    Analyst["Analyst Agent\nZ-score + IQR + Claude\nroot-cause reasoning"]
    Reporter["Reporter Agent\nExec briefings via\nClaude claude-opus-4-8"]

    LLM["LLM Service\nAnthropic Claude API\ntool-use agentic loop"]
    DB["PostgreSQL\n+ pgvector (RAG)"]
    Cache["Redis\nCelery task queue"]
    Obs["Observability\nPrometheus + Grafana\nOpenTelemetry"]

    User <-->|"HTTPS / WS"| API
    API --> Orch
    Orch --> Monitor
    Orch --> Analyst
    Orch --> Reporter
    Monitor & Analyst & Reporter <-->|"tool-use loop"| LLM
    Monitor & Analyst & Reporter <--> DB
    Orch <--> Cache
    API --> Obs

    style User fill:#1e40af,color:#fff,stroke:#3b82f6
    style API fill:#065f46,color:#fff,stroke:#10b981
    style Orch fill:#7c3aed,color:#fff,stroke:#a78bfa
    style Monitor fill:#0f766e,color:#fff,stroke:#2dd4bf
    style Analyst fill:#0f766e,color:#fff,stroke:#2dd4bf
    style Reporter fill:#0f766e,color:#fff,stroke:#2dd4bf
    style LLM fill:#92400e,color:#fff,stroke:#f59e0b
    style DB fill:#1e3a5f,color:#fff,stroke:#60a5fa
    style Cache fill:#7f1d1d,color:#fff,stroke:#f87171
    style Obs fill:#374151,color:#fff,stroke:#9ca3af
```

---

## Tech Stack

<div align="center">

### Backend
[![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.0-red?style=flat-square&logo=sqlalchemy&logoColor=white)](https://sqlalchemy.org)
[![Celery](https://img.shields.io/badge/Celery-37814A?style=flat-square&logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![Pydantic](https://img.shields.io/badge/Pydantic_v2-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)

### AI & Data
[![Anthropic](https://img.shields.io/badge/Anthropic_Claude-D97706?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![pgvector](https://img.shields.io/badge/pgvector_RAG-336791?style=flat-square&logo=postgresql&logoColor=white)](https://github.com/pgvector/pgvector)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-425CC7?style=flat-square&logo=opentelemetry&logoColor=white)](https://opentelemetry.io)

### Frontend & Infrastructure
[![React](https://img.shields.io/badge/React_18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-336791?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](docker-compose.yml)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white)](https://grafana.com)

</div>

---

## Features

### Multi-Agent AI Pipeline

```
Data Source --> [Monitor Agent] --> [Analyst Agent] --> [Reporter Agent] --> Executive Briefing
                  Polls every         Z-score + IQR         Claude opus          Delivered in
                  15 minutes          + Claude RCA           synthesis            < 5 minutes
```

| Agent | Role | AI Capability |
|:---|:---|:---|
| **MonitorAgent** | Polls PostgreSQL, REST APIs, webhooks on schedule | Autonomous scheduling with Celery |
| **AnalystAgent** | Detects anomalies statistically then investigates with Claude | Z-score, IQR, + chain-of-thought RCA |
| **ReporterAgent** | Generates C-suite-ready briefings | Full Claude `claude-opus-4-8` synthesis |
| **Orchestrator** | Routes tasks, manages agent state machine | Priority queue + retry logic |

### Enterprise Features

| Category | Capabilities |
|:---|:---|
| **Security** | JWT/OAuth2, RBAC (Admin/Analyst/Viewer), row-level multi-tenancy |
| **Compliance** | Immutable audit log, encryption at rest + in transit, SOC2-ready |
| **Observability** | OpenTelemetry spans per agent, LLM cost tracking, Prometheus + Grafana |
| **Integrations** | PostgreSQL, Snowflake, BigQuery, Redshift, REST, Slack, PagerDuty, Jira |
| **Scalability** | Stateless API + Redis Celery = horizontal scale, Docker Compose or K8s |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose v2+
- [Anthropic API key](https://console.anthropic.com)

### 1. Clone & Configure

```bash
git clone https://github.com/avase33/meridian-ai.git
cd meridian-ai
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### 2. Start All Services

```bash
docker-compose up -d
```

| Service | URL |
|:---|:---|
| **API + Swagger Docs** | http://localhost:8000/docs |
| **React Dashboard** | http://localhost:3000 |
| **Grafana Metrics** | http://localhost:3001 |

### 3. Create Your First Monitoring Agent

```python
import httpx

client = httpx.Client(base_url="http://localhost:8000/api/v1")

# Authenticate
token = client.post("/auth/login", json={
    "email": "admin@example.com",
    "password": "changeme"
}).json()["access_token"]

client.headers["Authorization"] = f"Bearer {token}"

# Deploy a Revenue Monitor agent
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
        "alert_threshold_pct": 15      # alert on >15% deviation
    }
}).json()

print(f"Agent deployed: {agent['id']}")
# Meridian now autonomously monitors revenue and alerts you on drops.
```

---

## API Reference

<details>
<summary><strong>Authentication</strong></summary>

```http
POST /api/v1/auth/login
Content-Type: application/json

{ "email": "admin@company.com", "password": "..." }
```

Returns `{ "access_token": "eyJ...", "token_type": "bearer" }`

</details>

<details>
<summary><strong>Agent Management</strong></summary>

```http
GET    /api/v1/agents           # List all agents
POST   /api/v1/agents           # Create agent
GET    /api/v1/agents/{id}      # Get agent details
PUT    /api/v1/agents/{id}      # Update agent config
DELETE /api/v1/agents/{id}      # Delete agent
POST   /api/v1/agents/{id}/run  # Trigger immediate run
```

</details>

<details>
<summary><strong>Insights Feed</strong></summary>

```http
GET  /api/v1/insights              # Get insight feed (paginated)
GET  /api/v1/insights/{id}         # Get single insight + reasoning chain
POST /api/v1/insights/{id}/feedback # Submit thumbs up/down feedback
```

</details>

---

## Project Structure

```
meridian-ai/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ app/
â”‚   â”‚   â”œâ”€â”€ agents/
â”‚   â”‚   â”‚   â”œâ”€â”€ base.py           # Abstract BaseAgent + Claude tool-use loop
â”‚   â”‚   â”‚   â”œâ”€â”€ orchestrator.py   # Multi-agent pipeline coordinator
â”‚   â”‚   â”‚   â”œâ”€â”€ monitor_agent.py  # Data polling + Celery scheduling
â”‚   â”‚   â”‚   â”œâ”€â”€ analyst_agent.py  # Statistical detection + LLM root-cause
â”‚   â”‚   â”‚   â””â”€â”€ reporter_agent.py # Executive briefing via Claude
â”‚   â”‚   â”œâ”€â”€ api/v1/
â”‚   â”‚   â”‚   â”œâ”€â”€ auth.py           # JWT login endpoint
â”‚   â”‚   â”‚   â”œâ”€â”€ agents.py         # Agent CRUD + trigger
â”‚   â”‚   â”‚   â””â”€â”€ insights.py       # Insight feed + feedback
â”‚   â”‚   â”œâ”€â”€ models/               # SQLAlchemy ORM (User, Agent, Insight)
â”‚   â”‚   â”œâ”€â”€ services/
â”‚   â”‚   â”‚   â””â”€â”€ llm_service.py    # Anthropic async wrapper + cost tracking
â”‚   â”‚   â”œâ”€â”€ config.py             # Pydantic Settings
â”‚   â”‚   â”œâ”€â”€ database.py           # Async SQLAlchemy sessions
â”‚   â”‚   â””â”€â”€ main.py               # FastAPI entry point
â”‚   â”œâ”€â”€ tests/
â”‚   â”‚   â””â”€â”€ test_agents.py        # Pytest unit tests with mocking
â”‚   â”œâ”€â”€ Dockerfile
â”‚   â””â”€â”€ requirements.txt
â”œâ”€â”€ frontend/
â”‚   â””â”€â”€ src/
â”‚       â”œâ”€â”€ App.tsx               # React Router setup
â”‚       â””â”€â”€ pages/Dashboard.tsx   # Stats cards + LineChart + Insight feed
â”œâ”€â”€ docs/
â”‚   â””â”€â”€ ARCHITECTURE.md
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/ci.yml          # Lint + Test + Security + Docker build
â”œâ”€â”€ docker-compose.yml            # Full stack: API + Worker + PG + Redis + Grafana
â””â”€â”€ .env.example
```

---

## Configuration

| Variable | Description | Required |
|:---|:---|:---:|
| `ANTHROPIC_API_KEY` | Claude API key | **Yes** |
| `DATABASE_URL` | PostgreSQL DSN | **Yes** |
| `REDIS_URL` | Redis DSN | **Yes** |
| `SECRET_KEY` | JWT signing secret (32+ chars) | **Yes** |
| `LLM_MODEL` | Claude model (default: `claude-opus-4-8`) | No |
| `MAX_AGENTS_PER_ORG` | Per-tenant agent cap | No |
| `ALLOWED_ORIGINS` | CORS allowed origins | No |

---

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v --cov=app --cov-report=term-missing

# Lint
ruff check . && black --check .
```

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)

---

## License

MIT (c) [avase33](https://github.com/avase33) - see [LICENSE](LICENSE)

---

<div align="center">

[â­ Star this repo](https://github.com/avase33/meridian-ai/stargazers) if Meridian helps you!

</div>
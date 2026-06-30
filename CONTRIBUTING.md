# Contributing to Meridian AI

Thank you for your interest in contributing! This document explains how.

## Development Setup

```bash
git clone https://github.com/avase33/meridian-ai.git
cd meridian-ai

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## Coding Standards

- **Python**: Black formatting, Ruff linting, type annotations on all public functions
- **TypeScript**: ESLint + Prettier, strict mode enabled
- **Tests**: minimum 80% coverage on new code (`pytest --cov=app`)
- **Commits**: Conventional Commits format (`feat:`, `fix:`, `docs:`, `chore:`)

## Pull Request Process

1. Fork and create a feature branch from `main`
2. Write tests for your changes
3. Ensure `pytest tests/ -v` passes locally
4. Ensure `ruff check . && black --check .` passes
5. Update CHANGELOG.md under `[Unreleased]`
6. Open a PR with a clear description of the change and why

## Agent Development

To add a new agent type:

1. Create `backend/app/agents/your_agent.py` inheriting from `BaseAgent`
2. Implement `run(context)` and `_register_tools()`
3. Register in `AgentType` enum in `models/agent.py`
4. Add the agent to `Orchestrator._agent_factory()`
5. Write tests in `tests/test_agents.py`

## Questions?

Open a GitHub Discussion or file an issue with the `question` label.
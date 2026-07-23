# OpenSchoolOS

An Educational Operating System that helps teachers make better educational
decisions through evidence-guided reasoning.

This is NOT a school management system.

## Sprint 001 — Repository Layout

```
OpenSchoolOS/
├── apps/
│   ├── web/            # Educational Case Notebook front end (Next.js)
│   └── api/            # Backend serving the educational domain (FastAPI)
├── packages/
│   ├── domain/         # Shared, framework-free domain model
│   ├── shared/         # Cross-cutting types and utilities
│   └── ui/             # Shared React components (shadcn/ui + Tailwind)
├── knowledge/          # Curated educational knowledge (LDG subject graphs)
├── .ai/                # Constitutional brain — read before code
├── docs/               # User and developer documentation
└── docker/             # Container definitions (Docker Compose)
```

## Authority

Every AI agent MUST begin in `.ai/README.md` before writing code. The order of
authority is:

`README → constitution → philosophy → educational-principles → domain →
architecture → coding-rules → implementation`

## First Build Target

Sprint 001 builds the **Educational Case Notebook** — a single linear workflow:

```
Student → Create Learning Case → Record Observation →
Identify Root Gap → Choose Intervention → Review → Close Case
```

In `apps/web` this is exactly **three pages**:

1. **Students** — search, click, done.
2. **Learning Cases** — every active struggle (not report cards, not marks).
3. **New Observation** — five fields only: Observed, Possible Root Gap,
   Evidence, Strategy, Next Review.

No dashboard. No analytics. No AI. No recommendation engine. One teacher, one
learner, one better decision. You are the recommendation engine.

What we are actually validating is the **Educational Loop** (see
`.ai/educational-loop.md`): Observe → Think → Act → Reflect → Observe Again.
The software only records and supports this loop; the teacher runs it.

## GitHub Goal

Not stars. Not forks.

We want someone to visit this repository and say:

> "This teacher deeply understands learning."

Every file in this repo — code, docs, and `.ai/` — should earn that reaction.
If a visitor cannot tell we understand learning, we have failed, regardless of
metrics.

## For AI Agents (Kilo Code)

Read `FOUNDERS_AI_OPERATING_MANUAL.md` first. It turns Kilo Code into a senior
engineer on the team — bound by `.ai/constitution.md` — not an autocomplete
tool. The `.ai/` directory is the constitutional brain; start in
`.ai/README.md`.

The AI engineering team operates from the **Engineering Playbook**
(`.ai/playbook.md`): identified prompts (A00–A90), reusable workflows
(`.ai/workflows/`), an identical session start (`.ai/session-start.md`),
recorded decisions (`.ai/decision-log.md`), and one disciplined pipeline every
feature passes through. This is tool-agnostic — it works the same regardless of
which coding assistant you use.

## Running the Project

### Prerequisites

- **Docker** (recommended): Docker Engine + Docker Compose v2+.
  _or_
- **Host**: Node.js 20+ (with `pnpm`), Python 3.13+ (with `pip` or `uv`), PostgreSQL 17 running on `localhost:5432`.

### Option A — Docker Compose (recommended)

```bash
cp .env.example .env   # optional: override DATABASE_URL or NEXT_PUBLIC_API_URL
./scripts/dev.sh
# → Web:  http://localhost:3000
# → API:  http://localhost:8000/docs
```

Source is mounted; changes reload automatically. Postgres data persists in the
`pgdata` volume.

### Option B — Host (no Docker)

```bash
cp .env.example .env   # adjust DATABASE_URL if your Postgres differs

# Start Postgres (macOS example)
brew services start postgresql@17

# Install API deps and start API with live reload
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000

# In another terminal, start the web
pnpm --filter @openschoolos/web dev
# → Web:  http://localhost:3000
# → API:  http://localhost:8000/docs
```

A helper script for the host path also exists: `./scripts/dev-local.sh` (starts
Postgres, creates the venv, and runs both services in the foreground).

### Stopping

- **Docker:** `Ctrl+C` in the terminal running `./scripts/dev.sh`, then `docker compose down`.
- **Host:** `Ctrl+C` in each terminal. To reset Postgres data (Docker only): `docker compose down -v`.

### Tests

```bash
pnpm test                           # web (Vitest) + domain (Vitest)
cd apps/api && pytest tests/test_api.py  # API (requires installed dev deps)
```

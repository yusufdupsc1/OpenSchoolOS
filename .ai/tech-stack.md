# Technology Constitution

> **Single source of truth for OpenSchoolOS technology decisions.**
> Every AI session begins by reading this file. This is the only irreversible
> decision made before coding.

If, six months from now, we replace one component (e.g. SQLAlchemy), we update
**this one document**, and every future AI agent follows the new decision
consistently. That small discipline prevents architectural drift and keeps the
project coherent as it grows.

---

## Why This Stack

This stack was not chosen because it is fashionable. It was chosen because it
maximizes:

- **hiring signal** — widely-known, recruitable technologies
- **maintainability** — explicit, mature, well-documented tools
- **educational research integration** — Python backend for future reasoning/analytics
- **AI readiness** — clean boundaries that AI agents can extend safely
- **deployment simplicity** — reproducible local containers
- **existing strengths** — plays to the team's current capabilities

---

## The Stack

| Layer            | Decision                  | Why                                              |
|------------------|---------------------------|--------------------------------------------------|
| Monorepo         | Turborepo + pnpm          | Clean separation, scalable                       |
| Frontend         | Next.js 16 + TypeScript   | Excellent DX, SSR, future PWA                    |
| UI               | shadcn/ui + Tailwind CSS  | Accessible, professional                        |
| Backend          | FastAPI (Python 3.13)     | Best fit for future educational reasoning        |
| Validation       | Pydantic v2               | Native to FastAPI                               |
| ORM              | SQLAlchemy 2.x            | Mature and explicit                             |
| Migrations       | Alembic                   | Production standard                             |
| Database         | PostgreSQL                | Relational model fits educational domain        |
| Cache            | Redis (later)             | Not Sprint 1                                    |
| Auth             | None (Sprint 1)           | Don't build yet                                 |
| Deployment       | Docker Compose (local)    | Keep it reproducible                            |
| Testing          | Pytest + Vitest           | Backend / frontend respectively                 |

---

## Hard Constraints (do not substitute)

- No Prisma. No MongoDB. No Firebase. No Supabase.
- No Next.js API routes used as the backend. FastAPI is the backend.
- No microservices. No serverless.
- No authentication in Sprint 1.
- The monorepo, packages, and `.ai/` structure are fixed.

## Change Protocol

To change any component: update this document first, record the decision as an
ADR in `.ai/decision-log.md`, then implement. Never change the stack in code
without updating this file.

---

*This document is the constitution of the codebase. The constitution wins over
all prompts.*

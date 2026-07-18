# Architecture

> High-level technical architecture for OpenSchoolOS. This is a living document;
> refine it as the system takes shape. It must always obey the
> [Constitution](./constitution.md) and the root authority in
> [README.md](./README.md).

## Goals

- Run on modest, school-owned hardware (single node today, small cluster later).
- Deploy as one cohesive unit — no fragile multi-service orchestration for the
  common case.
- Self-hostable: data lives in the project's PostgreSQL instance (Docker Compose
  locally), never required to leave the school's infrastructure or a vendor
  cloud.

## Repository Shape (Sprint 001)

```
OpenSchoolOS/
├── apps/
│   ├── web/     # Teacher-facing Educational Case Notebook (front end)
│   └── api/     # Backend serving the educational domain (FastAPI)
├── packages/
│   └── domain/  # Shared educational domain model (pure, framework-free)
├── knowledge/   # Curated educational knowledge (e.g. LDG subject graphs)
├── .ai/         # Constitutional brain — read before code
└── docs/        # User and developer documentation
```

- **packages/domain** is the single source of truth for domain types. Sprint
  001 models exactly three aggregates: **Student**, **LearningCase**,
  **Observation** (see domain.md). The Learning Dependency Graph (ldg.md) is a
  reference structure used to identify the root gap, not an aggregate. Pure
  domain, no framework dependency, no business logic in the UI.
- **apps/api** serves the domain and persists state to PostgreSQL (Docker
  Compose locally) with full export and full deletion.
- **apps/web** is the Educational Case Notebook — the only screen Sprint 001
  builds.

## First Build Target: Educational Case Notebook

The workflow the Notebook supports:

```
Student
  ↓
Create Learning Case
  ↓
Record Observation
  ↓
Identify Root Gap   (using the Learning Dependency Graph — see ldg.md)
  ↓
Choose Strategy (intervention — part of the LearningCase, not a separate model)
  ↓
Review
  ↓
Close Case
```

In `apps/web` this is exactly **three pages**:

1. **Students** — search, click, done.
2. **Learning Cases** — every active struggle (not report cards, not marks).
3. **New Observation** — five fields only: Observed, Possible Root Gap,
   Evidence, Strategy, Next Review.

Explicitly not built: no dashboard, no analytics, no AI, no recommendation
engine. See [anti-patterns.md](./anti-patterns.md) and
[constraints.md](./constraints.md).

What we are actually validating is the **Educational Loop**
([educational-loop.md](./educational-loop.md)): Observe → Think → Act →
Reflect → Observe Again. The software only records and supports this loop; the
teacher runs it.

No dashboard. No analytics. No AI guessing. One teacher, one learner, one
better decision. See [constitution.md](./constitution.md) Definition of Done.

## Boundaries

```
┌─────────────────────────────────────────────┐
│                 OpenSchoolOS                │
│                                             │
│   ┌──────────────┐      ┌────────────────┐  │
│   │  apps/web    │ ───▶ │   apps/api     │  │
│   │  (Notebook)  │      │  (domain API)  │  │
│   └──────────────┘      └───────┬────────┘  │
│                                 │          │
│                    ┌────────────┴─────────┐ │
│                    │   packages/domain    │ │
│                    └────────────┬─────────┘ │
│                                 │          │
│                 ┌───────────────┴──────────┐│
│                 │  PostgreSQL (Docker)     │ │
│                 │  (export / delete)      │ │
│                 └─────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Data Flow

1. A teacher opens the Notebook in `apps/web`.
2. Actions call `apps/api`, which validates against `packages/domain`.
3. All state persists to PostgreSQL (Docker Compose locally).
4. Export/delete operations act on the datastore as a whole.

## Data Model (v0)

Exactly three tables: `students`, `learning_cases`, `observations`
(see [data-model.md](./data-model.md)). No other tables for v0. Interventions
are a column on `learning_cases`, not a separate table. The Learning Dependency
Graph is not stored as a table.

## Failure Modes

- **Hardware dies:** restore from backup; the system must be restorable by a
  non-expert following a written runbook.
- **Update fails:** roll back to the previous version automatically; never
  leave the school with a broken install.
- **API or web fails:** the other tier keeps running; the Notebook degrades
  gracefully without losing teacher reasoning.

## To Refine

- Concrete stack choices (see [coding-rules](./coding-rules.md)).
- Backup/restore format and cadence for PostgreSQL.
- Identity & access model for multi-teacher schools.
- Cluster mode for multi-campus schools.

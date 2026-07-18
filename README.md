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

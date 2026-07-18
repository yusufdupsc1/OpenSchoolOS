# Session Start

Every day. Every AI. Every session starts here.

Read this file first. Then read `.ai/prompts/A00-System.md` to adopt the
operating personality. Then follow the AI Development Pipeline
(`.ai/development-pipeline.md`).

---

## Today's Goal

Build and validate the smallest honest slice that helps one teacher make one
better decision for one learner. For Sprint 001 that means the Educational Case
Notebook (three aggregates, three tables, three pages) on the FastAPI /
PostgreSQL stack — not yet implemented; the skeleton is in place.

## Current Sprint

Sprint 001 — Educational Case Notebook.

```
Student → Create Learning Case → Record Observation →
Identify Root Gap → Choose Intervention → Review → Close Case
```

Three pages in apps/web: Students (search/click), Learning Cases (active
struggles), New Observation (five fields). No dashboard, no analytics, no AI, no
recommendation engine.

## Current Research Question

After a teacher uses the Notebook for a week: "What did using this for a week
teach us?" If "nothing" → change the design. If "it changed how I think about
students" → we've found something worth expanding.

## Current Domain Model

Three aggregates only (see `.ai/domain.md`, `packages/domain/src/types.ts`):

- **Student** — a child; search/click entry point.
- **LearningCase** — one active struggle; holds possible root gap, evidence,
  strategy (intervention is part of the case, not separate), next review, status.
- **Observation** — one recorded moment: observed, possible root gap, evidence,
  strategy, next review.

Persisted as three tables: `students`, `learning_cases`, `observations`
(`.ai/data-model.md`). The SQLAlchemy models are defined in `apps/api/app/`
(TODO: create the models per the pipeline / ADR). The Learning Dependency Graph
(`.ai/ldg.md`) is a reference structure, not a table.

## Current Constraints

- Constitution wins over everything (`.ai/constitution.md`).
- No school management features (attendance, marks, ERP, chat, etc.).
- Self-hostable via Docker Compose (PostgreSQL); no required cloud dependency.
- Only three aggregates / three tables for v0.
- No dashboard, no analytics, no AI guessing, no recommendation engine.
- Every feature needs a real classroom case (THE CLASSROOM-CASE QUESTION);
  otherwise it goes to `.ai/ideas.md`.

## Current Decision Log

See `.ai/decision-log.md`. Key entries: Sprint 001 scope, the week-question
gate, the classroom-case challenge, the SYNC→AUDIT→NORMALIZE→FREEZE→IMPLEMENT
cadence (ADR-008), and the pre-implementation existence check (ADR-009).

## Files Allowed To Modify

- `apps/` (api, web) — implementation, within the domain model.
- `packages/domain/` — only when the domain genuinely changes (use
  workflow domain-change.md).
- `.ai/` — to keep docs consistent with code (glossary, decision-log, etc.).
- `knowledge/` — educational knowledge only (workflow knowledge-update.md).

## Files Forbidden To Modify

- `constitution.md` — supreme authority; propose changes, do not edit directly.
- Anything that would break the three-aggregate / three-table model without a
  classroom case.
- `FOUNDERS_AI_OPERATING_MANUAL.md` — the Founder's manual; propose, don't edit.
- Any file adding dashboards, analytics, AI guessing, or recommendation engines.

## Definition of Done

The feature helps a real teacher make one better decision for one real learner.
It passes the AI Development Pipeline stages and the A90 release checklist.

## Stop Conditions

- The classroom-case question has no answer → file in ideas.md, stop.
- "What educational decision becomes easier because of this code?" is unclear →
  STOP.
- A stage of the pipeline would violate the constitution → stop and say so.
- Never commit unless the Founder asks.

## Questions Before Coding

See `.ai/questions-before-code.md` and the A10 research questions. The first and
last question is always:

> "Can you point to a real classroom case that justifies this?"

## Reporting After Every Step

Do not dump code. After each step, answer four questions (see playbook.md §7):

1. **What changed?**
2. **Why was it necessary?**
3. **Which architectural rule did it follow?**
4. **What should be implemented next?**

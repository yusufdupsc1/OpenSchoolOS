# Domain Package

Shared educational domain model for OpenSchoolOS. The single source of truth for
domain types used by `apps/api` and `apps/web`.

## Sprint 001 — Three Aggregates Only

We deliberately model only three aggregates. Nothing else.

- **Student** — a child the teacher works with (search/click entry point).
- **LearningCase** — one active struggle for one Student. Holds the
  Observations, Possible Root Gap, Evidence, Strategy (intervention), Next
  Review, and eventual Close. An intervention is NOT a separate model — it is
  part of the LearningCase.
- **Observation** — a single recorded moment in the loop: Observed, Possible
  Root Gap, Evidence, Strategy, Next Review.

The Learning Dependency Graph (see `.ai/ldg.md`) is a reference structure used
inside a LearningCase to identify the root gap — not an aggregate.

## Persistence (v0)

Exactly three tables back these aggregates (see `.ai/data-model.md`):

- `students` ↔ Student
- `learning_cases` ↔ LearningCase
- `observations` ↔ Observation

Interventions are a column on `learning_cases`, not a separate table.

## Principles

Pure domain. No framework dependency. No business logic in the UI. See
`.ai/domain.md`, `.ai/coding-rules.md`.

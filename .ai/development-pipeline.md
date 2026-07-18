# AI Development Pipeline

Every coding task passes through these stages, in order. No stage is skipped.
This replaces random prompting with a disciplined pipeline.

```
Think
  ↓
Research
  ↓
Model
  ↓
Review
  ↓
Implement
  ↓
Refactor
  ↓
Validate
  ↓
Document
```

## Stage Definitions

### 1. Think
Challenge the request with the classroom-case question (constitution.md, THE
CLASSROOM-CASE QUESTION). If there is no real classroom case, file it in
ideas.md and stop. If justified, restate the problem as one teacher decision for
one learner.

### 2. Research
Read the governing docs in order: README.md → .ai/README.md → constitution.md →
philosophy.md / educational-principles.md → domain.md / data-model.md → the
specific doc for the task. Never invent educational theories. Request evidence
when uncertain.

### 3. Model
Locate or extend the domain. We model only three aggregates (Student,
LearningCase, Observation) and three tables. Reuse packages/domain types. An
intervention is part of a LearningCase, not a separate model.

### 4. Review
Before writing code, lay out the plan: which domain objects change, which
repository methods are needed, and how it serves the Educational Loop
(educational-loop.md). Surface any constitution conflict rather than hiding it.

### 5. Implement
Write the smallest honest change. Thin controllers, fat pure domain, no business
logic in the UI. Self-hostable; no cloud dependency for core functionality.

### 6. Refactor
Remove duplication, name from the domain vocabulary, keep it boring and
maintainable. No cleverness for its own sake.

### 7. Validate
Run it. For the API: exercise the FastAPI endpoints (e.g. via pytest or a seed
script) against the PostgreSQL dev database. TODO: add a FastAPI/Postgres
validation command once the SQLAlchemy models exist. Confirm the feature helps
one teacher decision. If a week of use would teach us nothing, the design must
change (educational-loop.md, After a Week of Use).

### 8. Document
Update .ai/ so it stays consistent with code. Add or revise the relevant doc.
Every file should earn the GitHub goal: "This teacher deeply understands
learning."

## Rules

- A task may not skip a stage. "Think" and "Research" are mandatory even for
  small changes.
- "Document" is part of done. Code without updated .ai/ consistency is not
  finished.
- The pipeline serves the constitution, not the other way around. If a stage
  would violate the constitution, stop and say so.

---

## Pre-Implementation Check (mandatory, before any code)

Before implementing a requested feature, Kilo MUST first check whether the
functionality already exists somewhere in the repository.

- Never duplicate functionality. Search the codebase and `.ai/` before building.
- Never rename established educational concepts (e.g. LearningCase, Observation,
  LDG, intervention/strategy). Renaming is an architectural decision — see the
  CTO Rule.
- Never introduce a new architectural pattern without explicit Founder approval.
- When uncertain whether something exists, conflicts, or fits — **report, do not
  implement**. Surface the question and stop.

This check runs at the start of the IMPLEMENT stage, after FREEZE. If a duplicate
or conflict is found, return to SYNC/NORMALIZE rather than building anew.

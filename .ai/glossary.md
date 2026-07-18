# Glossary

> Extracted terminology only. Every term below is defined in an existing
> `.ai/` document. No new terminology has been introduced.

## Constitution

- **Educational Operating System** — A system that helps teachers make better
  educational decisions through evidence-guided reasoning. (Not a School
  Management System.)
- **Evidence-guided reasoning** — Reasoning that is driven by evidence rather
  than assumption, used to support teacher decisions.
- **Learning growth** — Measurable improvement in learning, the target outcome
  of transforming classroom observations.
- **Teacher reasoning** — The professional thinking of teachers, which the
  system is built to preserve and support (not replace).
- **Professional judgment** — The expert decision-making of teachers, which the
  system supports rather than replaces.
- **Core beliefs** — Foundational statements the project adheres to:
  - Every child learns differently.
  - Learning difficulties are cumulative.
  - Diagnosis precedes intervention.
  - Observation precedes diagnosis.
  - Evidence precedes conclusion.
  - Teachers need thinking support.
  - Students are learning journeys—not marks.
- **Non goals** — Explicitly out-of-scope areas: Attendance, Payroll,
  Inventory, Accounting, Exam Management, ERP, Parent Billing, Chat, Generic AI
  chatbot.
- **Architectural rule** — "Pedagogy drives software. Software never drives
  pedagogy."
- **AI rule** — "Never invent educational theories. Never create assumptions.
  Always request evidence. If uncertain, create extension points, not fake
  intelligence."
- **Domain first** — Every feature must belong to the educational domain and
  improve a teacher's educational decision, or it should not exist.
- **Definition of Done** — The feature helps a real teacher make one better
  decision for one real learner.

## Domain

Sprint 001 models exactly three aggregates (see domain.md):

- **Student** — A child the teacher works with; the search/click entry point.
- **LearningCase** — One active struggle for one Student. Holds the
  Observations, Possible Root Gap, Evidence, Strategy (intervention), Next
  Review, and eventual Close. Interventions are NOT separate — they are part of
  the LearningCase.
- **Observation** — A single recorded moment in the loop: Observed, Possible
  Root Gap, Evidence, Strategy, Next Review.
- **Learning Dependency Graph (LDG)** — A reference structure (not an
  aggregate) representing the teacher intuition that "this depends on that"
  (e.g. Addition → Repeated Addition → Multiplication → Division). Used to
  identify the root gap. See ldg.md.

Other earlier terms (Evidence, Hypothesis, Misconception, Learning Gap, Learning
Prescription, Learner Response, Review, Outcome) are collapsed into the three
aggregates for now; they are not separate models yet.

## Educational Principles

- **Observe → Understand → Diagnose → Teach → Reflect → Improve** — The
  philosophical flow describing the educational cycle.
- **Observation precedes diagnosis** — Observation must come before a diagnosis
  can be made.
- **Diagnosis precedes intervention** — Diagnosis must come before any
  intervention.
- **Evidence precedes conclusion** — Conclusions require evidence first.
- **Students are learning journeys—not marks** — Students are understood as
  ongoing learning processes rather than scores.

## Teacher Thinking

- **Teacher Thinking Pattern** — The documented way a teacher reasons: diagnosis
  is not done by fixed questions but through repeated classroom interaction.
- **Repeated classroom interaction** — The means by which a teacher gathers
  evidence over time to inform diagnosis.
- **Hypothesis changes** — As evidence accumulates, the teacher's hypothesis
  changes.
- **Confidence** — The threshold of accumulated evidence after which a teacher
  intervenes.
- **Intervene** — The action a teacher takes only after sufficient confidence is
  reached.
- **Educational Loop** — The loop OpenSchoolOS validates: Observe → Think →
  Act → Reflect → Observe Again. The teacher runs it; the software only records
  and supports it (see educational-loop.md).

## Architecture

- **packages/domain** — The shared, framework-free educational domain model;
  single source of truth for domain types.
- **apps/api** — Backend serving the educational domain and persisting state.
- **apps/web** — The Educational Case Notebook front end (the only screen
  Sprint 001 builds).
- **Local-first data storage** — Data storage that keeps data on the school's
  infrastructure with full export and full deletion.
- **Local datastore** — The storage component supporting export and delete of
  all data.
- **Failure modes** — Defined failure scenarios and responses:
  - Hardware dies: restore from backup via a written runbook.
  - Update fails: automatic rollback to the previous version.
  - API or web fails: the other tier keeps running; the Notebook degrades
    gracefully.

# Data Model (v0)

The database for Sprint 001 has exactly three tables. That is enough for v0.

```
students
learning_cases
observations
```

## students

One row per child the teacher works with.

- id
- name
- (minimal — search and open only; no profiles, no report cards)

## learning_cases

One row per active struggle, belonging to one student.

- id
- student_id        → students.id
- possible_root_gap — the earliest missing prerequisite being investigated
- evidence          — what justifies the current thinking
- strategy          — the intervention chosen (part of the case, not separate)
- next_review       — when to look again
- status            — open / closed
- created_at, updated_at

An intervention is NOT a separate table. It lives in the `strategy` column of a
learning case. We keep it simple.

## observations

One row per recorded moment in the Educational Loop, belonging to one case.

- id
- learning_case_id  → learning_cases.id
- observed          — what the teacher saw
- possible_root_gap — the gap identified in this observation
- evidence          — what confirms it
- strategy          — the intervention chosen in this observation
- next_review       — when to look again
- created_at

Observations accumulate inside a case. As they do, the teacher's hypothesis
changes — the loop turns (see educational-loop.md).

## Mapping to the Domain

These three tables are the persistence of the three aggregates in domain.md:

- students        ↔ Student
- learning_cases  ↔ LearningCase
- observations    ↔ Observation

The Learning Dependency Graph (ldg.md) is NOT stored as a table — it is a
reference structure used to fill `possible_root_gap`.

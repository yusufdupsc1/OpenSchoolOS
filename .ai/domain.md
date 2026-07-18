# Domain Model — Sprint 001

Three aggregates only.

Student

LearningCase

Observation

Nothing else.

## Student

A child the teacher works with. The entry point: search, click, open.

## LearningCase

One active struggle for one Student.

A LearningCase holds everything about that struggle:

- the Observations made so far
- the Possible Root Gap being investigated (traced via the Learning Dependency
  Graph — see ldg.md)
- the Evidence gathered
- the Strategy (intervention) chosen
- the Next Review date
- the Review and eventual Close

An intervention is NOT modelled separately yet. It is simply part of a
LearningCase (the Strategy field). We keep it simple.

## Observation

A single recorded moment in the loop (see educational-loop.md):

- Observed — what the teacher saw
- Possible Root Gap — the earliest missing prerequisite
- Evidence — what justifies it
- Strategy — the intervention chosen
- Next Review — when to look again

Observations accumulate inside a LearningCase. As they do, the teacher's
hypothesis changes — the loop turns.

## Out of Scope (for now)

The earlier broader vocabulary — Evidence, Hypothesis, Competency, Misconception,
Learning Gap, Learning Prescription, Learner Response, Review, Outcome — is
collapsed into the three aggregates above. These concepts live inside a
LearningCase or an Observation; they are not separate models yet.

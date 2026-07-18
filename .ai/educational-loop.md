# The Educational Loop

This is what OpenSchoolOS is actually validating. Not a feature set. Not a
system. A loop.

```
Observe
  ↓
Think
  ↓
Act
  ↓
Reflect
  ↓
Observe Again
```

## Meaning

- **Observe** — what the teacher actually sees in the classroom.
- **Think** — the teacher reasons about root cause (using the Learning
  Dependency Graph, see ldg.md).
- **Act** — the teacher chooses a Strategy (the intervention). In Sprint 001
  the intervention is simply part of the LearningCase — not a separate model.
- **Reflect** — the teacher reviews what happened at the Next Review.
- **Observe Again** — the loop continues; evidence accumulates, the hypothesis
  changes.

## What the Software Does

The software does NOT run the loop. The teacher does.

The software only **records and supports** this loop:

- It records Observations, the Possible Root Gap, the Evidence, the Strategy,
  and the Next Review (see apps/web, New Observation — five fields).
- It keeps the Learning Case open so the loop is visible across time.
- It preserves teacher reasoning — it never replaces it.

## Relationship to Other Docs

- This loop is the validation target of the Educational Case Notebook
  (architecture.md, root README.md).
- It is the live form of the philosophy cycle
  (Observe → Understand → Diagnose → Teach → Reflect → Improve,
  philosophy.md) and the teacher thinking pattern (teacher-thinking.md).
- It is grounded in the domain model (domain.md): the three aggregates
  Student, LearningCase, and Observation. Hypothesis, root gap, evidence, and
  intervention all live inside a LearningCase for now.
- It obeys the constitution: DOMAIN FIRST, AI RULE (no fake intelligence), and
  the Definition of Done — one better decision for one learner.

## After a Week of Use — The Real Question

We do not ask about features. We ask only after a teacher has used the Notebook
for a week:

> "What did using this for a week teach us?"

- If the answer is **"nothing"** — we change the design.
- If the answer is **"it changed how I think about students"** — then we have
  found something worth expanding.

This is the Reflect step made explicit, and it is the gate that precedes any
expansion. It is the live form of the constitution's VALIDATION BEFORE
EXPANSION rule and the GitHub goal: a visitor should feel "this teacher deeply
understands learning." If a week of use teaches us nothing, no amount of
building matters.

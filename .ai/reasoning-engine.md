# Reasoning Process (teacher's, not a software component)

This is the teacher's internal reasoning, not a software component. It runs
inside a **LearningCase** (see domain.md) — every step becomes an
**Observation** and updates the case. The software only records it; it never
generates it.

```
Observation
  ↓
Hypothesis (Possible Root Gap)
  ↓
Evidence
  ↓
Confidence
  ↓
Alternative Hypothesis
  ↓
Need More Evidence?
  ↓
YES → Observe Again (loop continues)
  ↓
NO
  ↓
Choose Strategy (intervention — part of the LearningCase)
```

This loop is the live engine behind the Educational Loop
(educational-loop.md): Observe → Think → Act → Reflect → Observe Again.

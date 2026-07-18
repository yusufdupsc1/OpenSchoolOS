# Roadmap

OpenSchoolOS is built in layers. Each layer earns the next by proving it helps
one teacher make one better decision for one learner.

```
Knowledge          (LDG subject graphs, misconception patterns — see ldg.md, mental-model.md)
  ↓
Reasoning          (teacher thinking loop — see reasoning-engine.md, teacher-thinking.md)
  ↓
Domain             (three aggregates: Student, LearningCase, Observation — packages/domain)
  ↓
Application        (Educational Case Notebook — apps/web + apps/api)
  ↓
Platform           (local-first deploy, backup/restore, multi-teacher)
  ↓
Research           (measure whether cases improve learning — see questions-before-code.md)
  ↓
AI                 (only as extension points, never fake intelligence — constitution AI RULE)
```

## Sprint 001 — Educational Case Notebook

The only thing we build now:

```
Student → Create Learning Case → Record Observation →
Identify Root Gap → Choose Intervention → Review → Close Case
```

Nothing more. No dashboard, no analytics, no AI guessing.

## After Sprint 001: The Week Question

We do not expand until a teacher has used the Notebook for a week and we can
answer one question honestly:

> "What did using this for a week teach us?"

- **"Nothing"** → we change the design.
- **"It changed how I think about students"** → we have found something worth
  expanding, and only then do we move up the layer stack above.

This is the Reflect step of the Educational Loop (educational-loop.md) and the
practical face of the constitution's VALIDATION BEFORE EXPANSION rule.

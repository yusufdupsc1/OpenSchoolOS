# Research — Sprint 001 Week-of-Use Question

**Date:** 2026-07-23
**Trigger:** ADR-002 / `.ai/roadmap.md` / `.ai/educational-loop.md` §After a Week of Use
**Status:** Open question — no classroom evidence collected yet. Cannot be answered from code alone.

---

## What We Built

Sprint 001 delivered the Educational Case Notebook: a teacher records a student,
opens a learning case for one active struggle, and records observations (Observed,
Possible Root Gap, Evidence, Strategy, Next Review). The software records the
Educational Loop (Observe → Think → Act → Reflect → Observe Again); the teacher
runs it.

## What We Cannot Answer From Code

The week-of-use question is not a software question. It is a classroom question.

> **"What did using this for a week teach us?"**

The answer determines everything:
- **"Nothing"** → redesign.
- **"It changed how I think about students"** → expand.

The codebase cannot answer this. Only a teacher using the Notebook with real
learners can.

## Research Questions (from `.ai/research.md` and `.ai/questions-before-code.md`)

1. **What educational problem is solved?**  
   Learning difficulties are cumulative (Principle 001). The visible error is
   often not the root cause (Principle 002). Teachers need a way to capture
   reasoning over time so diagnosis precedes intervention and observation
   precedes diagnosis (Constitution, Core Beliefs).

2. **What teacher decision improves?**  
   Choosing an intervention based on accumulated evidence rather than a single
   observation. The Notebook should make the hypothesis visible across time.

3. **What classroom evidence justifies the feature?**  
   _Pending — requires one teacher, one learner, one week of use._ Until then,
   the feature is unvalidated.

4. **Which domain object changes?**  
   No new domain objects. The existing aggregates (Student, LearningCase,
   Observation) are sufficient for v0. Expansion (M2+) requires a classroom case.

5. **Could this be solved simpler?**  
   Notebook is intentionally minimal — three tables, three pages, five-field
   observation. No dashboard, no analytics, no AI. Simplicity is already baked
   in.

6. **Is this based on observation or assumption?**  
   Mixed. The educational principles (`.ai/educational-principles.md`) are drawn
   from the Constitution and existing knowledge, but the Notebook's usability
   is an assumption until a teacher uses it.

7. **Would Yusuf actually use this tomorrow?**  
   _Unknown — requires Founder/CTO classroom access or a teacher pilot._

8. **Does this preserve teacher reasoning?**  
   Yes — the Notebook records Strategy and Evidence inside the case; it never
   replaces judgment (Principle 005, Constitution).

9. **Can another teacher understand this?**  
   The UI is plain (list → open → form). Whether it is intuitive without
   instruction is unknown until used.

10. **Would removing this feature hurt learning?**  
    _Unknown — the Notebook has not yet been proven to improve learning outcomes._

## What the Week-of-Use Study Should Measure

If Sprint 001 is deployed for a week, the study should record:

| Metric | Signal |
|--------|--------|
| Teacher opens the Notebook at least once per day | Adoption |
| Teacher adds ≥3 observations to one case | Engagement with the loop |
| Teacher revises the Possible Root Gap or Strategy between observations | Reasoning preserved, not just logging |
| Teacher closes at least one case | Completion of the loop |
| Teacher says "it changed how I think about this student" (or equivalent) | **The gate question answered positively** |
| Teacher says "this taught me nothing" or abandons after <3 uses | **Negative signal — redesign** |

## Relationship to the Layer Stack

```
Application (Notebook) — BUILT, UNVALIDATED
  ↓
Research (this file)     — OPEN, AWAITING CLASSROOM USE
  ↓
AI / Expansion           — GATED BY THIS RESEARCH
```

No code should be written for M2 (Reasoning Timeline), M3 (LDG), M4 (Knowledge
Base), or M5 (Classroom Validation) until this research produces a finding.

## Outcome

**Cannot route to new-feature.md.** No classroom case exists to justify expansion.

**Open questions filed in research:**
1. What does a teacher say after one week of Notebook use?
2. Does the Notebook make the hypothesis visible across time?
3. Does it change the teacher's next intervention decision?
4. What breaks, what feels unnecessary, what is missing?

**Next step:** One teacher, one learner, one week. Then the Founder answers the
week question honestly.

## Stop Condition

From the Execution Protocol:

> Immediately stop if ... Breaking change

This research finding does not authorize building M2+. It authorizes only a
classroom pilot. No implementation should proceed until the week question is
answered in writing by the Founder/CTO.

---

*This document is the live form of ADR-002. It will be updated when classroom
evidence is collected.*

# Workflow: Bug Fix

Use when correcting incorrect or broken behaviour.

## 1. Think (A00)
- Identify the educational decision the bug breaks. A bug that doesn't affect a
  teacher decision may not be worth fixing yet — say so.
- Reproduce from the teacher workflow, not from stack traces alone.

## 2. Research (A10)
- What observation/case is affected? Which classroom case reveals it?
- Confirm it is a real defect, not a missing feature (features go to
  new-feature.md / ideas.md).

## 3. Model & Locate (A20)
- Trace to the aggregate (Student, LearningCase, Observation) and the
  repository in apps/api/src. Never patch outside the domain boundary.

## 4. Fix (A50, A60)
- Smallest change. Keep persistence in repositories, logic in domain.
- If UI, keep it teacher-thinking-shaped.

## 5. Test (A80)
- Add a regression test at the educational-workflow level.

## 6. Review (A70)
- Confirm no DDD violation, no duplicated logic, no premature optimisation.

## 7. Release (A90)
- Verify against the release checklist. Approve only if all pass.

## 8. Document
- Note the fix in decision-log.md if it changes reasoning or assumptions.

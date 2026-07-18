# Workflow: New Feature

Use when adding a capability to OpenSchoolOS.

## 1. Think (A00, A10)
- Challenge with the classroom-case question (constitution.md, THE
  CLASSROOM-CASE QUESTION).
- If no real classroom case → write to ideas.md, stop.
- Answer the A10 research questions. The feature must improve one teacher
  decision for one learner.

## 2. Research & Model (A20, A30)
- Identify entities, value objects, aggregates, domain services, repositories,
  policies, events (DDD).
- We model only three aggregates: Student, LearningCase, Observation.
- Educational knowledge (competencies, misconceptions, interventions, mental
  models) belongs in knowledge/, never hardcoded in app logic.

## 3. Architecture Review (A40)
- Return a review against SOLID, DDD, Clean Architecture, the dependency rule.
- Implementation begins only after approval.

## 4. Implement (A50, A60)
- One vertical slice. Thin controllers, fat pure domain, no persistence leak.
- UI reduces teacher thinking effort; prefer Observation → Reasoning →
  Decision → Review over data entry.

## 5. Test (A80)
- Unit, domain, integration, and educational workflow tests. Test behaviour,
  not implementation.

## 6. Review (A70)
- Identify DDD violations, educational inconsistencies, duplication, premature
  optimisation, hidden assumptions, naming, complexity. Suggest; don't rewrite
  immediately.

## 7. Release (A90)
- Verify educational philosophy, architecture, domain, quality, performance,
  docs, README, decision log, research notes. Approve only if all pass.

## 8. Document
- Update .ai/ so it stays consistent. Log the decision in decision-log.md.

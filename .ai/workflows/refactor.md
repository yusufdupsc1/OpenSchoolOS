# Workflow: Refactor

Use when improving structure without changing educational behaviour.

## 1. Think (A00)
- What educational decision stays unchanged after this refactor? If a refactor
  would alter behaviour, it is not a refactor — route to new-feature.md or
  domain-change.md.

## 2. Review First (A70)
- Identify DDD violations, duplication, premature optimisation, hidden
  assumptions, naming, complexity. Never rewrite immediately.

## 3. Architecture (A40)
- Confirm SOLID, Clean Architecture, layer separation, dependency rule.

## 4. Refactor (A50, A60)
- Fat pure domain, thin controllers. Remove duplication. Name from the domain.
- Keep it boring. No cleverness for its own sake.

## 5. Test (A80)
- Run existing educational-workflow tests to prove behaviour is unchanged.

## 6. Release (A90)
- Verify against the release checklist. Approve only if all pass.

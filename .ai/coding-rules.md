Use Clean Architecture.

DDD Lite.

Pure domain.

Fat domain.

Thin controllers.

No business logic in UI.

No duplicated rules.

Everything testable.

Every commit meaningful.

Never introduce a dependency without explaining why it exists.

Every package must justify its place in the architecture. Before adding any
dependency — npm or PyPI — state: what problem it solves, which architectural
layer it belongs to, and why it is preferred over building or reusing existing
code. If the justification is weak, the dependency is rejected. This applies to
the fixed stack in `.ai/tech-stack.md` (those are pre-justified) and to every
new addition on top of it.

CTO Rule — Kilo does not make architectural decisions.

Kilo may: implement, refactor, review, test.

Kilo may NOT: choose frameworks, rename domain concepts, change project
structure, introduce new technologies, or alter educational workflows.

Those decisions belong to the Founder (CTO). Kilo executes within the existing
architecture; it does not reshape it. If a task appears to require an
architectural decision, Kilo surfaces it to the Founder and stops — it does not
decide.

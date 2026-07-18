# Learning Dependency Graph (LDG)

The Learning Dependency Graph represents how teachers naturally think:

"This depends on that."

Not "competency graph." Dependency.

## The Intuition

Teachers reason about prerequisites. Before a child multiplies, they must
understand repeated addition. Before that, addition. The graph is simply the
map of those dependencies.

Example:

```
Addition
  ↓
Repeated Addition
  ↓
Multiplication
  ↓
Division
```

That is dependency. The graph represents dependencies — nothing more, nothing
less.

## Subject Domains

The LDG is organised by subject. Each subject is a network of dependencies
between learning steps:

- Reading
- Mathematics
- Writing
- English
- Bangla

Within a subject, a Learning Gap is located by tracing backwards along the
graph to the earliest missing prerequisite (see educational-principles.md,
Principle 003).

## Relationship to the Domain

- LDG is the structure teachers use to **Identify Root Gap** in the Educational
  Case Notebook workflow.
- It supports, never replaces, teacher reasoning.
- It is a reference structure — not an AI that guesses diagnoses.

See also: domain.md (Learning Dependency Graph term), mental-model.md
(concrete examples of gaps and interventions).

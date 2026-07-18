# Workflow: Domain Change

Use when the domain model itself changes (aggregates, relationships, tables).

## 1. Think (A00, A10)
- Why does the model need to change? Point to the classroom case.
- Remember: we model only three aggregates (Student, LearningCase,
  Observation). An intervention is part of a LearningCase, not separate.

## 2. Model (A20)
- Apply DDD: entities, value objects, aggregates, domain services,
  repositories, policies, events.
- Update packages/domain/src/types.ts (the single source of truth).

## 3. Data (see .ai/data-model.md)
- If tables change, update the SQLAlchemy models in apps/api/app/ (TODO: create
  the models per the pipeline). The three-table schema (students,
  learning_cases, observations) is defined in .ai/data-model.md.
- We have exactly: students, learning_cases, observations. No other tables for
  v0.

## 4. Architecture Review (A40)
- Confirm layer separation and the dependency rule hold after the change.

## 5. Implement & Test (A50, A60, A80)
- Migrate repositories, add domain + integration tests (pytest against
  PostgreSQL).

## 6. Review (A70)
- Watch for hidden assumptions and naming drift from the domain vocabulary.

## 7. Document
- Update domain.md, data-model.md, glossary.md, and decision-log.md.

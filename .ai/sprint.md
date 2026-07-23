# Active Sprint

Sprint 001

## Goal

Educational Case System

## Current Milestone

M1 — Educational Case System (implementation complete)

## Completed

- Repository (pnpm workspace scaffold)
- Frozen technology stack (FastAPI + PostgreSQL + SQLAlchemy + Alembic, no auth)
- Project Constitution (.ai/)
- Domain: Student, LearningCase, Observation aggregates (46/46 tests)
- Infra: three tables + Alembic migration
- API: FastAPI shell + CRUD routes + integration tests
- Web: Students / Learning Cases / New Observation pages + create forms

## Next

Validate with one teacher for a week (ADR-002 week-of-use question).
Expansion toward M2 (Reasoning Timeline) is gated on that answer.

## Definition of Done

Student
↓
Learning Case
↓
Observation
↓
Timeline

working end-to-end

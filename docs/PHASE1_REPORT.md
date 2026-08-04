# Phase 1: Sprint 001.5 — Harden Report

Date: 2026-08-04

## Summary

All 8 planned hardening features implemented. API layer fully modernized with
UUIDs, CRUD completeness, soft delete, search, and timeline. Frontend updated
to expose every new capability.

## What Changed

### 1.1 UUID-based IDs ✅
- Replaced string-concatenated IDs (`STU-12-5A`, `LC-...`, `OB-...`) with
  `uuid4()` in all three routers.
- Added `UniqueConstraint` on `students(grade, section, roll_number)` to
  replace the old ID-based conflict detection.
- Files: `apps/api/app/routers/students.py`, `learning_cases.py`, `observations.py`,
  `apps/api/app/models.py`

### 1.2 Soft Delete ✅
- Added `deleted_at` column (nullable DateTime) to all three models.
- All list/search/timeline queries filter `WHERE deleted_at IS NULL`.
- New `DELETE` endpoints on all three resources (returns 204).
- Files: `apps/api/app/models.py`, all three routers

### 1.3 PATCH Student ✅
- New `PATCH /students/{id}` endpoint with `StudentUpdate` schema.
- Frontend: modal edit form with full name, roll number, grade, section, status.
- Files: `apps/api/app/routers/students.py`, `apps/api/app/schemas.py`,
  `apps/web/app/students/[id]/EditStudentForm.tsx`

### 1.4 PATCH Observation ✅
- New `PATCH /observations/{id}` endpoint with `ObservationUpdate` schema.
- Files: `apps/api/app/routers/observations.py`, `apps/api/app/schemas.py`

### 1.5 Reopen Case ✅
- New `PATCH /learning-cases/{id}/reopen` endpoint.
- Existing `PATCH /learning-cases/{id}/close` retained.
- Frontend: toggle button (Close/Reopen) with status-aware styling.
- Files: `apps/api/app/routers/learning_cases.py`,
  `apps/web/app/learning-cases/[id]/CaseActions.tsx`

### 1.6 Case Detail View ✅
- New `GET /learning-cases/{id}` endpoint returns single case.
- Frontend case page now shows: subject, competency, possible root gap,
  evidence, strategy, next review, status, plus all observations below.
- Edit, close/reopen, and delete actions available on the case page.
- Files: `apps/api/app/routers/learning_cases.py`,
  `apps/web/app/learning-cases/[id]/page.tsx`,
  `apps/web/app/learning-cases/[id]/EditCaseForm.tsx`

### 1.7 Search Students ✅
- New `q` query parameter on `GET /students` — searches full_name and
  roll_number with ILIKE.
- Frontend: search input with submit button, updates URL with `?q=…`.
- Files: `apps/api/app/routers/students.py`,
  `apps/web/app/page.tsx`, `apps/web/app/StudentSearch.tsx`

### 1.8 Timeline View ✅
- New `GET /students/{id}/timeline` endpoint returns all observations
  across all cases for a student, newest-first.
- Frontend: timeline section on the student detail page showing each
  observation with case subject, date, observed, root gap, and strategy.
- Files: `apps/api/app/routers/students.py`, `apps/api/app/schemas.py`
  (new `TimelineEntry` schema), `apps/web/app/students/[id]/page.tsx`

## Files Modified/Created

### Backend (apps/api/)
| File | Change |
|------|--------|
| `app/main.py` | Added `lifespan` to auto-create tables on startup |
| `app/models.py` | Added `deleted_at`, unique constraint, UUID-sized IDs (36) |
| `app/schemas.py` | Added Update schemas, TimelineEntry schema, deleted_at fields |
| `app/routers/students.py` | UUID, PATCH, DELETE, GET by id, search, timeline |
| `app/routers/learning_cases.py` | UUID, PATCH, GET by id, DELETE, reopen, status filter |
| `app/routers/observations.py` | UUID, PATCH, GET by id, DELETE |
| `tests/test_api.py` | 15 tests covering all new endpoints |
| `pyproject.toml` | Fixed build config |

### Frontend (apps/web/)
| File | Change |
|------|--------|
| `lib/api.ts` | Added all new API methods and types |
| `app/page.tsx` | Added search functionality |
| `app/StudentSearch.tsx` | **NEW** — client search component |
| `app/students/[id]/page.tsx` | Added student header, timeline, edit/delete |
| `app/students/[id]/EditStudentForm.tsx` | **NEW** — modal edit form |
| `app/students/[id]/DeleteStudentButton.tsx` | **NEW** — confirm-delete |
| `app/learning-cases/[id]/page.tsx` | Full case detail card + observations |
| `app/learning-cases/[id]/CaseActions.tsx` | **NEW** — close/reopen/delete |
| `app/learning-cases/[id]/EditCaseForm.tsx` | **NEW** — modal edit form |

## Test Results

- **Domain tests:** 46/46 ✅
- **API tests:** 15/15 ✅
- **TypeScript:** compiles clean ✅
- **API server:** running on port 8000 ✅
- **Web server:** running on port 3000 ✅

## What Was NOT Changed

- `packages/domain/` — unchanged (pure domain is stable)
- `.ai/` constitution — unchanged (no new ADRs needed; these are implementation
  hardening, not scope expansion)
- The three-table model — preserved; `deleted_at` is an infrastructure column,
  not a domain change
- No dashboards, no analytics, no AI, no recommendation engine

## Next Phase (gated on ADR-002)

Phase 2: Knowledge Layer — Learning Dependency Graph (LDG) as curated reference
structure in `knowledge/`.

# Phase 4: Application Layer — Expanded Notebook

Date: 2026-08-04

## Summary

Extended the Educational Case Notebook with subject templates from the LDG,
reflection-based case closure, bulk student import via CSV, printable case
reports for parent meetings, and case transfer between students.

## What Changed

### 4.5 Subject Templates ✅

LDG-integrated subject/competency dropdowns in the create case form:

- **Subject dropdown** — populated from all 5 LDG subjects (Math, Reading,
  Writing, English, Bangla) with "Other" fallback
- **Competency dropdown** — dynamically loaded when a subject is selected,
  showing grade levels
- **Auto-fill** — selecting a competency pre-fills root gap, evidence, and
  strategy from the first misconception pattern
- Free-text fields remain available for custom subjects/competencies

Files: `apps/web/app/SubjectTemplatePicker.tsx` (new),
`apps/web/app/students/[id]/NewLearningCaseForm.tsx` (updated)

### 4.1 Case Review/Reflection ✅

Closing a case now prompts for a teacher reflection:

- "Close Case" button opens a reflection input field
- Teacher can write what they learned, why they're closing, what worked
- Reflection is saved in the `reflection` column on the case
- Closed cases show the reflection in a green callout box and the `closed_at`
  timestamp
- Reopening clears the `closed_at` timestamp

Files: `apps/api/app/models.py` (+2 columns: `reflection` Text, `closed_at` DateTime),
`apps/api/app/schemas.py` (+CloseCaseBody schema),
`apps/api/app/routers/learning_cases.py` (close accepts reflection body, reopen
clears closed_at),
`apps/web/app/learning-cases/[id]/CaseActions.tsx` (reflection input on close),
`apps/web/app/learning-cases/[id]/page.tsx` (reflection + closed_at display)

### 4.3 Bulk Student Import ✅

CSV upload for adding many students at once:

- `POST /students/import` — accepts CSV file with columns: `full_name`,
  `roll_number`, `grade`, `section`
- Returns `BulkImportResult` with `created` count and `errors` list
- Frontend: file picker + upload button with results display
- Graceful error handling: reports per-row errors, commits successful rows

Files: `apps/api/app/routers/students.py` (+import endpoint),
`apps/api/app/schemas.py` (+BulkImportResult),
`apps/web/app/BulkImport.tsx` (new),
`apps/web/app/page.tsx` (added BulkImport below new student form)

### 4.2 Print/Export Case ✅

Server-rendered printable HTML for parent meetings:

- `GET /learning-cases/{id}/print` — returns a clean HTML page
- Shows: student name, grade, case details, all observations in a table with
  confidence and evidence strength badges, and teacher reflection
- Print-optimized CSS (`@media print`) for clean output
- Frontend: "Print" button opens in new tab

Files: `apps/api/app/routers/learning_cases.py` (+print endpoint),
`apps/web/app/learning-cases/[id]/CaseActions.tsx` (+Print button)

### 4.4 Case Transfer ✅

Move a case to a different student:

- `POST /learning-cases/{id}/transfer` — accepts `{"student_id": "..."}`
- Validates target student exists and is not deleted
- All observations remain attached to the case
- Useful for: moving cases to new school year records, transferring between
  sibling records, correcting student assignment

Files: `apps/api/app/schemas.py` (+TransferCaseBody),
`apps/api/app/routers/learning_cases.py` (+transfer endpoint)

## Test Results

| Suite | Count | Status |
|-------|-------|--------|
| Domain (Vitest) | 46 | ✅ |
| API (pytest) | 15 | ✅ |
| Knowledge (pytest) | 11 | ✅ |
| Reasoning (pytest) | 5 | ✅ |
| **Total** | **77** | **✅** |
| TypeScript | — | ✅ |

## Live Demo

- **API:** http://localhost:8000/docs
- **Website:** http://localhost:3000
- **Print preview:** http://localhost:8000/learning-cases/{id}/print
- **CSV import:** Upload on the Students page
- **LDG templates:** Subject/competency dropdowns in New Learning Case form

## Design Decisions

- **Reflection is free text**, not structured. Per the constitution, teacher
  reasoning is preserved, not boxed into categories.
- **CSV import prioritizes partial success** — one bad row doesn't block others.
- **Print view is server-rendered HTML**, not PDF. Print-to-PDF is done by
  the browser. No new dependencies.
- **Transfer is a simple student_id change**, not a deep clone. Observations
  belong to the case, not the student.
- **Subject template uses dropdown + free-text hybrid** — teachers are never
  forced into the LDG if they need something custom.

## Next Phase (gated on ADR-002)

Phase 5: Platform Layer — backup/restore, authentication, multi-teacher support,
data export.

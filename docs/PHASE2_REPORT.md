# Phase 2: Knowledge Layer — LDG (Learning Dependency Graph)

Date: 2026-08-04

## Summary

Built the Learning Dependency Graph as curated knowledge files across 5 subjects
(Mathematics, Reading, Writing, English, Bangla) with an API and a smart
RootGapPicker component that integrates the LDG into the case/observation
creation workflow.

## What Changed

### 2.1 LDG Data Structure ✅

5 knowledge files in `knowledge/`, each containing:

- **Subject metadata** (name, description)
- **Competencies** — 31 total across all subjects:
  - Mathematics: 10 (Number Sense → Place Value → Addition → Subtraction →
    Repeated Addition → Multiplication → Division → Fractions → Decimals →
    Word Problem Solving)
  - Reading: 5 (Phonemic Awareness → Phonics → Fluency, Vocabulary →
    Comprehension)
  - Writing: 5 (Letter Formation → Spelling → Sentence Construction →
    Paragraph → Extended Composition)
  - English: 5 (Parts of Speech → Tenses, Subject-Verb Agreement, Punctuation →
    Sentence Variety)
  - Bangla: 6 (Letter Recognition → Kar → Joint Letters → Reading Fluency →
    Comprehension, Composition)
- **Dependency graphs** — each competency declares its prerequisites
- **Misconception patterns** — 20+ patterns with observed behaviour, root gap,
  evidence, and strategy for each

Files: `knowledge/math.json`, `knowledge/reading.json`, `knowledge/writing.json`,
`knowledge/english.json`, `knowledge/bangla.json`

### 2.2 LDG API ✅

New `knowledge` router serving read-only reference data:

| Endpoint | Purpose |
|---|---|
| `GET /knowledge/subjects` | List all 5 subjects with metadata |
| `GET /knowledge/subjects/{subject}` | Full LDG: competencies + dependency graph |
| `GET /knowledge/subjects/{subject}/competencies` | Flat competency list |
| `GET /knowledge/subjects/{subject}/competencies/{id}` | Single competency with misconceptions |
| `GET /knowledge/subjects/{subject}/search?q=…` | Search competencies & misconceptions within subject |
| `GET /knowledge/search?q=…` | Cross-subject search |

Files: `apps/api/app/routers/knowledge.py`, `apps/api/app/main.py`

### 2.3 LDG-Guided Root Gap Picker ✅

New `RootGapPicker` client component:

- Type in the "Possible Root Gap" field to search the LDG
- Dropdown shows matching competencies with grade level
- Matched misconceptions appear as sub-options with a pattern label
- Selecting a misconception auto-fills: root gap, evidence, AND strategy
- Scoped by subject when the case's subject is known (e.g., Mathematics →
  searches math.json)
- Falls back gracefully: teacher can still type freely

Integration points:
- `NewLearningCaseForm` — root gap picker with LDG search, evidence/strategy
  auto-fill from misconception patterns
- `NewObservationForm` — same, scoped to the case's subject
- Both forms upgraded to use `<textarea>` for evidence and strategy fields,
  and `<input type="date">` for next review

Files: `apps/web/app/RootGapPicker.tsx`,
`apps/web/app/students/[id]/NewLearningCaseForm.tsx`,
`apps/web/app/learning-cases/[id]/NewObservationForm.tsx`,
`apps/web/lib/api.ts`

### 2.4 Misconception Patterns ✅

Every competency includes misconception patterns with:
- **Observed** — what the teacher actually sees
- **Root Gap** — the earliest missing prerequisite
- **Evidence** — what confirms the diagnosis
- **Strategy** — a concrete intervention suggestion

Examples:
- Math Multiplication: "Student memorizes tables. Cannot explain why." →
  root gap: "Repeated addition is never understood."
- Reading Phonics: "Guesses words" → root gap: "Words memorized visually;
  letters not mapped to sounds."
- Bangla Kar: "Reads কি as ক" → root gap: "Treats base consonant as full
  syllable."

## Test Results

- **Domain tests:** 46/46 ✅
- **API tests:** 15/15 ✅
- **Knowledge tests:** 11/11 ✅
- **Total:** 72/72 ✅
- **TypeScript:** compiles clean ✅

## Live Servers

- **API:** http://localhost:8000/docs — all endpoints including /knowledge/*
- **Website:** http://localhost:3000 — LDG picker in all create forms

## Design Decisions

- Knowledge files are static JSON — no database, no migrations. They change
  with code deploys, not at runtime.
- API is read-only. Teachers cannot modify the LDG through the UI; that's
  curricular work done by domain experts.
- The RootGapPicker always allows free-text input. The LDG supports reasoning,
  it never constrains it (per constitution AI RULE).
- Knowledge is cached in-memory after first load.

## Next Phase (gated on ADR-002)

Phase 3: Reasoning Layer — make teacher thinking visible:
- Reasoning timeline per case (how hypotheses change over observations)
- Confidence tracking (low/medium/high)
- Evidence strength tagging

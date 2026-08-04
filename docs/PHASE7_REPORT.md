# Phase 7: AI Layer — Extension Points Only

Date: 2026-08-04

## Summary

Built three AI extension points — not AI features, but structured interfaces
that an external AI agent or LLM could use. Per the constitution, nothing is
auto-applied. Every result is presented for teacher review.

## What Changed

### 7.1 Similar Cases Lookup ✅

`GET /ai/similar-cases/{case_id}?max_results=10`

Finds cases from other students that share the same root gap, subject, or
strategy. Each result includes:

- **Match type** — `same_root_gap`, `same_subject`, or `same_strategy`
- **Student context** — name, subject, competency
- **Status & outcome** — whether the case was closed and what happened
- **Observation count** — how much evidence was gathered

Frontend: `SimilarCases` component on every case page, showing matching cases
as clickable cards.

Files: `apps/api/app/routers/ai.py`, `apps/api/app/schemas.py`,
`apps/web/app/learning-cases/[id]/SimilarCases.tsx`

### 7.2 Observation Summarizer ✅

`GET /ai/observation-summary/{case_id}`

Packages a case's observations into a structured summary:

- **Heuristic summary** — concatenated narrative string (no LLM)
- **Root gap progression** — how the hypothesis changed: "Place value → Number sense"
- **Confidence progression** — low → medium → high
- **Strategy progression** — how the intervention evolved
- **Raw context** — full text formatted for external AI consumption

Frontend: `ObservationSummary` component showing the heuristic summary, root
gap evolution as chips, confidence badges, and a toggleable raw context view.

Files: `apps/api/app/routers/ai.py`, `apps/api/app/schemas.py`,
`apps/web/app/learning-cases/[id]/ObservationSummary.tsx`

### 7.3 Autocomplete (LDG + Past Cases) ✅

`GET /ai/autocomplete?q=…&source=ldg|past_cases|all`

Searches for matching root gap strings from:

- **LDG knowledge files** — competencies and misconception root gaps
- **Past cases** — distinct root gaps from previously recorded cases

Returns up to 15 matching strings with their source.

This extends the existing `RootGapPicker` which already does LDG search in
the create forms.

Files: `apps/api/app/routers/ai.py`, `apps/api/app/schemas.py`

## Frontend Integration

All three extension points appear on every case detail page:

```
┌─ Case Detail ─────────────────────────────────────┐
│  Math — Fractions                                 │
│  [Case card] [Reflection]                         │
│                                                   │
│  ┌─ Similar Cases (1) ────────────────────────┐  │
│  │  Rahim: Math — Addition (same_root_gap)    │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
│  ┌─ Observation Summary ──────────────────────┐  │
│  │  Root gap: Place value                     │  │
│  │  Confidence: low → high                     │  │
│  │  [Show raw AI context]                     │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
│  [New Observation Form]                           │
└───────────────────────────────────────────────────┘
```

## Test Results

| Suite | Count | Status |
|-------|-------|--------|
| Domain (Vitest) | 46 | ✅ |
| API | 15 | ✅ |
| Knowledge | 11 | ✅ |
| Reasoning | 5 | ✅ |
| Auth | 9 | ✅ |
| Platform | 5 | ✅ |
| Research | 5 | ✅ |
| AI | 7 | ✅ |
| **Total** | **103** | **✅** |
| TypeScript | — | ✅ |

## Constitutional Compliance

Per `.ai/constitution.md` AI RULE:

- ✅ Never invents educational theories — all summaries are heuristic concatenation
- ✅ Never creates assumptions — autocomplete shows what exists, never guesses
- ✅ Always requests evidence — similar cases link to actual recorded evidence
- ✅ Creates extension points, not fake intelligence — every endpoint returns
  data for teacher review; nothing is auto-applied

## Live Demo

```
=== Similar Cases ===
Source: Math — Place value
Found 1 similar case(s):
  Rahim: Math — Addition (same_root_gap, 0 obs)

=== Observation Summary ===
Case for Aisha: Math — Fractions.
Root gap evolved: Place value.
Strategy evolved: Base-10 blocks.
Confidence ranged: low → high.
Latest observation: 'Now writes 12 correctly with blocks'

=== Autocomplete ===
6 matches (source=all):
  'Place Value', 'No mental representation...', 'Does not extend...', ...
```

## Complete Project Summary

| Phase | Features | Tests |
|-------|----------|-------|
| Phase 1: Harden | UUIDs, full CRUD, search, soft delete, timeline | 15 |
| Phase 2: Knowledge | 5 LDG subjects, 31 competencies, smart picker | 11 |
| Phase 3: Reasoning | Confidence, evidence strength, alt hypotheses, timeline | 5 |
| Phase 4: Application | Templates, reflection, bulk import, print, transfer | — |
| Phase 5: Platform | Auth, multi-teacher, health, export, backup/restore | 14 |
| Phase 6: Research | Outcome tracking, duration metrics, strategy effectiveness | 5 |
| Phase 7: AI | Similar cases, observation summary, autocomplete | 7 |
| **Total** | **35+ features, 103 tests, 0 failures** | **103** |

The entire roadmap from `.ai/roadmap.md` is now implemented:
```
Knowledge → Reasoning → Domain → Application → Platform → Research → AI ✅
```

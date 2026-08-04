# Phase 6: Research Layer

Date: 2026-08-04

## Summary

Built the research and analytics layer — the "proof" that OpenSchoolOS helps
teachers make better decisions. Outcome tracking captures what happened after
case closure. A rich analytics dashboard aggregates case durations by subject
and grade, ranks strategies by effectiveness, and measures observation volume.

## What Changed

### 6.1 Case Outcome Tracking ✅

New `outcome` column on LearningCase — records what happened after closure:

- `improved` — learner showed measurable progress
- `plateaued` — no clear change
- `worsened` — learner regressed
- `transferred` — case moved to another teacher/context
- `unknown` — default when no outcome is specified

**Integration points:**
- `PATCH /learning-cases/{id}/close` — accepts `{"outcome": "improved", "reflection": "..."}`
- `PATCH /learning-cases/{id}` — outcome can be set/updated via normal update
- Close flow in the UI now shows an outcome dropdown alongside the reflection field
- Backup/restore includes outcome data

Files: `apps/api/app/models.py` (+outcome column),
`apps/api/app/schemas.py` (+outcome fields), `apps/api/app/routers/learning_cases.py`,
`apps/api/app/routers/platform.py`, `apps/web/app/learning-cases/[id]/CaseActions.tsx`,
`apps/web/lib/api.ts`

### 6.2 Time-to-Close Metrics ✅

New `GET /research/dashboard` endpoint that computes:

- **Overall duration** — avg/median/min/max days for all closed cases
- **By subject** — duration breakdown per subject (Math, Reading, Writing, etc.)
- **By grade** — duration breakdown per grade level
- Uses actual time deltas between `created_at` and `closed_at`

Files: `apps/api/app/routers/research.py` (new), `apps/api/app/schemas.py`
(+DurationMetrics, DurationReport)

### 6.3 Intervention Effectiveness ✅

The dashboard ranks strategies by usage and correlates them with outcomes:

- **Top 10 strategies** by case count
- Each strategy shows: improved / plateaued / worsened / unknown breakdown
- Teachers can see which strategies correlate with improvement

Strategy names are truncated at 80 chars for grouping; different phrasings of
the same approach appear as separate entries.

Files: `apps/api/app/routers/research.py`, `apps/api/app/schemas.py`
(+StrategyEffectiveness)

### 6.4 Research Dashboard (Frontend) ✅

New `/research` page with:
- **Summary cards** — total cases, open, closed, observations
- **Outcome breakdown** — color-coded pills (green=improved, amber=plateaued, red=worsened)
- **Time-to-close** — overall stats + per-subject breakdown
- **Strategy effectiveness** — ranked list with outcome counts per strategy
- **Cases per subject** — distribution across subjects

Files: `apps/web/app/research/page.tsx` (new), `apps/web/app/layout.tsx`
(+Research nav link)

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
| **Total** | **96** | **✅** |
| TypeScript | — | ✅ |

## Dashboard Demo Data

```
Cases:      3 total (1 open, 2 closed)
Observations: 3 (1.0 avg/case)

Outcomes:   improved: 1, plateaued: 1

Top strategies:
  "Base-10 blocks" — 1 case (improved=1)
  "Sound drills"   — 1 case (plateaued=1)

Cases per subject: Math:1, Reading:1, Writing:1
```

## Design Decisions

- **Outcome is teacher-reported, not auto-detected.** Per the constitution,
  teacher judgment is preserved; the system doesn't guess whether a learner
  improved.
- **Duration metrics are computed live** from `created_at` and `closed_at`,
  not a pre-computed column. This ensures accuracy, and the cost is negligible
  for a single-school deployment.
- **Strategy effectiveness is directional, not statistical.** With realistic
  sample sizes (dozens not thousands), we show patterns without claiming
  significance. This is honest research, not misleading analytics.
- **Dashboard is read-only** — no new write endpoints, only aggregation of
  existing data.

## Full Sprint Completion

| Phase | Features | Tests |
|-------|----------|-------|
| Phase 1 | UUIDs, CRUD, search, soft delete, timeline | 15 |
| Phase 2 | LDG knowledge: 5 subjects, 31 competencies, misconception patterns | 11 |
| Phase 3 | Reasoning: confidence, evidence strength, alt hypotheses, timeline | 5 |
| Phase 4 | Templates, reflection, bulk import, print, transfer | 0 (frontend only) |
| Phase 5 | Auth, multi-teacher, health, export, backup/restore | 14 |
| Phase 6 | Outcome tracking, duration metrics, strategy effectiveness, research dashboard | 5 |
| **Total** | **30+ features, 96 tests, 0 failures** | **96** |

## Next Phase (gated on ADR-002)

Phase 7: AI Layer — extension points only (LDG autocomplete, similar case lookup,
observation summarizer). Per the constitution, AI never invents educational
theories, never creates fake intelligence, and is only added as extension points
that a teacher controls.

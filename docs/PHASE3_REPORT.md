# Phase 3: Reasoning Layer

Date: 2026-08-04

## Summary

Made teacher thinking visible and traceable. Added confidence tracking, evidence
strength tagging, alternative hypotheses, and a reasoning timeline that shows
how the teacher's hypothesis evolves across observations — directly implementing
the reasoning loop from `.ai/reasoning-engine.md`.

## What Changed

### 3.1 Reasoning Timeline ✅

New `GET /learning-cases/{id}/reasoning-timeline` endpoint that computes:

- **Snapshots** — one per observation, showing the state of thinking at that
  moment (root gap, evidence, strategy, confidence)
- **Change detection** — each snapshot flags whether root gap, strategy, or
  confidence changed from the previous observation (3 boolean diffs)
- **Current summary** — case-level root gap, strategy, and status

Frontend: `ReasoningTimeline` component renders a vertical timeline with:
- Numbered steps with date markers
- Amber dots for observations where the hypothesis shifted
- "Hypothesis shifted" / "Strategy revised" labels
- Colored confidence badges (red=low, amber=medium, green=high)
- Colored evidence strength badges (blue=direct, purple=inference, teal=test)
- Alternative hypotheses in amber callout boxes
- Summary bar at top showing current case state

Files: `apps/api/app/routers/learning_cases.py` (new endpoint),
`apps/api/app/schemas.py` (ReasoningSnapshot + ReasoningTimeline models),
`apps/web/app/learning-cases/[id]/ReasoningTimeline.tsx` (new component),
`apps/web/app/learning-cases/[id]/page.tsx` (integrated)

### 3.2 Confidence Tracking ✅

New `confidence` column on observations:
- `low` — "I'm guessing"
- `medium` — "Plausible but not certain"
- `high` — "Strong evidence supports this"

Stored as a simple string in the database. Displayed as a colored badge in the
timeline and observation list. The timeline tracks `confidence_changed` across
observations.

Files: `apps/api/app/models.py`, `apps/api/app/schemas.py`,
`apps/api/app/routers/observations.py`,
`apps/web/app/learning-cases/[id]/NewObservationForm.tsx`

### 3.3 Alternative Hypotheses ✅

New `alternative_hypotheses` column on observations — a JSON array of strings.
The teacher can record "what else could explain this?" alongside their primary
hypothesis. Frontend provides an inline add/remove UI:

- Type a hypothesis → press Enter or click "Add"
- Chips appear as amber tags
- Click ✕ to remove
- Stored as `'["gap A","gap B"]'` in the database

Files: same as 3.2, plus the dynamic list UI in the form

### 3.4 Evidence Strength Tagging ✅

New `evidence_strength` column on observations:
- `direct_observation` — "I saw this happen"
- `inference` — "I'm drawing a conclusion from what I saw"
- `test_result` — "A formal assessment confirms this"

Displayed as a colored badge (blue/purple/teal) in the timeline and observation
list.

Files: same as 3.2

## Frontend Improvements

- Case detail page now shows the Reasoning Timeline as the primary view
- Raw observation list moved to a collapsible `<details>` section
- Observation form expanded with 4 new fields: evidence strength (dropdown),
  confidence (dropdown with descriptions), alternative hypotheses (add/remove
  chips), plus the existing LDG picker
- Timeline shows the full arc of teacher thinking — not just a flat list

## Test Results

| Suite | Count | Status |
|-------|-------|--------|
| Domain (Vitest) | 46 | ✅ |
| API (pytest) | 15 | ✅ |
| Knowledge (pytest) | 11 | ✅ |
| Reasoning (pytest) | 5 | ✅ |
| **Total** | **77** | **✅** |
| TypeScript | — | ✅ clean |

## Design Decisions

- **Observations don't auto-update the case.** The teacher must deliberately
  update the case (via PATCH) when their thinking changes. The timeline shows
  the gap between case state and observation evolution — this is intentional.
- **Confidence is a simple string, not a float.** Teachers think in qualitative
  terms (low/medium/high), not percentages. The reasoning-engine.md confirms
  this.
- **Alternative hypotheses stored as JSON.** Simple, queryable if needed, and
  avoids adding a 4th table. Three tables remain.
- **Evidence strength is separate from evidence.** The evidence text is the
  narrative; evidence_strength is the classification. Both matter for
  understanding the teacher's reasoning.

## Files Modified/Created

### Backend
| File | Change |
|------|--------|
| `app/models.py` | +3 columns on ObservationModel |
| `app/schemas.py` | Updated all observation schemas, added ReasoningSnapshot/Timeline |
| `app/routers/observations.py` | New field handling, shared `_apply_payload` helper |
| `app/routers/learning_cases.py` | New reasoning-timeline endpoint |
| `app/routers/students.py` | Pass new fields through timeline entries |
| `tests/test_reasoning.py` | 5 new tests |

### Frontend
| File | Change |
|------|--------|
| `lib/api.ts` | Added reasoning types and `getReasoningTimeline` method |
| `app/learning-cases/[id]/ReasoningTimeline.tsx` | New component — full timeline UI |
| `app/learning-cases/[id]/page.tsx` | Integrated timeline, collapsible observation list |
| `app/learning-cases/[id]/NewObservationForm.tsx` | +4 reasoning fields with UI |

## Next Phase (gated on ADR-002)

Phase 4: Application Layer — Expanded Notebook:
- Case review/reflection page
- Print/Export case as PDF
- Bulk student import
- Subject-specific templates from LDG

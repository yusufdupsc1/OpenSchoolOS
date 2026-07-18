# API

Backend service for Sprint 001. Serves the educational domain defined in
`packages/domain`. Supports the Educational Case Notebook workflow:

Student → Create Learning Case → Record Observation → Identify Root Gap →
Choose Intervention → Review → Close Case.

Local-first. No required external cloud dependency.

## Data (v0)

Persists exactly three tables — `students`, `learning_cases`, `observations`
(see `.ai/data-model.md`). No other tables for v0.

## Run

From the repo root:

```
npm install        # install workspace deps (builds better-sqlite3)
npm run seed       # Step 3-5: create Naim, his case, and one observation
npm run retrieve   # read everything back and print it
```

The database is a local embedded SQLite file (`apps/api/openschoolos.db`),
excluded from git. No server, no cloud.


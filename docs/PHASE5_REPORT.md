# Phase 5: Platform Layer

Date: 2026-08-04

## Summary

Built the platform infrastructure: authentication with JWT, multi-teacher data
scoping, enriched health dashboard, data export, and backup/restore. This
transforms OpenSchoolOS from a single-user prototype into a deployable
multi-teacher platform.

## What Changed

### 5.4 Authentication ✅

- **User model** — `users` table with email, full_name, hashed_password (bcrypt),
  is_active, created_at, deleted_at
- **JWT tokens** — HS256-signed, 24-hour expiry, configurable secret
- **Register** — `POST /auth/register` returns token + user
- **Login** — `POST /auth/login` validates credentials, returns token
- **Me** — `GET /auth/me` returns current user (requires auth)
- **Auth dependency** — `require_user` (401 if no token), `optional_user`
  (returns None if no token)
- **Frontend** — Login/register page at `/login`, auth header with sign-in/sign-out,
  token stored in localStorage, sent on all API requests

Files: `apps/api/app/auth.py` (new), `apps/api/app/routers/auth.py` (new),
`apps/api/app/models.py` (+UserModel), `apps/api/app/config.py` (+JWT settings),
`apps/web/app/login/page.tsx` (new), `apps/web/app/AuthHeader.tsx` (new),
`apps/web/app/layout.tsx` (updated), `apps/web/lib/api.ts` (auth headers, login/register methods)

### 5.5 Multi-Teacher Support ✅

- **teacher_id** nullable FK on `students` → `users.id`
- **Auto-assignment** — creating a student while authenticated auto-assigns
  teacher_id to current user
- **Query scoping** — `GET /students` filters by teacher_id when authenticated
- **Cross-tenant protection** — `POST /learning-cases` rejects if the student
  belongs to a different teacher (403)
- **No auth fallback** — when no token is present, everything works as before
  (all students visible)
- **CSV import** — imported students auto-assigned to the importing teacher

Files: `apps/api/app/models.py` (+teacher_id on StudentModel),
`apps/api/app/routers/students.py` (scoping + auto-assign),
`apps/api/app/routers/learning_cases.py` (ownership check + scoping)

### 5.1 Health Dashboard ✅

- `GET /health` now returns rich dashboard: status, db connection, counts for
  students, cases, observations, and users
- Graceful degradation: reports `db: "disconnected"` if DB is unavailable
- Frontend API: `api.getHealth()`

Files: `apps/api/app/routers/platform.py` (health endpoint),
`apps/api/app/schemas.py` (+HealthStatus)

### 5.3 Backup/Restore ✅

- `GET /backup` — downloads complete JSON backup including users (with hashed
  passwords), students, cases, observations
- `POST /restore` — uploads a backup file, clears all data, and restores from
  the file
- Version-tagged backups (v1.0)
- All datetime fields properly serialized/deserialized

Files: `apps/api/app/routers/platform.py`

### 5.2 Data Export ✅

- `GET /export` — exports all non-deleted data (students, cases, observations)
  as structured JSON
- Suitable for migration, reporting, or external analysis

Files: `apps/api/app/routers/platform.py`, `apps/api/app/schemas.py` (+DataExport)

## Test Results

| Suite | Count | Status |
|-------|-------|--------|
| Domain (Vitest) | 46 | ✅ |
| API | 15 | ✅ |
| Knowledge | 11 | ✅ |
| Reasoning | 5 | ✅ |
| Auth | 9 | ✅ |
| Platform | 5 | ✅ |
| **Total** | **91** | **✅** |

## Architecture Decisions

- **JWT over sessions** — Stateless, no server-side session store needed. Fits
  the "run on modest hardware" goal.
- **Nullable teacher_id** — Allows unauthenticated use for development and
  testing. When null, all data is visible.
- **bcrypt 4.0.1** — Pinned to avoid passlib compatibility issues with newer
  bcrypt.
- **Backup includes passwords** — Hashes are included so restore works. In
  production, backup files should be stored securely.
- **CORS wide open** — `allow_origins=["*"]` for development. Production should
  restrict this.

## Impact on Existing Features

- **Backward compatible** — All existing endpoints work without auth tokens
- **Progressive** — Adding auth scoping only activates when a token is present
- **No breaking changes** — StudentOut now includes `teacher_id` (nullable)

## Next Phase (gated on ADR-002)

Phase 6: Research Layer — case outcome tracking, time-to-close metrics,
intervention effectiveness, teacher reflection journal.

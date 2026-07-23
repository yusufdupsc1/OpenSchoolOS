# Project Index

The table of contents for the entire OpenSchoolOS repository. Every other
navigational question funnels through here.

This is a documentation artifact. It does not add educational functionality and
touches no domain model. It exists to keep the project legible to the Founder and
any AI agent, consistent with the Engineering Playbook (`.ai/playbook.md` §7–§8).

---

## Where is the latest architecture?

- **Authoritative architecture:** `.ai/architecture.md` — repository shape,
  boundaries, data flow, and the v0 data model (three tables).
- **Root layout:** `README.md` — the repository structure and authority order.
- **Boundaries / data flow diagram:** `.ai/architecture.md` §Boundaries.
- **Governing authority (root):** `.ai/README.md` — the constitutional brain; the
  order of authority is `README → constitution → philosophy → educational-principles
  → domain → architecture → coding-rules → implementation`.

Note: the three-aggregate / three-table model is frozen for v0 (no dashboard,
analytics, AI guessing, or recommendation engine). See *Which decisions are
frozen?* below.

---

## Which chat owns implementation?

This chat (the Founding Principal Software Engineer / Kilo as implementation
engineer).

- **Role:** implementation engineer, not general assistant, not CTO.
- **Authority:** ADR-006 — Kilo as Implementation Engineer; ADR-007 — the CTO
  Rule.
- **Operating protocol:** start at `.ai/session-start.md`, adopt the A00 System
  Prompt (`.ai/prompts/A00-System.md`), route tasks to the matching workflow in
  `.ai/workflows/`, and pass every change through the pipeline
  (`.ai/development-pipeline.md`).
- **Limits:** Kilo implements, refactors, reviews, and tests. It does NOT choose
  frameworks, rename domain concepts, change project structure, introduce new
  technologies, or alter educational workflows. Those require explicit Founder
  instruction. If a task appears to need an architectural decision, Kilo surfaces
  it and stops (ADR-007, ADR-009).

---

## Which chat owns educational research?

The Founder (CTO) owns educational research, strategic direction, scope, and the
classroom-case challenge.

- **Constitution AI RULE:** never invent educational theories, never create
  assumptions, always request evidence. If uncertain, create extension points, not
  fake intelligence.
- **Research prompts / workflows:** `.ai/prompts/A10-Research.md` and
  `.ai/workflows/research.md` — executed under the Founder's direction, not
  independently invented by the implementation chat.
- **Knowledge curation:** `knowledge/` — curated educational knowledge only,
  updated via `.ai/workflows/knowledge-update.md`.
- **Open research question (active):** "What did using the Notebook for a week
  teach us?" — see `.ai/session-start.md` and `.ai/roadmap.md` (the Week
  Question). This is the gate before any feature expansion.

---

## Which decisions are frozen?

Frozen = Accepted ADRs in `.ai/decision-log.md` plus the constitutional red lines.

- **ADR-001** — Sprint 001 scope: Educational Case Notebook only.
- **ADR-002** — No expansion before the week-of-use question is answered.
- **ADR-003** — Every feature challenged by THE CLASSROOM-CASE QUESTION; NO →
  `ideas.md`.
- **ADR-004** — AI Development Pipeline & Engineering Playbook are the process.
- **ADR-005** — The Educational Case Notebook is the first irreversible workflow.
- **ADR-006** — Kilo as implementation engineer.
- **ADR-007** — CTO Rule: Kilo makes no architectural decisions.
- **ADR-008** — Sprint cadence: SYNC → AUDIT → NORMALIZE → FREEZE → IMPLEMENT →
  REVIEW → COMMIT.
- **ADR-009** — Pre-implementation existence check (no duplication / no unapproved
  patterns).

Constitutional red lines (`.ai/constitution.md`), never to be crossed:

- Pedagogy drives software; software never drives pedagogy.
- Three aggregates / three tables only for v0: **Student, LearningCase,
  Observation**. Intervention is part of a LearningCase, not a separate model.
- No dashboards, analytics, AI guessing, or recommendation engines.
- NON GOALS are off-limits: attendance, payroll, inventory, accounting, exam
  management, ERP, parent billing, chat, generic AI chatbot.

---

## Which sprint is active?

**Sprint 001 — Educational Case Notebook.**

- **Goal:** the smallest honest slice that helps one teacher make one better
  decision for one learner.
- **Workflow:** `Student → Create Learning Case → Record Observation → Identify
  Root Gap → Choose Intervention → Review → Close Case`.
- **Three pages in `apps/web`:** Students (search/click), Learning Cases (active
  struggles), New Observation (five fields: Observed, Possible Root Gap, Evidence,
  Strategy, Next Review).
- **State:** skeleton in place; SQLAlchemy models still TODO per the pipeline
  (see `.ai/session-start.md`).
- **Source of truth:** `.ai/session-start.md` (Today's Goal / Current Sprint).

---

## What's the next milestone?

**Validate the Educational Loop with one teacher, one learner.**

1. Finish Sprint 001 implementation (the three pages + FastAPI/PostgreSQL
   persistence of the three aggregates) — `apps/api`, `apps/web`,
   `packages/domain`.
2. Validate via FastAPI endpoints / pytest against the PostgreSQL dev database once
   the SQLAlchemy models exist (`.ai/development-pipeline.md` §Validate).
3. Ask the Week Question after a week of real use: "What did using this for a week
   teach us?" (`ADR-002`, `.ai/roadmap.md`).
   - "Nothing" → redesign.
   - "It changed how I think about students" → only then expand up the layer
     stack (`.ai/roadmap.md`).

No expansion before that question is answered honestly.

---

## Quick file map

| Need | File |
| --- | --- |
| Constitution (supreme authority) | `.ai/constitution.md` |
| Root authority & layout | `README.md` |
| AI operating brain | `.ai/README.md` |
| Session bootstrap | `.ai/session-start.md` |
| Architecture | `.ai/architecture.md` |
| Domain model | `.ai/domain.md`, `packages/domain` |
| Data model (v0 tables) | `.ai/data-model.md` |
| Engineering Playbook | `.ai/playbook.md` |
| Development pipeline | `.ai/development-pipeline.md` |
| Decision log (frozen ADRs) | `.ai/decision-log.md` |
| Roadmap & next milestone | `.ai/roadmap.md` |
| Unvalidated wants (graveyard) | `.ai/ideas.md` |
| Prompt catalog | `.ai/prompts/` (A00–A90) |
| Reusable workflows | `.ai/workflows/` |
| Founder's manual | `FOUNDERS_AI_OPERATING_MANUAL.md` |

# Decision Log

Architectural and process decisions for OpenSchoolOS, recorded as **Architectural
Decision Records (ADRs)**. This is the "every decision is recorded" mechanism of
the Engineering Playbook (`.ai/playbook.md` §6).

## ADR Convention

```
## ADR-<n> — <short title>
Date: <YYYY-MM-DD>
Status: Proposed | Accepted | Superseded by ADR-<m>
Decision: <what we decided>
Context: <classroom case / problem that triggered it>
Consequences: <what changes, what we give up>
Authority: <which .ai doc this aligns with>
```

Rules: no architectural change is "done" until its ADR exists; an ADR cites the
real classroom case or research that justified it; superseded ADRs are kept with
a pointer to the replacement.

---

## ADR-001 — Sprint 001 scope and first build target

Date: 2026-07-18
Status: Accepted
Decision: Sprint 001 builds only the **Educational Case Notebook** — a single
linear workflow:

```
Student → Create Learning Case → Record Observation →
Identify Root Gap → Choose Intervention → Review → Close Case
```

Repository layout for Sprint 001:

```
apps/web      # Educational Case Notebook front end
apps/api      # Backend serving the educational domain
packages/domain  # Shared, framework-free domain model
knowledge/    # Curated educational knowledge (LDG subject graphs)
.ai/          # Constitutional brain
docs/         # Documentation
```

Context: The smallest piece of software that makes one teacher (Yusuf) better
tomorrow is a notebook for one worried student — not a dashboard, not analytics,
not AI.
Consequences: We do not build for thousands of schools until we help one
classroom tomorrow.
Authority: Aligns with constitution.md (Definition of Done, NON GOALS,
DOMAIN FIRST, VALIDATION BEFORE EXPANSION) and the root README.md.

## ADR-002 — What happens after a week of use

Date: 2026-07-18
Status: Accepted
Decision: Only after a teacher has used the Notebook for a week do we ask "What
did using this for a week teach us?" If "nothing," we change the design. If "it
changed how I think about students," we have found something worth expanding. No
expansion before that question is answered.
Context: This is the Reflect step of the Educational Loop made explicit, and the
gate before any feature growth.
Consequences: Feature expansion is paused until validated by real use.
Authority: Aligns with educational-loop.md (After a Week of Use),
constitution.md (VALIDATION BEFORE EXPANSION, Definition of Done), and the
GitHub goal in README.md.

## ADR-003 — The classroom-case challenge

Date: 2026-07-18
Status: Accepted
Decision: Every feature request — including our own — is challenged with "Can
you point to a real classroom case that justifies this?" YES → build it. NO →
write to ideas.md and move on. ideas.md is a graveyard of unvalidated wants, not
a backlog.
Context: Prevents scope creep from unvalidated wants.
Consequences: Unvalidated ideas accumulate in ideas.md instead of the codebase.
Authority: Aligns with constitution.md (THE CLASSROOM-CASE QUESTION, VALIDATION
BEFORE EXPANSION).

## ADR-004 — AI Development Pipeline & Engineering Playbook

Date: 2026-07-18
Status: Accepted
Decision: Every coding task passes through the disciplined pipeline
(Think → Research → Model → Review → Implement → Refactor → Validate →
Document). Prompts are identified A00–A90 in `.ai/prompts/`; task types route to
reusable workflows in `.ai/workflows/`; every session starts at
`.ai/session-start.md`; decisions are recorded as ADRs here. This is the
Engineering Playbook (`.ai/playbook.md`).
Context: Replaces random prompting with a repeatable, tool-agnostic process so
the mission survives contributor and tool changes.
Consequences: No session starts from a blank prompt; no decision ships without
an ADR.
Authority: Aligns with development-pipeline.md, prompts/*, workflows/*,
session-start.md, and constitution.md.

## ADR-005 — The First Irreversible Educational Workflow

Date: 2026-07-18
Status: Accepted
Decision: OpenSchoolOS's mission is to build the first irreversible educational
workflow — the Educational Case Notebook:
Student → Create Learning Case → Record Observation → Identify Root Gap →
Choose Intervention → Review → Close Case. It is irreversible because opening a
case for a real child and writing the first observation is a commitment that
changes the teacher, not just the database; the loop (Observe → Think → Act →
Reflect → Observe Again) makes closing one case open the next.
Context: Stated as the mission; distinguishes the work from OpenSchoolOS-as-
product, AI, or dashboards.
Consequences: No future feature may weaken the centrality of this workflow. The
constitution, three aggregates, pipeline, playbook, and ADRs exist only to
protect it from dilution into a dashboard, an AI, or a school-management system.
Authority: Aligns with educational-loop.md, constitution.md (Definition of
Done, DOMAIN FIRST), and the GitHub goal.

## ADR-006 — Kilo as Implementation Engineer

Date: 2026-07-18
Status: Accepted
Decision: From this point, Kilo Code operates as an implementation engineer, not
a general assistant. It executes the Engineering Playbook (playbook.md): starts
at session-start.md, adopts the A00 System Prompt, routes tasks to the matching
workflow, and passes every change through the disciplined pipeline. Strategic
direction, scope, and the classroom-case challenge remain the Founder's; Kilo
implements within those bounds.
Context: The playbook and prompt catalog are now in place; the role shift makes
the process operational rather than advisory.
Consequences: Kilo builds and verifies slices (e.g. npm run seed / retrieve); it
does not expand scope, invent features, or bypass ADRs. Constitutional red lines
(A00 rules, anti-patterns.md) are enforced even against Founder requests.
Authority: Aligns with playbook.md, FOUNDERS_AI_OPERATING_MANUAL.md,
prompts/A00-System.md, and constitution.md.

> Erratum: the line above references "npm run seed / retrieve", which described the early Node/SQLite prototype. That slice was removed; the current stack is FastAPI + PostgreSQL (see tech-stack.md). Validation now uses pytest/FastAPI endpoints once SQLAlchemy models exist.

## ADR-007 — CTO Rule: Kilo makes no architectural decisions

Date: 2026-07-18
Status: Accepted
Decision: Kilo is forbidden from making architectural decisions. It may
implement, refactor, review, and test. It may NOT choose frameworks, rename
domain concepts, change project structure, introduce new technologies, or alter
educational workflows. Those decisions belong to the Founder (CTO). If a task
appears to require an architectural decision, Kilo surfaces it and stops.
Context: Sharpens ADR-006 (Kilo as implementation engineer) — execution within
the existing architecture, not reshaping it.
Consequences: Framework/structure/workflow changes require explicit Founder
instruction; Kilo escalates rather than decides.
Authority: Aligns with coding-rules.md (CTO Rule), playbook.md, ADR-006, and
constitution.md.

## ADR-008 — Sprint cadence: SYNC → AUDIT → NORMALIZE → FREEZE → IMPLEMENT → REVIEW → COMMIT

Date: 2026-07-18
Status: Accepted
Decision: Every sprint begins with this fixed sequence, and no stage is skipped:
SYNC (read everything, build mental model) → AUDIT (detect contradictions,
drift, violations) → NORMALIZE (minimum changes for consistency) → FREEZE
(lock decisions) → IMPLEMENT → REVIEW → COMMIT. SYNC is mandatory and must
never be skipped.
Context: The repository had drifted (truncated entry-point docs, orphaned
manifests) because work started without a sync/audit pass. A fixed cadence
prevents recurrence.
Consequences: No implementation begins before SYNC+AUDIT+NORMALIZE+FREEZE. The
Engineering Playbook and development-pipeline.md encode the stages.
Authority: Aligns with playbook.md, development-pipeline.md, coding-rules.md,
and constitution.md.

## ADR-009 — Pre-implementation existence check

Date: 2026-07-18
Status: Accepted
Decision: Before implementing any requested feature, Kilo MUST check whether the
functionality already exists in the repository. Never duplicate functionality;
never rename established educational concepts; never introduce a new architectural
pattern without explicit Founder approval. When uncertain, report — do not
implement.
Context: Prevents redundant code and concept drift as the codebase grows.
Consequences: Suspected duplicates/conflicts route back to SYNC/NORMALIZE;
uncertainty stops implementation and is surfaced to the Founder.
Authority: Aligns with ADR-008 (cadence), coding-rules.md (CTO Rule, dependency
justification), and constitution.md (DOMAIN FIRST).

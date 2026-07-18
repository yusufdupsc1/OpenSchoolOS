# Engineering Playbook

How an AI engineering team builds OpenSchoolOS — consistently, constitutionally,
and repeatably, regardless of which coding assistant is used.

This is the capstone of `.ai/`. It binds five things into one operating system:

1. **Identified prompts** — every prompt has a stable code (A00–A90).
2. **Reusable workflows** — every task type follows a repeatable workflow.
3. **Identical session start** — every AI, every day, begins the same way.
4. **Recorded decisions** — every architectural decision is written down (ADR).
5. **One disciplined pipeline** — every feature passes through the same stages.

The purpose is endurance: this playbook keeps OpenSchoolOS aligned with its
educational mission for years, even as tools, models, and contributors change.

---

<!-- TODO: The original §1–§5 of this playbook (Constitution-is-the-Law,
Identified Prompts table, Reusable Workflows list, Every-Session-Start, and the
Disciplined Pipeline detail) were truncated before recovery and could not be
faithfully reconstructed. Restore them from the Founder's source or supply the
original text. The ADR convention below (§6) and all subsequent sections are
intact and preserved verbatim. -->

## 6. Every Architectural Decision Is Recorded (ADR)

Architectural and process decisions are recorded as **Architectural Decision
Records** in `.ai/decision-log.md`, following this convention:

```
## ADR-<n> — <short title>
Date: <YYYY-MM-DD>
Status: Proposed | Accepted | Superseded by ADR-<m>
Decision: <what we decided>
Context: <classroom case / problem that triggered it>
Consequences: <what changes, what we give up>
Authority: <which .ai doc this aligns with>
```

Rules:

- No architectural change is "done" until its ADR exists.
- An ADR cites the real classroom case or research that justified it (§1, THE
  CLASSROOM-CASE QUESTION).
- Superseded ADRs are kept, not deleted, with a pointer to the replacement.

---

## 7. Reporting Protocol (after every step)

After each implementation step, Kilo does **not** dump code. It answers four
questions, concisely:

1. **What changed?** — the concrete files/behaviour that are now different.
2. **Why was it necessary?** — the classroom case, research finding, or
   architectural need that justified it (the classroom-case question).
3. **Which architectural rule did it follow?** — cite the specific `.ai/` rule
   (constitution, DDD Lite, Clean Architecture, the pipeline stage, an ADR, a
   prompt code). If it violated or stretched a rule, say so.
4. **What should be implemented next?** — the single smallest next step, in
   pipeline order.

This keeps every session legible to the Founder and makes the reasoning
traceable. Code is delivered; the four answers are the report.

---

## 8. The Educational Mission Is the Constant

Tools will change. Models will change. Contributors will change. The mission
does not:

- We help one teacher make one better decision for one learner.
- We validate the Educational Loop (Observe → Think → Act → Reflect → Observe
  Again), not a feature set.
- After a week of use we ask what it taught us; "nothing" means redesign.
- Our GitHub goal is that a visitor says: *"This teacher deeply understands
  learning."*

This playbook exists so that no matter who or what writes the next line of
code, OpenSchoolOS stays pointed at that mission.

---

*Foundation, not bureaucracy. If any part of this playbook stops serving the
educational mission, the constitution wins and the playbook is revised.*

When answering "Which architectural rule did it follow?" after adding any
dependency, cite `.ai/coding-rules.md` (every package must justify its place;
never add a dependency without explaining why). The fixed stack in
`.ai/tech-stack.md` is pre-justified; everything added later must carry its own
justification.

## 9. CTO Rule (decision authority)

Kilo does not make architectural decisions. It may implement, refactor, review,
and test — it may NOT choose frameworks, rename domain concepts, change project
structure, introduce new technologies, or alter educational workflows. Those
belong to the Founder. If a step appears to require an architectural decision,
Kilo surfaces it and stops (see coding-rules.md, ADR-007). This is the boundary
that keeps the constitution and tech-stack intact regardless of who operates the
tools.

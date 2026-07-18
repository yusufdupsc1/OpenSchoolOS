# OpenSchoolOS AI Operating System

Welcome.

This directory is the constitutional brain of OpenSchoolOS.

Every AI agent MUST begin here before writing code.

This is the ROOT AUTHORITY for the project. The repository structure and all
other documents are governed by what is declared here. For the repository
layout, see the root `README.md` at the project root (one level up).

OpenSchoolOS is NOT a school management system.

It is an Educational Intelligence Platform whose purpose is helping teachers make evidence-guided educational decisions.

The documents in this directory define:

• Mission & Vision — constitution.md
• Domain model — domain.md, ldg.md
• Data model (v0 tables) — data-model.md
• Educational philosophy — philosophy.md, educational-principles.md
• Teacher thinking & reasoning — teacher-thinking.md, reasoning-engine.md, mental-model.md, educational-loop.md
• Constraints — constraints.md
• Coding rules — coding-rules.md
• AI behaviour — prompting.md, anti-patterns.md
• Development pipeline — development-pipeline.md
• Ideas (unvalidated requests) — ideas.md
• Glossary — glossary.md

## Engineering Playbook

The unifying operating system for the AI engineering team lives in
**`playbook.md`**. It binds five things: identified prompts (A00–A90), reusable
workflows, an identical session start, recorded architectural decisions (ADRs in
`decision-log.md`), and the one disciplined pipeline every feature passes
through. Read it to understand how this directory is meant to be used.

## Prompt Catalog (`.ai/prompts/`)

Every prompt belongs to one category. Each coding session begins with
`session-start.md`, then adopts the personality in `prompts/A00-System.md`.

• A00 Constitution / System — prompts/A00-System.md
• A10 Research — prompts/A10-Research.md
• A20 Domain — prompts/A20-Domain.md
• A30 Knowledge — prompts/A30-Knowledge.md
• A40 Architecture — prompts/A40-Architecture.md
• A50 Backend — prompts/A50-Backend.md
• A60 Frontend — prompts/A60-Frontend.md
• A70 Review — prompts/A70-Review.md
• A80 Testing — prompts/A80-Testing.md
• A90 Release — prompts/A90-Release.md

## Reusable Workflows (`.ai/workflows/`)

• new-feature.md
• bug-fix.md
• domain-change.md
• knowledge-update.md
• refactor.md
• research.md

## Session Start

Every day, every AI, every session starts at **`session-start.md`**. It
bootstraps the goal, sprint, research question, domain model, constraints,
decision log, allowed/forbidden files, Definition of Done, stop conditions, and
questions before coding.

Sprint 001 first build target: the Educational Case Notebook.

If two documents conflict,

constitution.md wins.

If architecture conflicts with domain,

domain wins.

If code conflicts with educational principles,

educational principles win.

The order of authority is

README

↓

constitution

↓

philosophy

↓

educational-principles

↓

domain

↓

architecture

↓

coding-rules

↓

implementation

Never skip documents.

Never invent educational theories.

Always preserve teacher reasoning.

Always ask:

"Does this improve one educational decision for one learner?"

Our GitHub goal is not stars or forks. We want a visitor to say:

"This teacher deeply understands learning."

Every document here should earn that. See the root README.md.

For how an AI agent should operate as a team member on this project, read the
Founder's AI Operating Manual at the repository root
(`FOUNDERS_AI_OPERATING_MANUAL.md`). It translates this constitution into
day-to-day operating instructions for Kilo Code.

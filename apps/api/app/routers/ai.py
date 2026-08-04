# OpenSchoolOS API — AI Extension Points (Sprint 007).
"""Extension points that an AI agent or LLM could use — never fake intelligence.
All endpoints return structured data for teacher review; nothing is auto-applied."""
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select, func as safunc
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import LearningCaseModel, ObservationModel, StudentModel
from app.schemas import (
    AutocompleteResult, ObservationSummary, SimilarCaseEntry, SimilarCasesResult,
)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/similar-cases/{case_id}", response_model=SimilarCasesResult)
def similar_cases(
    case_id: str,
    max_results: int = Query(default=10, ge=1, le=50),
    session: Session = Depends(get_session),
):
    """Find cases similar to this one: same root gap, same subject, or same strategy."""
    source = session.get(LearningCaseModel, case_id)
    if source is None or source.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Case not found.")

    # Find cases that match on root gap, subject, or strategy (excluding self)
    candidates = session.scalars(
        select(LearningCaseModel)
        .where(
            LearningCaseModel.deleted_at.is_(None),
            LearningCaseModel.id != case_id,
            or_(
                LearningCaseModel.possible_root_gap == source.possible_root_gap,
                LearningCaseModel.subject == source.subject,
                LearningCaseModel.strategy == source.strategy,
            ),
        )
        .order_by(LearningCaseModel.created_at.desc())
        .limit(max_results)
    ).all()

    results: list[SimilarCaseEntry] = []
    for c in candidates:
        # Determine similarity type
        if c.possible_root_gap == source.possible_root_gap:
            sim = "same_root_gap"
        elif c.strategy == source.strategy:
            sim = "same_strategy"
        else:
            sim = "same_subject"

        obs_count = session.scalar(
            select(safunc.count(ObservationModel.id)).where(
                ObservationModel.learning_case_id == c.id,
                ObservationModel.deleted_at.is_(None),
            )
        ) or 0

        results.append(SimilarCaseEntry(
            case_id=c.id, student_id=c.student_id,
            student_name=c.student.full_name if c.student else "Unknown",
            subject=c.subject, competency=c.competency,
            possible_root_gap=c.possible_root_gap, strategy=c.strategy,
            status=c.status, outcome=c.outcome, similarity=sim,
            observation_count=obs_count,
        ))

    return SimilarCasesResult(
        source_case_id=case_id,
        source_root_gap=source.possible_root_gap,
        source_subject=source.subject,
        results=results,
    )


@router.get("/observation-summary/{case_id}", response_model=ObservationSummary)
def observation_summary(
    case_id: str, session: Session = Depends(get_session),
):
    """Packages a case's observations into a structured summary — an extension
    point for external AI. Includes a simple heuristic summary (no LLM)."""
    lc = session.get(LearningCaseModel, case_id)
    if lc is None or lc.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Case not found.")

    obs_rows = session.scalars(
        select(ObservationModel)
        .where(ObservationModel.learning_case_id == case_id, ObservationModel.deleted_at.is_(None))
        .order_by(ObservationModel.created_at)
    ).all()

    root_gap_prog = [o.possible_root_gap for o in obs_rows]
    strategy_prog = [o.strategy for o in obs_rows]
    confidence_prog = [o.confidence for o in obs_rows]

    latest = obs_rows[-1].observed if obs_rows else None

    # Heuristic summary — no AI, just structured concatenation
    parts = [f"Case for {lc.student.full_name}: {lc.subject} — {lc.competency}."]
    if root_gap_prog:
        unique_gaps = list(dict.fromkeys(root_gap_prog))  # deduplicate keeping order
        parts.append(f"Root gap evolved: {' → '.join(unique_gaps)}.")
    if strategy_prog:
        unique_strats = list(dict.fromkeys(strategy_prog))
        parts.append(f"Strategy evolved: {' → '.join(unique_strats)}.")
    if confidence_prog:
        confs = [c for c in confidence_prog if c]
        if confs:
            parts.append(f"Confidence ranged: {confs[0]} → {confs[-1]}.")
    if latest:
        parts.append(f"Latest observation: '{latest}'.")
    if lc.outcome:
        parts.append(f"Outcome: {lc.outcome}.")
    if lc.reflection:
        parts.append(f"Teacher reflection: {lc.reflection}")

    heuristic = " ".join(parts)

    # Raw context for external AI
    raw_lines = [f"CASE: {lc.subject} — {lc.competency}"]
    raw_lines.append(f"Student: {lc.student.full_name} (Grade {lc.student.grade}{lc.student.section})")
    raw_lines.append(f"Root Gap: {lc.possible_root_gap}")
    raw_lines.append(f"Evidence: {lc.evidence}")
    raw_lines.append(f"Strategy: {lc.strategy}")
    raw_lines.append("")
    for i, o in enumerate(obs_rows):
        raw_lines.append(f"OBSERVATION {i+1}:")
        raw_lines.append(f"  Observed: {o.observed}")
        raw_lines.append(f"  Root Gap: {o.possible_root_gap}")
        raw_lines.append(f"  Evidence: {o.evidence} ({o.evidence_strength or 'unspecified'})")
        raw_lines.append(f"  Strategy: {o.strategy}")
        raw_lines.append(f"  Confidence: {o.confidence or 'unspecified'}")
        if o.alternative_hypotheses:
            raw_lines.append(f"  Alternatives: {o.alternative_hypotheses}")
        raw_lines.append("")

    return ObservationSummary(
        case_id=lc.id, subject=lc.subject, competency=lc.competency,
        student_name=lc.student.full_name,
        observation_count=len(obs_rows),
        root_gap_progression=root_gap_prog,
        strategy_progression=strategy_prog,
        confidence_progression=confidence_prog,
        latest_observation=latest,
        heuristic_summary=heuristic,
        raw_context="\n".join(raw_lines),
    )


@router.get("/autocomplete", response_model=AutocompleteResult)
def autocomplete(
    q: str = Query(min_length=2),
    source: str = Query(default="all", pattern="^(ldg|past_cases|all)$"),
    session: Session = Depends(get_session),
):
    """Autocomplete root gaps from past cases and LDG knowledge.

    This is an extension point — returns matching strings that a teacher
    can choose from, never auto-applies them.
    """
    matches: list[str] = []
    match_source = "ldg"

    if source in ("ldg", "all"):
        # Search LDG knowledge files
        from pathlib import Path
        import json as _json
        knowledge_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / "knowledge"
        ql = q.lower()
        for fpath in knowledge_dir.glob("*.json"):
            try:
                data = _json.loads(fpath.read_text())
                for comp in data.get("competencies", []):
                    if ql in comp["label"].lower() or ql in comp.get("description", "").lower():
                        matches.append(comp["label"])
                    for m in comp.get("misconceptions", []):
                        if ql in m.get("rootGap", "").lower():
                            val = m["rootGap"]
                            if val not in matches:
                                matches.append(val)
            except Exception:
                continue

    if source in ("past_cases", "all"):
        # Search past case root gaps
        pattern = f"%{q}%"
        rows = session.scalars(
            select(LearningCaseModel.possible_root_gap)
            .where(
                LearningCaseModel.deleted_at.is_(None),
                LearningCaseModel.possible_root_gap.ilike(pattern),
            )
            .distinct()
            .limit(10)
        ).all()
        for r in rows:
            if r not in matches:
                matches.append(r)
        if source == "past_cases":
            match_source = "past_cases"
        else:
            match_source = "all"

    return AutocompleteResult(matches=matches[:15], source=match_source)

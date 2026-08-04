# OpenSchoolOS API — Research / Analytics routes (Sprint 006).
"""Measure whether cases improve learning — the research layer."""
import statistics
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, func as safunc
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import LearningCaseModel, ObservationModel, StudentModel
from app.schemas import (
    DurationMetrics, DurationReport, OutcomeBreakdown, ResearchDashboard,
    StrategyEffectiveness,
)

router = APIRouter(prefix="/research", tags=["research"])


def _days_between(start, end):
    """Duration in days between two datetimes or ISO strings."""
    if start is None or end is None:
        return None
    if isinstance(start, str):
        start = datetime.fromisoformat(start)
    if isinstance(end, str):
        end = datetime.fromisoformat(end)
    return (end - start).total_seconds() / 86400


def _compute_duration_metrics(label_key, rows):
    """Compute DurationMetrics for a labeled group of closed cases."""
    durations = [d for d in (_days_between(r.created_at, r.closed_at) for r in rows) if d is not None]
    if not durations:
        return DurationMetrics(group_key=label_key, group_label=label_key, count=0, avg_days=0, min_days=0, max_days=0, median_days=0)
    return DurationMetrics(
        group_key=label_key, group_label=label_key, count=len(durations),
        avg_days=round(sum(durations) / len(durations), 1),
        min_days=round(min(durations), 1), max_days=round(max(durations), 1),
        median_days=round(statistics.median(durations), 1),
    )


@router.get("/dashboard", response_model=ResearchDashboard)
def research_dashboard(session: Session = Depends(get_session)):
    """Full research dashboard: outcomes, durations, strategies, and more."""
    # All non-deleted cases
    all_cases = session.scalars(
        select(LearningCaseModel).where(LearningCaseModel.deleted_at.is_(None))
    ).all()

    total = len(all_cases)
    open_cases = sum(1 for c in all_cases if c.status == "open")
    closed_cases = sum(1 for c in all_cases if c.status == "closed")

    # Observations
    total_obs = session.scalar(
        select(safunc.count(ObservationModel.id)).where(ObservationModel.deleted_at.is_(None))
    ) or 0

    avg_obs = round(total_obs / total, 1) if total > 0 else 0

    # Outcomes
    outcome_counts: dict[str, int] = defaultdict(int)
    for c in all_cases:
        if c.status == "closed":
            outcome_counts[c.outcome or "unknown"] += 1
    outcomes = [OutcomeBreakdown(outcome=k, count=v) for k, v in sorted(outcome_counts.items())]

    # Duration by subject
    closed = [c for c in all_cases if c.status == "closed"]
    by_subject: dict[str, list] = defaultdict(list)
    by_grade: dict[str, list] = defaultdict(list)
    for c in closed:
        by_subject[c.subject].append(c)
        if c.student:
            by_grade[c.student.grade].append(c)

    duration = DurationReport(
        by_subject=[_compute_duration_metrics(s, cases) for s, cases in sorted(by_subject.items())],
        by_grade=[_compute_duration_metrics(g, cases) for g, cases in sorted(by_grade.items())],
        overall=_compute_duration_metrics("all", closed),
    )

    # Strategy effectiveness
    strategy_stats: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "improved": 0, "plateaued": 0, "worsened": 0, "unknown": 0})
    for c in all_cases:
        s = c.strategy[:80]  # truncate for grouping
        strategy_stats[s]["count"] += 1
        if c.status == "closed":
            o = c.outcome or "unknown"
            if o in strategy_stats[s]:
                strategy_stats[s][o] += 1

    top = sorted(strategy_stats.items(), key=lambda kv: kv[1]["count"], reverse=True)[:10]
    top_strategies = [
        StrategyEffectiveness(strategy=k, count=v["count"], improved=v["improved"],
                              plateaued=v["plateaued"], worsened=v["worsened"], unknown=v["unknown"])
        for k, v in top
    ]

    # Cases per subject
    subject_counts: dict[str, int] = defaultdict(int)
    for c in all_cases:
        subject_counts[c.subject] += 1
    cases_per_subject = [{"subject": s, "count": c} for s, c in sorted(subject_counts.items(), key=lambda x: -x[1])]

    return ResearchDashboard(
        total_cases=total, open_cases=open_cases, closed_cases=closed_cases,
        total_observations=total_obs, avg_observations_per_case=avg_obs,
        outcomes=outcomes, duration=duration,
        top_strategies=top_strategies, cases_per_subject=cases_per_subject,
    )

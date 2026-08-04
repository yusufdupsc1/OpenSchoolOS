# OpenSchoolOS API — LearningCase routes (Sprint 004).
import json as _json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import optional_user
from app.db import get_session
from app.models import LearningCaseModel, ObservationModel, StudentModel, UserModel
from app.schemas import (
    CloseCaseBody, LearningCaseCreate, LearningCaseOut, LearningCaseUpdate,
    ReasoningSnapshot, ReasoningTimeline, TransferCaseBody,
)

router = APIRouter(prefix="/learning-cases", tags=["learning-cases"])


def _to_out(r: LearningCaseModel) -> LearningCaseOut:
    return LearningCaseOut(
        id=r.id, student_id=r.student_id, subject=r.subject,
        competency=r.competency, possible_root_gap=r.possible_root_gap,
        evidence=r.evidence, strategy=r.strategy, next_review=r.next_review,
        status=r.status, reflection=r.reflection, outcome=r.outcome,
        closed_at=r.closed_at.isoformat() if r.closed_at else None,
        created_at=r.created_at.isoformat() if r.created_at else None,
        deleted_at=r.deleted_at.isoformat() if r.deleted_at else None,
    )


@router.post("", response_model=LearningCaseOut, status_code=status.HTTP_201_CREATED)
def create_learning_case(payload: LearningCaseCreate, session: Session = Depends(get_session), user: UserModel | None = Depends(optional_user)) -> LearningCaseOut:
    student = session.get(StudentModel, payload.student_id)
    if student is None or student.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    if user and student.teacher_id and student.teacher_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student does not belong to you.")
    model = LearningCaseModel(
        id=str(uuid.uuid4()), student_id=payload.student_id, subject=payload.subject,
        competency=payload.competency, possible_root_gap=payload.possible_root_gap,
        evidence=payload.evidence, strategy=payload.strategy, next_review=payload.next_review, status="open",
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.get("", response_model=list[LearningCaseOut])
def list_learning_cases(
    student_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    session: Session = Depends(get_session),
    user: UserModel | None = Depends(optional_user),
) -> list[LearningCaseOut]:
    stmt = select(LearningCaseModel).where(LearningCaseModel.deleted_at.is_(None))
    if student_id is not None: stmt = stmt.where(LearningCaseModel.student_id == student_id)
    if status is not None: stmt = stmt.where(LearningCaseModel.status == status)
    if user:
        stmt = stmt.join(LearningCaseModel.student).where(StudentModel.teacher_id == user.id)
    rows = session.scalars(stmt.order_by(LearningCaseModel.created_at)).all()
    return [_to_out(r) for r in rows]


@router.get("/{case_id}", response_model=LearningCaseOut)
def get_learning_case(case_id: str, session: Session = Depends(get_session)) -> LearningCaseOut:
    model = session.get(LearningCaseModel, case_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")
    return _to_out(model)


@router.patch("/{case_id}", response_model=LearningCaseOut)
def update_learning_case(case_id: str, payload: LearningCaseUpdate, session: Session = Depends(get_session)) -> LearningCaseOut:
    model = session.get(LearningCaseModel, case_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")
    if payload.subject is not None: model.subject = payload.subject
    if payload.competency is not None: model.competency = payload.competency
    if payload.possible_root_gap is not None: model.possible_root_gap = payload.possible_root_gap
    if payload.evidence is not None: model.evidence = payload.evidence
    if payload.strategy is not None: model.strategy = payload.strategy
    if payload.next_review is not None: model.next_review = payload.next_review
    if payload.reflection is not None: model.reflection = payload.reflection
    if payload.outcome is not None: model.outcome = payload.outcome
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.patch("/{case_id}/close", response_model=LearningCaseOut)
def close_learning_case(case_id: str, body: CloseCaseBody = CloseCaseBody(), session: Session = Depends(get_session)) -> LearningCaseOut:
    model = session.get(LearningCaseModel, case_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")
    model.status = "closed"
    model.closed_at = datetime.now(timezone.utc)
    if body.reflection is not None:
        model.reflection = body.reflection
    if body.outcome is not None:
        model.outcome = body.outcome
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.patch("/{case_id}/reopen", response_model=LearningCaseOut)
def reopen_learning_case(case_id: str, session: Session = Depends(get_session)) -> LearningCaseOut:
    model = session.get(LearningCaseModel, case_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")
    model.status = "open"
    model.closed_at = None
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.post("/{case_id}/transfer", response_model=LearningCaseOut)
def transfer_learning_case(case_id: str, body: TransferCaseBody, session: Session = Depends(get_session)) -> LearningCaseOut:
    model = session.get(LearningCaseModel, case_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")
    target = session.get(StudentModel, body.student_id)
    if target is None or target.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target student not found.")
    model.student_id = body.student_id
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning_case(case_id: str, session: Session = Depends(get_session)) -> None:
    model = session.get(LearningCaseModel, case_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")
    model.deleted_at = datetime.now(timezone.utc)
    session.commit()


@router.get("/{case_id}/print", response_class=HTMLResponse)
def print_case(case_id: str, session: Session = Depends(get_session)) -> HTMLResponse:
    lc = session.get(LearningCaseModel, case_id)
    if lc is None or lc.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")

    student = lc.student
    obs_rows = session.scalars(
        select(ObservationModel)
        .where(ObservationModel.learning_case_id == case_id, ObservationModel.deleted_at.is_(None))
        .order_by(ObservationModel.created_at)
    ).all()

    obs_html = ""
    for i, o in enumerate(obs_rows):
        conf = o.confidence or "—"
        strength = (o.evidence_strength or "").replace("_", " ")
        alts = ""
        if o.alternative_hypotheses:
            try:
                alt_list = _json.loads(o.alternative_hypotheses)
                alts = f'<div class="alts">Also considered: {" · ".join(alt_list)}</div>'
            except Exception:
                pass
        obs_html += f"""<tr><td>{i+1}</td><td>{o.observed}</td><td>{o.possible_root_gap}</td><td>{o.evidence}</td><td><span class="badge">{strength}</span></td><td>{o.strategy}</td><td><span class="badge">{conf}</span></td><td>{o.next_review}</td></tr>"""

    refl = ""
    if lc.reflection:
        refl = f'<div class="reflection"><strong>Teacher Reflection:</strong> {lc.reflection}</div>'

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Case: {lc.subject} — {lc.competency}</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:800px;margin:40px auto;padding:20px;color:#222;}}
h1{{font-size:1.5rem;margin-bottom:4px;}}
.meta{{color:#666;font-size:.875rem;margin-bottom:24px;}}
.card{{border:1px solid #ddd;border-radius:8px;padding:16px;margin-bottom:24px;}}
.card h3{{margin:0 0 8px 0;font-size:.75rem;text-transform:uppercase;color:#999;}}
.card p{{margin:4px 0;font-size:.9rem;}}
table{{width:100%;border-collapse:collapse;font-size:.85rem;}}
th{{background:#f5f5f5;text-align:left;padding:8px 6px;border-bottom:2px solid #ddd;}}
td{{padding:8px 6px;border-bottom:1px solid #eee;vertical-align:top;}}
.badge{{display:inline-block;padding:1px 6px;border-radius:4px;background:#f0f0f0;font-size:.75rem;}}
.alts{{margin-top:4px;font-size:.8rem;color:#b45309;background:#fef3c7;padding:4px 8px;border-radius:4px;}}
.reflection{{background:#f0fdf4;border-left:3px solid #22c55e;padding:12px 16px;margin-top:16px;font-style:italic;}}
@media print{{body{{margin:0;padding:0;}}}}
</style></head><body>
<h1>{lc.subject} — {lc.competency}</h1>
<p class="meta">Student: <strong>{student.full_name}</strong> · Grade {student.grade}{student.section} · Roll {student.roll_number} · Status: {lc.status}</p>
<div class="card"><h3>Case Details</h3>
<p><strong>Possible Root Gap:</strong> {lc.possible_root_gap}</p>
<p><strong>Evidence:</strong> {lc.evidence}</p>
<p><strong>Strategy:</strong> {lc.strategy}</p>
<p><strong>Next Review:</strong> {lc.next_review}</p></div>
<h2>Observations ({len(obs_rows)})</h2>
<table><tr><th>#</th><th>Observed</th><th>Root Gap</th><th>Evidence</th><th>Strength</th><th>Strategy</th><th>Confidence</th><th>Review</th></tr>
{obs_html}</table>
{refl}
<p style="margin-top:32px;font-size:.75rem;color:#999;">OpenSchoolOS — Educational Case Notebook — {now}</p>
</body></html>"""
    return HTMLResponse(content=html)


@router.get("/{case_id}/reasoning-timeline", response_model=ReasoningTimeline)
def get_reasoning_timeline(case_id: str, session: Session = Depends(get_session)) -> ReasoningTimeline:
    lc = session.get(LearningCaseModel, case_id)
    if lc is None or lc.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found.")

    observations = lc.observations
    snapshots = []
    prev_root_gap = prev_strategy = prev_confidence = None

    for i, obs in enumerate(observations):
        snapshots.append(ReasoningSnapshot(
            observation_id=obs.id, index=i + 1, observed=obs.observed,
            root_gap=obs.possible_root_gap, evidence=obs.evidence,
            evidence_strength=obs.evidence_strength, strategy=obs.strategy,
            confidence=obs.confidence, alternative_hypotheses=obs.alternative_hypotheses,
            created_at=obs.created_at.isoformat() if obs.created_at else None,
            root_gap_changed=prev_root_gap is not None and obs.possible_root_gap != prev_root_gap,
            strategy_changed=prev_strategy is not None and obs.strategy != prev_strategy,
            confidence_changed=prev_confidence is not None and obs.confidence != prev_confidence,
        ))
        prev_root_gap = obs.possible_root_gap
        prev_strategy = obs.strategy
        prev_confidence = obs.confidence

    return ReasoningTimeline(
        case_id=lc.id, subject=lc.subject, competency=lc.competency,
        current_root_gap=lc.possible_root_gap, current_strategy=lc.strategy,
        status=lc.status, snapshots=snapshots,
    )

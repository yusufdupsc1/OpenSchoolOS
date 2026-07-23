# OpenSchoolOS API — LearningCase routes (Sprint 001).
# Thin adapter over LearningCaseModel. Validates input, persists, returns
# shaped responses. No business rules here.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import LearningCaseModel, StudentModel
from app.schemas import LearningCaseCreate, LearningCaseOut

router = APIRouter(prefix="/learning-cases", tags=["learning-cases"])


@router.post("", response_model=LearningCaseOut, status_code=status.HTTP_201_CREATED)
def create_learning_case(
    payload: LearningCaseCreate, session: Session = Depends(get_session)
) -> LearningCaseOut:
    if session.get(StudentModel, payload.student_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found."
        )
    case_id = f"LC-{payload.student_id}-{payload.subject}"
    if session.get(LearningCaseModel, case_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Learning case for this student and subject already exists.",
        )
    model = LearningCaseModel(
        id=case_id,
        student_id=payload.student_id,
        subject=payload.subject,
        competency=payload.competency,
        possible_root_gap=payload.possible_root_gap,
        evidence=payload.evidence,
        strategy=payload.strategy,
        next_review=payload.next_review,
        status="open",
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.get("", response_model=list[LearningCaseOut])
def list_learning_cases(
    student_id: str | None = None, session: Session = Depends(get_session)
) -> list[LearningCaseOut]:
    stmt = select(LearningCaseModel)
    if student_id is not None:
        stmt = stmt.where(LearningCaseModel.student_id == student_id)
    rows = session.scalars(stmt.order_by(LearningCaseModel.created_at)).all()
    return [_to_out(r) for r in rows]


@router.patch("/{case_id}/close", response_model=LearningCaseOut)
def close_learning_case(
    case_id: str, session: Session = Depends(get_session)
) -> LearningCaseOut:
    model = session.get(LearningCaseModel, case_id)
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found."
        )
    model.status = "closed"
    session.commit()
    session.refresh(model)
    return _to_out(model)


def _to_out(r: LearningCaseModel) -> LearningCaseOut:
    return LearningCaseOut(
        id=r.id,
        student_id=r.student_id,
        subject=r.subject,
        competency=r.competency,
        possible_root_gap=r.possible_root_gap,
        evidence=r.evidence,
        strategy=r.strategy,
        next_review=r.next_review,
        status=r.status,
        created_at=r.created_at.isoformat() if r.created_at else None,
    )

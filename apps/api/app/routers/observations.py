# OpenSchoolOS API — Observation routes (Sprint 001).
# Thin adapter over ObservationModel. Validates input, persists, returns
# shaped responses. No business rules here.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import LearningCaseModel, ObservationModel
from app.schemas import ObservationCreate, ObservationOut

router = APIRouter(prefix="/observations", tags=["observations"])


@router.post("", response_model=ObservationOut, status_code=status.HTTP_201_CREATED)
def create_observation(
    payload: ObservationCreate, session: Session = Depends(get_session)
) -> ObservationOut:
    if session.get(LearningCaseModel, payload.learning_case_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found."
        )
    model = ObservationModel(
        id=f"OB-{payload.learning_case_id}-{payload.next_review}",
        learning_case_id=payload.learning_case_id,
        observed=payload.observed,
        possible_root_gap=payload.possible_root_gap,
        evidence=payload.evidence,
        strategy=payload.strategy,
        next_review=payload.next_review,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.get("", response_model=list[ObservationOut])
def list_observations(
    learning_case_id: str | None = None, session: Session = Depends(get_session)
) -> list[ObservationOut]:
    stmt = select(ObservationModel)
    if learning_case_id is not None:
        stmt = stmt.where(ObservationModel.learning_case_id == learning_case_id)
    rows = session.scalars(stmt.order_by(ObservationModel.created_at)).all()
    return [_to_out(r) for r in rows]


def _to_out(r: ObservationModel) -> ObservationOut:
    return ObservationOut(
        id=r.id,
        learning_case_id=r.learning_case_id,
        observed=r.observed,
        possible_root_gap=r.possible_root_gap,
        evidence=r.evidence,
        strategy=r.strategy,
        next_review=r.next_review,
        created_at=r.created_at.isoformat() if r.created_at else None,
    )

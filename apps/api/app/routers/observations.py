# OpenSchoolOS API — Observation routes (Sprint 003).
# Thin adapter over ObservationModel. Validates input, persists, returns
# shaped responses. No business rules here.
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import LearningCaseModel, ObservationModel
from app.schemas import ObservationCreate, ObservationOut, ObservationUpdate

router = APIRouter(prefix="/observations", tags=["observations"])


def _to_out(r: ObservationModel) -> ObservationOut:
    return ObservationOut(
        id=r.id,
        learning_case_id=r.learning_case_id,
        observed=r.observed,
        possible_root_gap=r.possible_root_gap,
        evidence=r.evidence,
        evidence_strength=r.evidence_strength,
        strategy=r.strategy,
        confidence=r.confidence,
        alternative_hypotheses=r.alternative_hypotheses,
        next_review=r.next_review,
        created_at=r.created_at.isoformat() if r.created_at else None,
        deleted_at=r.deleted_at.isoformat() if r.deleted_at else None,
    )


def _apply_payload(model: ObservationModel, payload: ObservationCreate | ObservationUpdate) -> None:
    """Apply payload fields to model instance (shared by create and update)."""
    if payload.observed is not None:
        model.observed = payload.observed
    if payload.possible_root_gap is not None:
        model.possible_root_gap = payload.possible_root_gap
    if payload.evidence is not None:
        model.evidence = payload.evidence
    if payload.evidence_strength is not None:
        model.evidence_strength = payload.evidence_strength
    if payload.strategy is not None:
        model.strategy = payload.strategy
    if payload.confidence is not None:
        model.confidence = payload.confidence
    if payload.alternative_hypotheses is not None:
        model.alternative_hypotheses = payload.alternative_hypotheses
    if payload.next_review is not None:
        model.next_review = payload.next_review


@router.post("", response_model=ObservationOut, status_code=status.HTTP_201_CREATED)
def create_observation(
    payload: ObservationCreate, session: Session = Depends(get_session)
) -> ObservationOut:
    lc = session.get(LearningCaseModel, payload.learning_case_id)
    if lc is None or lc.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Learning case not found."
        )
    model = ObservationModel(
        id=str(uuid.uuid4()),
        learning_case_id=payload.learning_case_id,
        observed=payload.observed,
        possible_root_gap=payload.possible_root_gap,
        evidence=payload.evidence,
        evidence_strength=payload.evidence_strength,
        strategy=payload.strategy,
        confidence=payload.confidence,
        alternative_hypotheses=payload.alternative_hypotheses,
        next_review=payload.next_review,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.get("", response_model=list[ObservationOut])
def list_observations(
    learning_case_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
) -> list[ObservationOut]:
    stmt = select(ObservationModel).where(ObservationModel.deleted_at.is_(None))
    if learning_case_id is not None:
        stmt = stmt.where(ObservationModel.learning_case_id == learning_case_id)
    rows = session.scalars(stmt.order_by(ObservationModel.created_at)).all()
    return [_to_out(r) for r in rows]


@router.get("/{observation_id}", response_model=ObservationOut)
def get_observation(
    observation_id: str, session: Session = Depends(get_session)
) -> ObservationOut:
    model = session.get(ObservationModel, observation_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Observation not found."
        )
    return _to_out(model)


@router.patch("/{observation_id}", response_model=ObservationOut)
def update_observation(
    observation_id: str,
    payload: ObservationUpdate,
    session: Session = Depends(get_session),
) -> ObservationOut:
    model = session.get(ObservationModel, observation_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Observation not found."
        )
    _apply_payload(model, payload)
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.delete("/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_observation(
    observation_id: str, session: Session = Depends(get_session)
) -> None:
    model = session.get(ObservationModel, observation_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Observation not found."
        )
    model.deleted_at = datetime.now(timezone.utc)
    session.commit()

# OpenSchoolOS API — Student routes (Sprint 001).
# Thin adapter: validates input via schemas, persists via SQLAlchemy models,
# returns shaped responses. No business rules here — those live in the domain.
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import StudentModel
from app.schemas import StudentCreate, StudentOut

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate, session: Session = Depends(get_session)
) -> StudentOut:
    student_id = f"STU-{payload.roll_number}-{payload.grade}{payload.section}"
    existing = session.get(StudentModel, student_id)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student with this id already exists.",
        )
    model = StudentModel(
        id=student_id,
        full_name=payload.full_name,
        roll_number=payload.roll_number,
        grade=payload.grade,
        section=payload.section,
        status="active",
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return StudentOut(
        id=model.id,
        full_name=model.full_name,
        roll_number=model.roll_number,
        grade=model.grade,
        section=model.section,
        status=model.status,
        created_at=model.created_at.isoformat() if model.created_at else None,
    )


@router.get("", response_model=list[StudentOut])
def list_students(session: Session = Depends(get_session)) -> list[StudentOut]:
    rows = session.scalars(select(StudentModel).order_by(StudentModel.created_at)).all()
    return [
        StudentOut(
            id=r.id,
            full_name=r.full_name,
            roll_number=r.roll_number,
            grade=r.grade,
            section=r.section,
            status=r.status,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in rows
    ]

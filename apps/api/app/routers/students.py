# OpenSchoolOS API — Student routes (Sprint 004).
import csv
import io
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.auth import optional_user
from app.db import get_session
from app.models import ObservationModel, StudentModel, UserModel
from app.schemas import BulkImportResult, StudentCreate, StudentOut, StudentUpdate, TimelineEntry

router = APIRouter(prefix="/students", tags=["students"])


def _to_out(r: StudentModel) -> StudentOut:
    return StudentOut(
        id=r.id, full_name=r.full_name, roll_number=r.roll_number,
        grade=r.grade, section=r.section, status=r.status,
        teacher_id=r.teacher_id,
        created_at=r.created_at.isoformat() if r.created_at else None,
        deleted_at=r.deleted_at.isoformat() if r.deleted_at else None,
    )


@router.post("", response_model=StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, session: Session = Depends(get_session), user: UserModel | None = Depends(optional_user)) -> StudentOut:
    model = StudentModel(
        id=str(uuid.uuid4()), full_name=payload.full_name,
        roll_number=payload.roll_number, grade=payload.grade,
        section=payload.section, status="active",
        teacher_id=user.id if user else None,
    )
    session.add(model)
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.post("/import", response_model=BulkImportResult)
def import_students(
    file: UploadFile = File(...), session: Session = Depends(get_session),
    user: UserModel | None = Depends(optional_user),
) -> BulkImportResult:
    """Import students from CSV. Columns: full_name, roll_number, grade, section."""
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    content = file.file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))
    required = {"full_name", "roll_number", "grade", "section"}
    if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
        raise HTTPException(status_code=400, detail="CSV must have: full_name, roll_number, grade, section")

    result = BulkImportResult()
    for i, row in enumerate(reader):
        try:
            fn = (row.get("full_name") or "").strip()
            rn = (row.get("roll_number") or "").strip()
            gr = (row.get("grade") or "").strip()
            se = (row.get("section") or "").strip()
            if not all([fn, rn, gr, se]):
                result.errors.append(f"Row {i + 2}: missing required fields")
                continue
            session.add(StudentModel(id=str(uuid.uuid4()), full_name=fn, roll_number=rn, grade=gr, section=se, status="active", teacher_id=user.id if user else None))
            result.created += 1
        except Exception as e:
            result.errors.append(f"Row {i + 2}: {e}")
    session.commit()
    return result


@router.get("", response_model=list[StudentOut])
def list_students(
    q: str | None = Query(default=None),
    session: Session = Depends(get_session),
    user: UserModel | None = Depends(optional_user),
) -> list[StudentOut]:
    stmt = select(StudentModel).where(StudentModel.deleted_at.is_(None))
    if user:
        stmt = stmt.where(StudentModel.teacher_id == user.id)
    if q:
        pattern = f"%{q}%"
        stmt = stmt.where(or_(StudentModel.full_name.ilike(pattern), StudentModel.roll_number.ilike(pattern)))
    rows = session.scalars(stmt.order_by(StudentModel.created_at)).all()
    return [_to_out(r) for r in rows]


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: str, session: Session = Depends(get_session)) -> StudentOut:
    model = session.get(StudentModel, student_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    return _to_out(model)


@router.patch("/{student_id}", response_model=StudentOut)
def update_student(student_id: str, payload: StudentUpdate, session: Session = Depends(get_session)) -> StudentOut:
    model = session.get(StudentModel, student_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    if payload.full_name is not None: model.full_name = payload.full_name
    if payload.roll_number is not None: model.roll_number = payload.roll_number
    if payload.grade is not None: model.grade = payload.grade
    if payload.section is not None: model.section = payload.section
    if payload.status is not None: model.status = payload.status
    session.commit()
    session.refresh(model)
    return _to_out(model)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, session: Session = Depends(get_session)) -> None:
    model = session.get(StudentModel, student_id)
    if model is None or model.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    model.deleted_at = datetime.now(timezone.utc)
    session.commit()


@router.get("/{student_id}/timeline", response_model=list[TimelineEntry])
def student_timeline(student_id: str, session: Session = Depends(get_session)) -> list[TimelineEntry]:
    student = session.get(StudentModel, student_id)
    if student is None or student.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    stmt = (
        select(ObservationModel)
        .join(ObservationModel.learning_case)
        .where(ObservationModel.learning_case.has(student_id=student_id), ObservationModel.deleted_at.is_(None))
        .order_by(ObservationModel.created_at.desc(), ObservationModel.id.desc())
    )
    rows = session.scalars(stmt).all()
    return [
        TimelineEntry(
            type="observation", id=r.id, case_id=r.learning_case_id,
            case_subject=r.learning_case.subject, observed=r.observed,
            possible_root_gap=r.possible_root_gap, evidence=r.evidence,
            evidence_strength=r.evidence_strength, strategy=r.strategy,
            confidence=r.confidence, alternative_hypotheses=r.alternative_hypotheses,
            next_review=r.next_review,
            created_at=r.created_at.isoformat() if r.created_at else None,
        ) for r in rows
    ]

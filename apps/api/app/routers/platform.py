# OpenSchoolOS API — Platform routes: health, export, backup (Sprint 005).
import io
import json as _json
import shutil
import uuid
from pathlib import Path
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func as safunc
from sqlalchemy.orm import Session

from app.db import get_session
from datetime import datetime as dt
from app.models import LearningCaseModel, ObservationModel, StudentModel, UserModel
from app.schemas import (
    DataExport, HealthStatus, LearningCaseOut, ObservationOut, StudentOut,
)


def _parse_dt(v: str | None):
    if v is None: return None
    try: return dt.fromisoformat(v)
    except: return None

router = APIRouter(tags=["platform"])


def _student_out(r: StudentModel) -> StudentOut:
    return StudentOut(
        id=r.id, full_name=r.full_name, roll_number=r.roll_number,
        grade=r.grade, section=r.section, status=r.status, teacher_id=r.teacher_id,
        created_at=r.created_at.isoformat() if r.created_at else None,
        deleted_at=r.deleted_at.isoformat() if r.deleted_at else None,
    )


@router.get("/health", response_model=HealthStatus)
def health(session: Session = Depends(get_session)):
    try:
        sc = session.scalar(select(safunc.count(StudentModel.id)).where(StudentModel.deleted_at.is_(None)))
        cc = session.scalar(select(safunc.count(LearningCaseModel.id)).where(LearningCaseModel.deleted_at.is_(None)))
        oc = session.scalar(select(safunc.count(ObservationModel.id)).where(ObservationModel.deleted_at.is_(None)))
        uc = session.scalar(select(safunc.count(UserModel.id)).where(UserModel.deleted_at.is_(None)))
        return HealthStatus(
            status="ok", db="connected", student_count=sc or 0,
            case_count=cc or 0, observation_count=oc or 0, user_count=uc or 0,
        )
    except Exception:
        return HealthStatus(status="degraded", db="disconnected", student_count=0, case_count=0, observation_count=0)


@router.get("/export", response_model=DataExport)
def export_data(session: Session = Depends(get_session)):
    students = session.scalars(select(StudentModel).where(StudentModel.deleted_at.is_(None))).all()
    cases = session.scalars(select(LearningCaseModel).where(LearningCaseModel.deleted_at.is_(None))).all()
    obs = session.scalars(select(ObservationModel).where(ObservationModel.deleted_at.is_(None))).all()
    return DataExport(
        students=[_student_out(s) for s in students],
        learning_cases=[LearningCaseOut(
            id=c.id, student_id=c.student_id, subject=c.subject, competency=c.competency,
            possible_root_gap=c.possible_root_gap, evidence=c.evidence, strategy=c.strategy,
            next_review=c.next_review, status=c.status, reflection=c.reflection, outcome=c.outcome,
            closed_at=c.closed_at.isoformat() if c.closed_at else None,
            created_at=c.created_at.isoformat() if c.created_at else None,
            deleted_at=c.deleted_at.isoformat() if c.deleted_at else None,
        ) for c in cases],
        observations=[ObservationOut(
            id=o.id, learning_case_id=o.learning_case_id, observed=o.observed,
            possible_root_gap=o.possible_root_gap, evidence=o.evidence,
            evidence_strength=o.evidence_strength, strategy=o.strategy,
            confidence=o.confidence, alternative_hypotheses=o.alternative_hypotheses,
            next_review=o.next_review,
            created_at=o.created_at.isoformat() if o.created_at else None,
            deleted_at=o.deleted_at.isoformat() if o.deleted_at else None,
        ) for o in obs],
    )


@router.get("/backup")
def backup_database(session: Session = Depends(get_session)):
    """Export all data (including soft-deleted) as JSON for backup."""
    students = session.scalars(select(StudentModel)).all()
    cases = session.scalars(select(LearningCaseModel)).all()
    obs = session.scalars(select(ObservationModel)).all()
    users = session.scalars(select(UserModel)).all()

    data = {
        "version": "1.0",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "students": [{"id": s.id, "teacher_id": s.teacher_id, "full_name": s.full_name, "roll_number": s.roll_number, "grade": s.grade, "section": s.section, "status": s.status, "created_at": s.created_at.isoformat() if s.created_at else None, "deleted_at": s.deleted_at.isoformat() if s.deleted_at else None} for s in students],
        "learning_cases": [{"id": c.id, "student_id": c.student_id, "subject": c.subject, "competency": c.competency, "possible_root_gap": c.possible_root_gap, "evidence": c.evidence, "strategy": c.strategy, "next_review": c.next_review, "status": c.status, "reflection": c.reflection, "closed_at": c.closed_at.isoformat() if c.closed_at else None, "created_at": c.created_at.isoformat() if c.created_at else None, "deleted_at": c.deleted_at.isoformat() if c.deleted_at else None} for c in cases],
        "observations": [{"id": o.id, "learning_case_id": o.learning_case_id, "observed": o.observed, "possible_root_gap": o.possible_root_gap, "evidence": o.evidence, "evidence_strength": o.evidence_strength, "strategy": o.strategy, "confidence": o.confidence, "alternative_hypotheses": o.alternative_hypotheses, "next_review": o.next_review, "created_at": o.created_at.isoformat() if o.created_at else None, "deleted_at": o.deleted_at.isoformat() if o.deleted_at else None} for o in obs],
        "users": [{"id": u.id, "email": u.email, "full_name": u.full_name, "hashed_password": u.hashed_password, "is_active": u.is_active, "created_at": u.created_at.isoformat() if u.created_at else None, "deleted_at": u.deleted_at.isoformat() if u.deleted_at else None} for u in users],
    }
    json_str = _json.dumps(data, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode()),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=openschoolos-backup-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.json"},
    )


@router.post("/restore")
def restore_database(file: UploadFile, session: Session = Depends(get_session)):
    """Restore data from a backup JSON file. WARNING: replaces all existing data."""
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Must upload a .json backup file.")

    try:
        data = _json.loads(file.file.read().decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON file.")

    if data.get("version") != "1.0":
        raise HTTPException(status_code=400, detail="Unsupported backup version.")

    # Clear existing data
    session.execute(ObservationModel.__table__.delete())
    session.execute(LearningCaseModel.__table__.delete())
    session.execute(StudentModel.__table__.delete())
    session.execute(UserModel.__table__.delete())

    # Restore users
    for u in data.get("users", []):
        session.execute(
            UserModel.__table__.insert().values(
                id=u["id"], email=u["email"], full_name=u["full_name"],
                hashed_password=u["hashed_password"], is_active=u.get("is_active", True),
                created_at=_parse_dt(u.get("created_at")), deleted_at=_parse_dt(u.get("deleted_at")),
            )
        )

    # Restore students
    for s in data.get("students", []):
        session.execute(
            StudentModel.__table__.insert().values(
                id=s["id"], teacher_id=s.get("teacher_id"), full_name=s["full_name"],
                roll_number=s["roll_number"], grade=s["grade"], section=s["section"],
                status=s.get("status", "active"), created_at=_parse_dt(s.get("created_at")),
                deleted_at=_parse_dt(s.get("deleted_at")),
            )
        )

    # Restore cases
    for c in data.get("learning_cases", []):
        session.execute(
            LearningCaseModel.__table__.insert().values(
                id=c["id"], student_id=c["student_id"], subject=c["subject"],
                competency=c["competency"], possible_root_gap=c["possible_root_gap"],
                evidence=c["evidence"], strategy=c["strategy"],
                next_review=c["next_review"], status=c.get("status", "open"),
                reflection=c.get("reflection"), outcome=c.get("outcome"),
                closed_at=_parse_dt(c.get("closed_at")),
                created_at=_parse_dt(c.get("created_at")), deleted_at=_parse_dt(c.get("deleted_at")),
            )
        )

    # Restore observations
    for o in data.get("observations", []):
        session.execute(
            ObservationModel.__table__.insert().values(
                id=o["id"], learning_case_id=o["learning_case_id"],
                observed=o["observed"], possible_root_gap=o["possible_root_gap"],
                evidence=o["evidence"], evidence_strength=o.get("evidence_strength"),
                strategy=o["strategy"], confidence=o.get("confidence"),
                alternative_hypotheses=o.get("alternative_hypotheses"),
                next_review=o["next_review"], created_at=_parse_dt(o.get("created_at")),
                deleted_at=_parse_dt(o.get("deleted_at")),
            )
        )
    session.commit()

    return {"status": "ok", "message": "Restore completed successfully."}

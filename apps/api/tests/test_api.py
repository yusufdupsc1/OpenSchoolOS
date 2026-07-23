# OpenSchoolOS API — pytest fixtures (Sprint 001).
# Integration tests use an in-memory SQLite DB with the same models/metadata,
# overriding the app's session dependency. No new dependencies; sqlite is
# bundled with SQLAlchemy.
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base
from app.db import get_session


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def override_get_session():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_student_create_and_list(client):
    res = client.post(
        "/students",
        json={"full_name": "Aisha Rahman", "roll_number": "12", "grade": "5", "section": "A"},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["full_name"] == "Aisha Rahman"
    assert body["status"] == "active"

    listed = client.get("/students").json()
    assert len(listed) == 1
    assert listed[0]["id"] == body["id"]


def test_student_duplicate_conflict(client):
    payload = {"full_name": "Aisha", "roll_number": "12", "grade": "5", "section": "A"}
    assert client.post("/students", json=payload).status_code == 201
    assert client.post("/students", json=payload).status_code == 409


def test_learning_case_requires_student(client):
    res = client.post(
        "/learning-cases",
        json={
            "student_id": "STU-12-5A",
            "subject": "Math",
            "competency": "Fractions",
            "possible_root_gap": "Place value",
            "evidence": "Reverses digits",
            "strategy": "Base-10 blocks",
            "next_review": "2026-08-01",
        },
    )
    assert res.status_code == 404


def test_full_notebook_workflow(client):
    student = client.post(
        "/students",
        json={"full_name": "Aisha", "roll_number": "12", "grade": "5", "section": "A"},
    ).json()
    case = client.post(
        "/learning-cases",
        json={
            "student_id": student["id"],
            "subject": "Math",
            "competency": "Fractions",
            "possible_root_gap": "Place value",
            "evidence": "Reverses digits",
            "strategy": "Base-10 blocks",
            "next_review": "2026-08-01",
        },
    )
    assert case.status_code == 201
    case_body = case.json()

    obs = client.post(
        "/observations",
        json={
            "learning_case_id": case_body["id"],
            "observed": "Wrote 21 for twelve",
            "possible_root_gap": "Place value",
            "evidence": "Consistent",
            "strategy": "Base-10 blocks",
            "next_review": "2026-08-05",
        },
    )
    assert obs.status_code == 201

    observations = client.get(f"/observations?learning_case_id={case_body['id']}").json()
    assert len(observations) == 1
    assert observations[0]["observed"] == "Wrote 21 for twelve"

    cases = client.get(f"/learning-cases?student_id={student['id']}").json()
    assert len(cases) == 1


def test_close_learning_case(client):
    student = client.post(
        "/students",
        json={"full_name": "Aisha", "roll_number": "12", "grade": "5", "section": "A"},
    ).json()
    case = client.post(
        "/learning-cases",
        json={
            "student_id": student["id"],
            "subject": "Math",
            "competency": "Fractions",
            "possible_root_gap": "Place value",
            "evidence": "Reverses digits",
            "strategy": "Base-10 blocks",
            "next_review": "2026-08-01",
        },
    ).json()

    closed = client.patch(f"/learning-cases/{case['id']}/close")
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"

    missing = client.patch("/learning-cases/does-not-exist/close")
    assert missing.status_code == 404

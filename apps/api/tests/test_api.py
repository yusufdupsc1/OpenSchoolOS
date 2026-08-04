# OpenSchoolOS API — pytest fixtures (Sprint 001.5).
# Integration tests use an in-memory SQLite DB with the same models/metadata,
# overriding the app's session dependency.
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


# ── Helpers ──────────────────────────────────────────────────────────────

def _create_student(client, **overrides):
    payload = {
        "full_name": "Aisha Rahman",
        "roll_number": "12",
        "grade": "5",
        "section": "A",
        **overrides,
    }
    res = client.post("/students", json=payload)
    assert res.status_code == 201
    return res.json()


def _create_case(client, student_id, **overrides):
    payload = {
        "student_id": student_id,
        "subject": "Mathematics",
        "competency": "Fractions",
        "possible_root_gap": "Place value",
        "evidence": "Reverses digits",
        "strategy": "Base-10 blocks",
        "next_review": "2026-08-01",
        **overrides,
    }
    res = client.post("/learning-cases", json=payload)
    assert res.status_code == 201
    return res.json()


def _create_obs(client, case_id, **overrides):
    payload = {
        "learning_case_id": case_id,
        "observed": "Wrote 21 for twelve",
        "possible_root_gap": "Place value",
        "evidence": "Consistent",
        "strategy": "Base-10 blocks",
        "next_review": "2026-08-05",
        **overrides,
    }
    res = client.post("/observations", json=payload)
    assert res.status_code == 201
    return res.json()


# ── Health ───────────────────────────────────────────────────────────────

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "student_count" in data


# ── Student CRUD ─────────────────────────────────────────────────────────

def test_student_create_and_list(client):
    body = _create_student(client)
    assert body["full_name"] == "Aisha Rahman"
    assert body["status"] == "active"
    assert len(body["id"]) == 36  # UUID

    listed = client.get("/students").json()
    assert len(listed) == 1
    assert listed[0]["id"] == body["id"]


def test_student_get_by_id(client):
    body = _create_student(client)
    fetched = client.get(f"/students/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["full_name"] == "Aisha Rahman"


def test_student_update(client):
    body = _create_student(client)
    res = client.patch(
        f"/students/{body['id']}",
        json={"full_name": "Aisha Rahman Updated", "section": "B"},
    )
    assert res.status_code == 200
    assert res.json()["full_name"] == "Aisha Rahman Updated"
    assert res.json()["section"] == "B"


def test_student_soft_delete(client):
    body = _create_student(client)
    res = client.delete(f"/students/{body['id']}")
    assert res.status_code == 204

    # should not appear in list
    listed = client.get("/students").json()
    assert len(listed) == 0

    # get by id should 404
    assert client.get(f"/students/{body['id']}").status_code == 404


def test_student_search(client):
    _create_student(client, full_name="Aisha", roll_number="1", grade="5", section="A")
    _create_student(client, full_name="Rahim", roll_number="2", grade="5", section="A")

    # search by name
    res = client.get("/students?q=aisha")
    assert len(res.json()) == 1
    assert res.json()[0]["full_name"] == "Aisha"

    # search by roll
    res = client.get("/students?q=2")
    assert len(res.json()) == 1
    assert res.json()[0]["full_name"] == "Rahim"


# ── Learning Case CRUD ───────────────────────────────────────────────────

def test_learning_case_requires_student(client):
    res = client.post(
        "/learning-cases",
        json={
            "student_id": "nonexistent-id",
            "subject": "Math",
            "competency": "Fractions",
            "possible_root_gap": "Place value",
            "evidence": "Reverses digits",
            "strategy": "Base-10 blocks",
            "next_review": "2026-08-01",
        },
    )
    assert res.status_code == 404


def test_learning_case_get_and_update(client):
    student = _create_student(client)
    case = _create_case(client, student["id"])

    fetched = client.get(f"/learning-cases/{case['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["subject"] == "Mathematics"

    res = client.patch(
        f"/learning-cases/{case['id']}",
        json={"strategy": "Number line approach", "next_review": "2026-09-01"},
    )
    assert res.status_code == 200
    assert res.json()["strategy"] == "Number line approach"
    assert res.json()["next_review"] == "2026-09-01"


def test_close_and_reopen_case(client):
    student = _create_student(client)
    case = _create_case(client, student["id"])

    closed = client.patch(f"/learning-cases/{case['id']}/close")
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"

    reopened = client.patch(f"/learning-cases/{case['id']}/reopen")
    assert reopened.status_code == 200
    assert reopened.json()["status"] == "open"


def test_learning_case_soft_delete(client):
    student = _create_student(client)
    case = _create_case(client, student["id"])

    res = client.delete(f"/learning-cases/{case['id']}")
    assert res.status_code == 204

    listed = client.get(f"/learning-cases?student_id={student['id']}").json()
    assert len(listed) == 0


def test_filter_by_status(client):
    student = _create_student(client)
    c1 = _create_case(client, student["id"], subject="Math")
    c2 = _create_case(client, student["id"], subject="Reading")

    client.patch(f"/learning-cases/{c1['id']}/close")

    open_cases = client.get("/learning-cases?status=open").json()
    closed_cases = client.get("/learning-cases?status=closed").json()
    assert len(open_cases) == 1
    assert len(closed_cases) == 1


# ── Observation CRUD ─────────────────────────────────────────────────────

def test_observation_update(client):
    student = _create_student(client)
    case = _create_case(client, student["id"])
    obs = _create_obs(client, case["id"])

    res = client.patch(
        f"/observations/{obs['id']}",
        json={"strategy": "Daily drill", "observed": "Now writes 12 correctly"},
    )
    assert res.status_code == 200
    assert res.json()["strategy"] == "Daily drill"
    assert res.json()["observed"] == "Now writes 12 correctly"


def test_observation_soft_delete(client):
    student = _create_student(client)
    case = _create_case(client, student["id"])
    obs = _create_obs(client, case["id"])

    res = client.delete(f"/observations/{obs['id']}")
    assert res.status_code == 204

    listed = client.get(f"/observations?learning_case_id={case['id']}").json()
    assert len(listed) == 0


# ── Full Notebook Workflow ───────────────────────────────────────────────

def test_full_notebook_workflow(client):
    student = _create_student(client)
    case = _create_case(client, student["id"])
    obs = _create_obs(client, case["id"])

    observations = client.get(
        f"/observations?learning_case_id={case['id']}"
    ).json()
    assert len(observations) == 1
    assert observations[0]["observed"] == "Wrote 21 for twelve"

    cases = client.get(f"/learning-cases?student_id={student['id']}").json()
    assert len(cases) == 1


# ── Timeline ─────────────────────────────────────────────────────────────

def test_student_timeline(client):
    student = _create_student(client)
    case1 = _create_case(client, student["id"], subject="Math")
    case2 = _create_case(client, student["id"], subject="Reading")

    _create_obs(client, case1["id"], observed="First math obs")
    _create_obs(client, case2["id"], observed="First reading obs")
    _create_obs(client, case1["id"], observed="Second math obs")

    timeline = client.get(f"/students/{student['id']}/timeline").json()
    assert len(timeline) == 3
    observed_set = {e["observed"] for e in timeline}
    assert observed_set == {"First math obs", "First reading obs", "Second math obs"}
    subjects = {e["case_subject"] for e in timeline}
    assert subjects == {"Math", "Reading"}

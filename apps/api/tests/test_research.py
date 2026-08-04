"""OpenSchoolOS API — Research / Analytics tests (Sprint 006)."""
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
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    def override():
        s = TestingSessionLocal()
        try: yield s
        finally: s.close()
    app.dependency_overrides[get_session] = override
    with TestClient(app) as c: yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def _post(client, path, data):
    return client.post(path, json=data)


def test_dashboard_empty(client):
    """Dashboard on empty DB returns zeroes, no crash."""
    res = client.get("/research/dashboard")
    assert res.status_code == 200
    d = res.json()
    assert d["total_cases"] == 0
    assert d["open_cases"] == 0
    assert d["closed_cases"] == 0
    assert d["outcomes"] == []


def test_dashboard_with_data(client):
    """Dashboard aggregates case outcomes and durations."""
    s = _post(client, "/students", {"full_name": "A", "roll_number": "1", "grade": "3", "section": "A"}).json()
    c1 = _post(client, "/learning-cases", {"student_id": s["id"], "subject": "Math", "competency": "Add", "possible_root_gap": "G", "evidence": "E", "strategy": "Use blocks", "next_review": "2026-01-01"}).json()
    c2 = _post(client, "/learning-cases", {"student_id": s["id"], "subject": "Reading", "competency": "Phonics", "possible_root_gap": "G", "evidence": "E", "strategy": "Sound drills", "next_review": "2026-01-01"}).json()

    # Add observations
    _post(client, "/observations", {"learning_case_id": c1["id"], "observed": "Counts well", "possible_root_gap": "G", "evidence": "E", "strategy": "ST", "next_review": "2026-01-01"})
    _post(client, "/observations", {"learning_case_id": c1["id"], "observed": "Still slow", "possible_root_gap": "G", "evidence": "E", "strategy": "ST", "next_review": "2026-01-01"})

    # Close c1 with outcome
    client.patch(
        f"/learning-cases/{c1['id']}/close",
        json={"outcome": "improved", "reflection": "Great progress"}
    )

    d = client.get("/research/dashboard").json()
    assert d["total_cases"] == 2
    assert d["open_cases"] == 1
    assert d["closed_cases"] == 1
    assert d["total_observations"] == 2
    assert d["avg_observations_per_case"] == 1.0

    # Outcomes
    outcomes = {o["outcome"]: o["count"] for o in d["outcomes"]}
    assert outcomes.get("improved") == 1

    # Duration
    assert d["duration"]["overall"]["count"] == 1
    assert d["duration"]["overall"]["avg_days"] >= 0

    # Strategies
    assert len(d["top_strategies"]) >= 1
    assert d["top_strategies"][0]["count"] >= 1

    # Cases per subject
    subjects = {x["subject"]: x["count"] for x in d["cases_per_subject"]}
    assert subjects["Math"] == 1
    assert subjects["Reading"] == 1


def test_close_with_outcome(client):
    """Closing a case with an outcome field works."""
    s = _post(client, "/students", {"full_name": "B", "roll_number": "2", "grade": "4", "section": "B"}).json()
    c = _post(client, "/learning-cases", {"student_id": s["id"], "subject": "Math", "competency": "M", "possible_root_gap": "G", "evidence": "E", "strategy": "S", "next_review": "2026-01-01"}).json()

    # Close with all fields
    res = client.patch(
        f"/learning-cases/{c['id']}/close",
        json={"outcome": "improved", "reflection": "Student grasped the concept"}
    )
    assert res.status_code == 200
    body = res.json()
    assert body["outcome"] == "improved"
    assert body["reflection"] == "Student grasped the concept"
    assert body["status"] == "closed"


def test_close_without_outcome_defaults_none(client):
    """Closing without outcome leaves it None."""
    s = _post(client, "/students", {"full_name": "C", "roll_number": "3", "grade": "2", "section": "C"}).json()
    c = _post(client, "/learning-cases", {"student_id": s["id"], "subject": "English", "competency": "X", "possible_root_gap": "G", "evidence": "E", "strategy": "S", "next_review": "2026-01-01"}).json()
    res = client.patch(f"/learning-cases/{c['id']}/close", json={})
    assert res.status_code == 200
    assert res.json()["outcome"] is None


def test_outcome_via_update(client):
    """Outcome can be set via PATCH update."""
    s = _post(client, "/students", {"full_name": "D", "roll_number": "4", "grade": "1", "section": "A"}).json()
    c = _post(client, "/learning-cases", {"student_id": s["id"], "subject": "Art", "competency": "Y", "possible_root_gap": "G", "evidence": "E", "strategy": "S", "next_review": "2026-01-01"}).json()

    # Set outcome before closing
    res = client.patch(f"/learning-cases/{c['id']}", json={"outcome": "plateaued"})
    assert res.status_code == 200
    assert res.json()["outcome"] == "plateaued"

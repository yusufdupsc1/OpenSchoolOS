# OpenSchoolOS API — Reasoning layer integration tests (Sprint 003).
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


def _create_student(client, name="Aisha", roll="12", grade="5", section="A"):
    return client.post(
        "/students",
        json={"full_name": name, "roll_number": roll, "grade": grade, "section": section},
    ).json()


def _create_case(client, sid, subject="Math", competency="Fractions"):
    return client.post(
        "/learning-cases",
        json={
            "student_id": sid,
            "subject": subject,
            "competency": competency,
            "possible_root_gap": "Place value",
            "evidence": "Reverses digits",
            "strategy": "Base-10 blocks",
            "next_review": "2026-08-01",
        },
    ).json()


def test_observation_with_confidence_and_evidence_strength(client):
    """Create an observation with reasoning fields set."""
    s = _create_student(client)
    c = _create_case(client, s["id"])

    res = client.post(
        "/observations",
        json={
            "learning_case_id": c["id"],
            "observed": "Wrote 21 for twelve",
            "possible_root_gap": "Place value",
            "evidence": "Consistent pattern",
            "evidence_strength": "direct_observation",
            "strategy": "Base-10 blocks",
            "confidence": "medium",
            "alternative_hypotheses": '["Number reversal habit","Weak place value"]',
            "next_review": "2026-08-05",
        },
    )
    assert res.status_code == 201
    body = res.json()
    assert body["confidence"] == "medium"
    assert body["evidence_strength"] == "direct_observation"
    assert "Number reversal" in body["alternative_hypotheses"]


def test_observation_update_reasoning_fields(client):
    """PATCH can update confidence, evidence_strength, and alternative_hypotheses."""
    s = _create_student(client)
    c = _create_case(client, s["id"])
    obs = client.post(
        "/observations",
        json={
            "learning_case_id": c["id"],
            "observed": "Test",
            "possible_root_gap": "PG",
            "evidence": "EV",
            "strategy": "ST",
            "next_review": "2026-08-01",
        },
    ).json()

    res = client.patch(
        f"/observations/{obs['id']}",
        json={
            "confidence": "high",
            "evidence_strength": "test_result",
            "alternative_hypotheses": '["Other gap"]',
            "observed": "Changed observation",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["confidence"] == "high"
    assert body["evidence_strength"] == "test_result"
    assert body["alternative_hypotheses"] == '["Other gap"]'
    assert body["observed"] == "Changed observation"


def test_reasoning_timeline_no_observations(client):
    """Timeline for a case with no observations is empty but valid."""
    s = _create_student(client)
    c = _create_case(client, s["id"])

    res = client.get(f"/learning-cases/{c['id']}/reasoning-timeline")
    assert res.status_code == 200
    tl = res.json()
    assert tl["case_id"] == c["id"]
    assert tl["snapshots"] == []


def test_reasoning_timeline_tracks_changes(client):
    """Timeline shows how hypothesis, strategy, and confidence evolve."""
    s = _create_student(client)
    c = _create_case(client, s["id"])

    # Observation 1
    client.post(
        "/observations",
        json={
            "learning_case_id": c["id"],
            "observed": "First obs",
            "possible_root_gap": "Place value",
            "evidence": "E1",
            "evidence_strength": "inference",
            "strategy": "Base-10 blocks",
            "confidence": "low",
            "next_review": "2026-08-01",
        },
    )

    # Observation 2 — changes root gap and strategy
    client.post(
        "/observations",
        json={
            "learning_case_id": c["id"],
            "observed": "Second obs",
            "possible_root_gap": "Number sense",
            "evidence": "E2",
            "evidence_strength": "direct_observation",
            "strategy": "Counting objects",
            "confidence": "medium",
            "next_review": "2026-08-05",
        },
    )

    # Observation 3 — same as 2, no change
    client.post(
        "/observations",
        json={
            "learning_case_id": c["id"],
            "observed": "Third obs",
            "possible_root_gap": "Number sense",
            "evidence": "E3",
            "strategy": "Counting objects",
            "confidence": "medium",
            "next_review": "2026-08-10",
        },
    )

    tl = client.get(
        f"/learning-cases/{c['id']}/reasoning-timeline"
    ).json()
    assert len(tl["snapshots"]) == 3

    # Snapshot 1: no changes (first observation)
    s1 = tl["snapshots"][0]
    assert s1["index"] == 1
    assert s1["root_gap_changed"] is False
    assert s1["strategy_changed"] is False
    assert s1["confidence_changed"] is False
    assert s1["confidence"] == "low"
    assert s1["evidence_strength"] == "inference"

    # Snapshot 2: root gap and strategy changed
    s2 = tl["snapshots"][1]
    assert s2["index"] == 2
    assert s2["root_gap_changed"] is True
    assert s2["strategy_changed"] is True
    assert s2["confidence_changed"] is True
    assert s2["root_gap"] == "Number sense"
    assert s2["evidence_strength"] == "direct_observation"

    # Snapshot 3: nothing changed from snapshot 2
    s3 = tl["snapshots"][2]
    assert s3["index"] == 3
    assert s3["root_gap_changed"] is False
    assert s3["strategy_changed"] is False

    # Current values reflect the case's state (not auto-updated by observations)
    assert tl["current_root_gap"] == "Place value"  # case was never updated
    assert tl["current_strategy"] == "Base-10 blocks"


def test_reasoning_timeline_404(client):
    res = client.get("/learning-cases/nonexistent/reasoning-timeline")
    assert res.status_code == 404

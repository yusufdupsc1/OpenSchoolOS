# OpenSchoolOS API — AI Extension Points tests (Sprint 007).
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


def _p(client, path, data):
    return client.post(path, json=data)


def test_similar_cases_empty(client):
    s = _p(client, "/students", {"full_name": "A", "roll_number": "1", "grade": "1", "section": "A"}).json()
    c = _p(client, "/learning-cases", {"student_id": s["id"], "subject": "Math", "competency": "X", "possible_root_gap": "Place value", "evidence": "E", "strategy": "Blocks", "next_review": "2026-01-01"}).json()
    res = client.get(f"/ai/similar-cases/{c['id']}")
    assert res.status_code == 200
    assert res.json()["results"] == []


def test_similar_cases_finds_matches(client):
    s = _p(client, "/students", {"full_name": "A", "roll_number": "1", "grade": "1", "section": "A"}).json()
    s2 = _p(client, "/students", {"full_name": "B", "roll_number": "2", "grade": "2", "section": "B"}).json()
    c1 = _p(client, "/learning-cases", {"student_id": s["id"], "subject": "Math", "competency": "Add", "possible_root_gap": "Place value", "evidence": "E", "strategy": "Blocks", "next_review": "2026-01-01"}).json()
    c2 = _p(client, "/learning-cases", {"student_id": s2["id"], "subject": "Math", "competency": "Fractions", "possible_root_gap": "Place value", "evidence": "E", "strategy": "Blocks", "next_review": "2026-01-01"}).json()

    res = client.get(f"/ai/similar-cases/{c1['id']}")
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) >= 1
    assert data["results"][0]["similarity"] == "same_root_gap"


def test_observation_summary(client):
    s = _p(client, "/students", {"full_name": "A", "roll_number": "1", "grade": "3", "section": "A"}).json()
    c = _p(client, "/learning-cases", {"student_id": s["id"], "subject": "Reading", "competency": "Phonics", "possible_root_gap": "Letter-sound", "evidence": "E", "strategy": "Sound drills", "next_review": "2026-01-01"}).json()
    _p(client, "/observations", {"learning_case_id": c["id"], "observed": "Guesses words", "possible_root_gap": "Letter-sound", "evidence": "EV", "strategy": "Sound drills", "confidence": "low", "next_review": "2026-01-05"})
    _p(client, "/observations", {"learning_case_id": c["id"], "observed": "Sounding out slowly", "possible_root_gap": "Letter-sound", "evidence": "EV", "strategy": "Sound drills", "confidence": "medium", "next_review": "2026-01-10"})

    res = client.get(f"/ai/observation-summary/{c['id']}")
    assert res.status_code == 200
    data = res.json()
    assert data["observation_count"] == 2
    assert "Letter-sound" in data["heuristic_summary"]
    assert "Guesses words" in data["raw_context"]
    assert len(data["root_gap_progression"]) == 2
    assert len(data["confidence_progression"]) == 2


def test_autocomplete_ldg(client):
    res = client.get("/ai/autocomplete?q=fractions&source=ldg")
    assert res.status_code == 200
    data = res.json()
    assert len(data["matches"]) > 0
    assert data["source"] == "ldg"


def test_autocomplete_past_cases(client):
    s = _p(client, "/students", {"full_name": "X", "roll_number": "9", "grade": "4", "section": "C"}).json()
    _p(client, "/learning-cases", {"student_id": s["id"], "subject": "Math", "competency": "Y", "possible_root_gap": "Custom gap ZZZ", "evidence": "E", "strategy": "S", "next_review": "2026-01-01"})

    res = client.get("/ai/autocomplete?q=ZZZ&source=past_cases")
    assert res.status_code == 200
    data = res.json()
    assert len(data["matches"]) >= 1
    assert any("ZZZ" in m for m in data["matches"])


def test_similar_cases_404(client):
    res = client.get("/ai/similar-cases/nonexistent")
    assert res.status_code == 404


def test_observation_summary_404(client):
    res = client.get("/ai/observation-summary/nonexistent")
    assert res.status_code == 404

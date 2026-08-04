# OpenSchoolOS API — Knowledge (LDG) integration tests (Sprint 002).
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def test_list_subjects(client):
    res = client.get("/knowledge/subjects")
    assert res.status_code == 200
    subjects = res.json()
    assert len(subjects) >= 5
    ids = {s["id"] for s in subjects}
    assert "math" in ids
    assert "reading" in ids
    assert "writing" in ids
    assert "english" in ids
    assert "bangla" in ids


def test_get_subject(client):
    res = client.get("/knowledge/subjects/math")
    assert res.status_code == 200
    data = res.json()
    assert data["subject"] == "Mathematics"
    assert len(data["competencies"]) >= 8
    assert "dependencyGraph" in data
    assert "math-number-sense" in data["dependencyGraph"]


def test_get_subject_not_found(client):
    res = client.get("/knowledge/subjects/nonexistent")
    assert res.status_code == 404


def test_list_competencies(client):
    res = client.get("/knowledge/subjects/reading/competencies")
    assert res.status_code == 200
    comps = res.json()
    assert len(comps) >= 5
    labels = {c["label"] for c in comps}
    assert "Phonemic Awareness" in labels
    assert "Phonics (Letter-Sound Mapping)" in labels


def test_get_competency(client):
    res = client.get(
        "/knowledge/subjects/math/competencies/math-fractions"
    )
    assert res.status_code == 200
    comp = res.json()
    assert comp["label"] == "Fractions"
    assert "prerequisites" in comp
    assert "math-division" in comp["prerequisites"]
    assert len(comp["misconceptions"]) >= 1


def test_get_competency_not_found(client):
    res = client.get(
        "/knowledge/subjects/math/competencies/nonexistent"
    )
    assert res.status_code == 404


def test_search_competencies(client):
    res = client.get(
        "/knowledge/subjects/math/search?q=fractions"
    )
    assert res.status_code == 200
    results = res.json()
    assert len(results) >= 1
    assert any("fractions" in r.get("competencyLabel", "").lower() for r in results)


def test_search_competencies_misconception(client):
    """Searching for 'guesses' should find the reading phonemic awareness misconception."""
    res = client.get(
        "/knowledge/subjects/reading/search?q=guesses"
    )
    assert res.status_code == 200
    results = res.json()
    assert len(results) >= 1
    # At least one result should have matched misconceptions
    has_misconceptions = any(
        r.get("matchedMisconceptions") and len(r["matchedMisconceptions"]) > 0
        for r in results
    )
    assert has_misconceptions, "Expected matched misconceptions for 'guesses'"


def test_search_all_subjects(client):
    res = client.get("/knowledge/search?q=place+value")
    assert res.status_code == 200
    results = res.json()
    assert len(results) >= 1
    # Should find math place-value
    subjects = {r["subjectId"] for r in results}
    assert "math" in subjects


def test_search_all_subjects_bangla(client):
    """Search should work across Bangla subject too."""
    res = client.get("/knowledge/search?q=কার")
    assert res.status_code == 200
    results = res.json()
    # Should find bangla kar-related competencies
    assert len(results) >= 1


def test_misconception_patterns_present(client):
    """Every competency with misconceptions should have observed, rootGap, evidence, strategy."""
    res = client.get("/knowledge/subjects/math/competencies/math-multiplication")
    comp = res.json()
    for m in comp.get("misconceptions", []):
        assert m.get("observed"), f"Misconception missing 'observed': {m}"
        assert m.get("rootGap"), f"Misconception missing 'rootGap': {m}"
        assert m.get("evidence"), f"Misconception missing 'evidence': {m}"
        assert m.get("strategy"), f"Misconception missing 'strategy': {m}"

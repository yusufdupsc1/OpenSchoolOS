import io, json
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

    def override_get_session():
        s = TestingSessionLocal()
        try:
            yield s
        finally:
            s.close()

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_health_enriched(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["db"] == "connected"


def test_health_with_data(client):
    client.post("/students", json={"full_name": "A", "roll_number": "1", "grade": "1", "section": "A"})
    res = client.get("/health")
    assert res.json()["student_count"] == 1


def test_export(client):
    client.post("/students", json={"full_name": "A", "roll_number": "1", "grade": "5", "section": "A"})
    res = client.get("/export")
    assert res.status_code == 200
    data = res.json()
    assert len(data["students"]) == 1
    assert data["students"][0]["full_name"] == "A"


def test_backup_and_restore(client):
    s = client.post("/students", json={"full_name": "Aisha", "roll_number": "1", "grade": "5", "section": "A"}).json()
    res = client.get("/backup")
    assert res.status_code == 200
    backup_data = res.json()
    assert len(backup_data["students"]) == 1

    backup_bytes = io.BytesIO(json.dumps(backup_data).encode())
    restore_res = client.post("/restore", files={"file": ("backup.json", backup_bytes, "application/json")})
    assert restore_res.status_code == 200

    students = client.get("/students").json()
    assert len(students) == 1
    assert students[0]["full_name"] == "Aisha"


def test_export_includes_all_entities(client):
    s = client.post("/students", json={"full_name": "S", "roll_number": "1", "grade": "1", "section": "A"}).json()
    c = client.post("/learning-cases", json={"student_id": s["id"], "subject": "Math", "competency": "X", "possible_root_gap": "Y", "evidence": "Z", "strategy": "W", "next_review": "2026-01-01"}).json()
    client.post("/observations", json={"learning_case_id": c["id"], "observed": "Obs", "possible_root_gap": "Gap", "evidence": "Ev", "strategy": "St", "next_review": "2026-01-01"})
    data = client.get("/export").json()
    assert len(data["students"]) == 1
    assert len(data["learning_cases"]) == 1
    assert len(data["observations"]) == 1

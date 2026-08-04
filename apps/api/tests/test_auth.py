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


def test_register(client):
    res = client.post("/auth/register", json={"email": "teacher@school.org", "full_name": "Ms. Rahman", "password": "secret123"})
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "teacher@school.org"


def test_register_duplicate(client):
    client.post("/auth/register", json={"email": "dup@school.org", "full_name": "T1", "password": "secret123"})
    res = client.post("/auth/register", json={"email": "dup@school.org", "full_name": "T2", "password": "secret123"})
    assert res.status_code == 409


def test_login(client):
    client.post("/auth/register", json={"email": "login@school.org", "full_name": "T", "password": "secret123"})
    res = client.post("/auth/login", json={"email": "login@school.org", "password": "secret123"})
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "wp@school.org", "full_name": "T", "password": "correct"})
    res = client.post("/auth/login", json={"email": "wp@school.org", "password": "wrong"})
    assert res.status_code == 401


def test_me(client):
    reg = client.post("/auth/register", json={"email": "me@school.org", "full_name": "Me", "password": "secret123"}).json()
    res = client.get("/auth/me", headers={"Authorization": f"Bearer {reg['access_token']}"})
    assert res.status_code == 200
    assert res.json()["email"] == "me@school.org"


def test_me_no_auth(client):
    res = client.get("/auth/me")
    assert res.status_code == 401


def test_student_auto_assigned_to_teacher(client):
    reg = client.post("/auth/register", json={"email": "t@school.org", "full_name": "T", "password": "secret123"}).json()
    tok = reg["access_token"]
    s = client.post("/students", json={"full_name": "Aisha", "roll_number": "1", "grade": "5", "section": "A"}, headers={"Authorization": f"Bearer {tok}"})
    assert s.status_code == 201
    assert s.json()["teacher_id"] == reg["user"]["id"]


def test_teacher_sees_only_own_students(client):
    ra = client.post("/auth/register", json={"email": "a@school.org", "full_name": "TA", "password": "secret123"}).json()
    rb = client.post("/auth/register", json={"email": "b@school.org", "full_name": "TB", "password": "secret123"}).json()
    client.post("/students", json={"full_name": "StudentA", "roll_number": "1", "grade": "1", "section": "A"}, headers={"Authorization": f"Bearer {ra['access_token']}"})
    client.post("/students", json={"full_name": "StudentB", "roll_number": "2", "grade": "1", "section": "A"}, headers={"Authorization": f"Bearer {rb['access_token']}"})
    list_a = client.get("/students", headers={"Authorization": f"Bearer {ra['access_token']}"}).json()
    list_b = client.get("/students", headers={"Authorization": f"Bearer {rb['access_token']}"}).json()
    assert len(list_a) == 1
    assert list_a[0]["full_name"] == "StudentA"
    assert len(list_b) == 1
    assert list_b[0]["full_name"] == "StudentB"


def test_cannot_create_case_for_other_teachers_student(client):
    ra = client.post("/auth/register", json={"email": "owner@school.org", "full_name": "Owner", "password": "secret123"}).json()
    rb = client.post("/auth/register", json={"email": "intruder@school.org", "full_name": "Intruder", "password": "secret123"}).json()
    s = client.post("/students", json={"full_name": "S", "roll_number": "1", "grade": "1", "section": "A"}, headers={"Authorization": f"Bearer {ra['access_token']}"}).json()
    res = client.post("/learning-cases", json={"student_id": s["id"], "subject": "Math", "competency": "X", "possible_root_gap": "Y", "evidence": "Z", "strategy": "W", "next_review": "2026-01-01"}, headers={"Authorization": f"Bearer {rb['access_token']}"})
    assert res.status_code == 403

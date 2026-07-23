# OpenSchoolOS API — application entrypoint (Sprint 001).
# Thin FastAPI shell. Domain logic lives in packages/domain; persistence in
# app.models. No auth in Sprint 1 (tech-stack.md).
from fastapi import FastAPI

from app.routers import students, learning_cases, observations

app = FastAPI(title="OpenSchoolOS API", version="0.1.0")

app.include_router(students.router)
app.include_router(learning_cases.router)
app.include_router(observations.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

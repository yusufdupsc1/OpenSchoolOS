# OpenSchoolOS API — application entrypoint (Sprint 005).
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine
from app.models import Base
from app.routers import students, learning_cases, observations, knowledge, auth, platform, research, ai


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="OpenSchoolOS API", version="0.7.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(learning_cases.router)
app.include_router(observations.router)
app.include_router(knowledge.router)
app.include_router(auth.router)
app.include_router(platform.router)
app.include_router(research.router)
app.include_router(ai.router)

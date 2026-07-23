# OpenSchoolOS API — Pydantic schemas (Sprint 001).
# Validation/Boundary layer. Mirrors the persisted shape of the three
# aggregates. Domain rules live in packages/domain; these only validate wire
# input and shape responses.
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    full_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    grade: str = Field(min_length=1)
    section: str = Field(min_length=1)


class StudentOut(BaseModel):
    id: str
    full_name: str
    roll_number: str
    grade: str
    section: str
    status: str
    created_at: str | None = None


class LearningCaseCreate(BaseModel):
    student_id: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    competency: str = Field(min_length=1)
    possible_root_gap: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    strategy: str = Field(min_length=1)
    next_review: str = Field(min_length=1)


class LearningCaseOut(BaseModel):
    id: str
    student_id: str
    subject: str
    competency: str
    possible_root_gap: str
    evidence: str
    strategy: str
    next_review: str
    status: str
    created_at: str | None = None


class ObservationCreate(BaseModel):
    learning_case_id: str = Field(min_length=1)
    observed: str = Field(min_length=1)
    possible_root_gap: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    strategy: str = Field(min_length=1)
    next_review: str = Field(min_length=1)


class ObservationOut(BaseModel):
    id: str
    learning_case_id: str
    observed: str
    possible_root_gap: str
    evidence: str
    strategy: str
    next_review: str
    created_at: str | None = None

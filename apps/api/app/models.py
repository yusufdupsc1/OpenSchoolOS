# OpenSchoolOS API — SQLAlchemy models (Sprint 001).
# Infrastructure adapter. Maps the three educational aggregates to exactly
# three tables (data-model.md). The Python domain is represented here as
# persisted primitives; the rich TypeScript domain in packages/domain stays
# framework-free and is the conceptual source of truth.
#
# students        <-> Student
# learning_cases  <-> LearningCase
# observations    <-> Observation
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class StudentModel(Base):
    __tablename__ = "students"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    roll_number: Mapped[str] = mapped_column(String(64), nullable=False)
    grade: Mapped[str] = mapped_column(String(32), nullable=False)
    section: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    learning_cases: Mapped[list["LearningCaseModel"]] = relationship(
        back_populates="student"
    )


class LearningCaseModel(Base):
    __tablename__ = "learning_cases"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    student_id: Mapped[str] = mapped_column(
        ForeignKey("students.id"), nullable=False, index=True
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    competency: Mapped[str] = mapped_column(String(255), nullable=False)
    possible_root_gap: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    strategy: Mapped[str] = mapped_column(Text, nullable=False)
    next_review: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    student: Mapped["StudentModel"] = relationship(back_populates="learning_cases")
    observations: Mapped[list["ObservationModel"]] = relationship(
        back_populates="learning_case"
    )


class ObservationModel(Base):
    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    learning_case_id: Mapped[str] = mapped_column(
        ForeignKey("learning_cases.id"), nullable=False, index=True
    )
    observed: Mapped[str] = mapped_column(Text, nullable=False)
    possible_root_gap: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    strategy: Mapped[str] = mapped_column(Text, nullable=False)
    next_review: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    learning_case: Mapped["LearningCaseModel"] = relationship(back_populates="observations")

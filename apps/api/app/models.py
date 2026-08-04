# OpenSchoolOS API — SQLAlchemy models (Sprint 005).
from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped["DateTime | None"] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    students: Mapped[list["StudentModel"]] = relationship(back_populates="teacher")


class StudentModel(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("grade", "section", "roll_number", name="uq_student_class_roll"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    teacher_id: Mapped["str | None"] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    roll_number: Mapped[str] = mapped_column(String(64), nullable=False)
    grade: Mapped[str] = mapped_column(String(32), nullable=False)
    section: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped["DateTime | None"] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    teacher: Mapped["UserModel | None"] = relationship(back_populates="students")
    learning_cases: Mapped[list["LearningCaseModel"]] = relationship(back_populates="student")


class LearningCaseModel(Base):
    __tablename__ = "learning_cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    competency: Mapped[str] = mapped_column(String(255), nullable=False)
    possible_root_gap: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    strategy: Mapped[str] = mapped_column(Text, nullable=False)
    next_review: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    reflection: Mapped["str | None"] = mapped_column(Text, nullable=True, default=None)
    closed_at: Mapped["DateTime | None"] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
    outcome: Mapped["str | None"] = mapped_column(String(32), nullable=True, default=None)
    # "improved" | "plateaued" | "worsened" | "transferred" | "unknown"
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped["DateTime | None"] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    student: Mapped["StudentModel"] = relationship(back_populates="learning_cases")
    observations: Mapped[list["ObservationModel"]] = relationship(back_populates="learning_case", order_by="ObservationModel.created_at")


class ObservationModel(Base):
    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    learning_case_id: Mapped[str] = mapped_column(ForeignKey("learning_cases.id"), nullable=False, index=True)
    observed: Mapped[str] = mapped_column(Text, nullable=False)
    possible_root_gap: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_strength: Mapped["str | None"] = mapped_column(String(32), nullable=True, default=None)
    strategy: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped["str | None"] = mapped_column(String(16), nullable=True, default=None)
    alternative_hypotheses: Mapped["str | None"] = mapped_column(Text, nullable=True, default=None)
    next_review: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped["DateTime | None"] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    learning_case: Mapped["LearningCaseModel"] = relationship(back_populates="observations")

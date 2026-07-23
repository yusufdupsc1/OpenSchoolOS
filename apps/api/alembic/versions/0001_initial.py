# OpenSchoolOS API — initial schema (Sprint 001).
# Creates the three tables backing the educational aggregates (data-model.md).
# students <-> Student, learning_cases <-> LearningCase,
# observations <-> Observation. Interventions live in learning_cases.strategy.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("roll_number", sa.String(length=64), nullable=False),
        sa.Column("grade", sa.String(length=32), nullable=False),
        sa.Column("section", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "learning_cases",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("student_id", sa.String(length=64), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("competency", sa.String(length=255), nullable=False),
        sa.Column("possible_root_gap", sa.Text(), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=False),
        sa.Column("strategy", sa.Text(), nullable=False),
        sa.Column("next_review", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_learning_cases_student_id", "learning_cases", ["student_id"])

    op.create_table(
        "observations",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("learning_case_id", sa.String(length=64), sa.ForeignKey("learning_cases.id"), nullable=False),
        sa.Column("observed", sa.Text(), nullable=False),
        sa.Column("possible_root_gap", sa.Text(), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=False),
        sa.Column("strategy", sa.Text(), nullable=False),
        sa.Column("next_review", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_observations_learning_case_id", "observations", ["learning_case_id"])


def downgrade() -> None:
    op.drop_table("observations")
    op.drop_table("learning_cases")
    op.drop_table("students")

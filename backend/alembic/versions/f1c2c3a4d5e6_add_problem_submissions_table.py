"""add problem submissions table

Revision ID: f1c2c3a4d5e6
Revises: 78bc88f6ce70
Create Date: 2026-05-25 15:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f1c2c3a4d5e6"
down_revision: Union[str, Sequence[str], None] = "78bc88f6ce70"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "problem_submissions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=100), nullable=False),
        sa.Column("language", sa.String(length=50), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "RECEIVED",
                "ACCEPTED",
                "WRONG_ANSWER",
                "RUNTIME_ERROR",
                "TIME_LIMIT_EXCEEDED",
                name="submissionstatus",
            ),
            nullable=False,
        ),
        sa.Column("score_percent", sa.Integer(), nullable=True),
        sa.Column("runtime_ms", sa.Integer(), nullable=True),
        sa.Column("memory_kb", sa.Integer(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_problem_submissions_problem_id"), "problem_submissions", ["problem_id"], unique=False)
    op.create_index(op.f("ix_problem_submissions_user_id"), "problem_submissions", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_problem_submissions_user_id"), table_name="problem_submissions")
    op.drop_index(op.f("ix_problem_submissions_problem_id"), table_name="problem_submissions")
    op.drop_table("problem_submissions")
    sa.Enum(name="submissionstatus").drop(op.get_bind(), checkfirst=True)

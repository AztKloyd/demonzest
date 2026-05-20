from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import QuestionType


class WrongAnswer(Base):
    __tablename__ = "wrong_answers"
    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_wrong_answers_user_question"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    lesson_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    question_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    wrong_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    last_wrong_answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_wrong_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

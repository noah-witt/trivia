import base64
from typing import TYPE_CHECKING
from pydantic import Field
from uuid import uuid4
from beanie import BackLink, Document
from pydantic import BaseModel
from pymongo import IndexModel
import secrets

if TYPE_CHECKING:
    from trivia.documents.response import ResponseDocument


class Question(BaseModel):
    question: str
    answers: list[str]
    correct: int


def key_factory() -> str:
    # 16 bytes of randomness
    return secrets.token_urlsafe(16)


class QuizInput(BaseModel):
    title: str
    questions: list[Question]


class Quiz(QuizInput, Document):
    key: str = Field(default_factory=key_factory)
    owner_email: str
    responses: list[BackLink["ResponseDocument"]] = Field(original_field="quiz")

    class Settings:
        collection_name = "quizzes"
        indexes = [IndexModel("key", unique=True)]

    @classmethod
    def from_input(cls, quiz_input: QuizInput, email: str) -> "Quiz":
        return cls(**quiz_input.model_dump(), owner_email=email)

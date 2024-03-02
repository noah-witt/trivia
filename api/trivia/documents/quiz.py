import base64
from pydantic import Field
from uuid import uuid4
from beanie import Document
from pydantic import BaseModel
from pymongo import IndexModel


class Question(Document):
    question: str
    answers: list[str]
    correct: int


def key_factory() -> str:
    # 128bit random number
    random = uuid4().int
    # 16 bytes
    random_bytes = random.to_bytes(16, "big")
    random_b64_bytes = base64.urlsafe_b64encode(random_bytes)
    return random_b64_bytes.decode("utf-8")


class QuizInput(BaseModel):
    title: str
    questions: list[Question]


class Quiz(QuizInput, Document):
    key: str = Field(default_factory=key_factory)
    owner_email: str

    class Settings:
        collection_name = "quizzes"
        indexes = [IndexModel("key", unique=True)]

    @classmethod
    def from_input(cls, quiz_input: QuizInput, email: str) -> "Quiz":
        return cls(**quiz_input.model_dump(), owner_email=email)

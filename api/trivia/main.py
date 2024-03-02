import logging
from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from trivia.auth.auth import User, get_current_active_user
from trivia.documents.quiz import Quiz, QuizInput
from trivia.documents.response import ResponseDocument

FORMAT = "%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOG = logging.getLogger(__name__)

app = FastAPI(
    title="trivia api",
    prefix="/api",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize services on startup."""
    import trivia.auth.endpoints as auth_endpoints
    from trivia.documents import initialize_db
    await initialize_db()


@app.get("/api")
async def root():
    return {"message": "Hello World"}


@app.put("/api/quiz")
async def put_quiz(
    current_user: Annotated[User, Depends(get_current_active_user)], quiz: QuizInput
):
    LOG.debug(f"quiz: {quiz}")
    record = Quiz.from_input(quiz, current_user.email)
    await record.save()
    return {"message": "Quiz created successfully"}


@app.get("/api/quiz/{key}")
async def get_quiz(key: str):
    record = await Quiz.find_one(Quiz.key == key)
    return record.model_dump()


class ResponseInput(BaseModel):
    responses: list[int]
    email: str
    name: str


@app.put("/api/quiz/{key}/answer")
async def put_responses(key: str, input: ResponseInput):
    # answer is a list of integers
    input = ResponseInput()
    quiz = await Quiz.find_one(Quiz.key == key)
    response = ResponseDocument(
        quiz=quiz, responses=input.responses, email=input.email, name=input.name
    )
    await response.save()

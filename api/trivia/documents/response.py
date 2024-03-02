
from beanie import Document, Link

from trivia.documents.quiz import Quiz


class ResponseDocument(Document):
    quiz: Link[Quiz]
    responses: list[int]
    email: str
    name: str

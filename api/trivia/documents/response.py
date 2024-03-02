from beanie import Document, Link
from pymongo import IndexModel
from trivia.documents.quiz import Quiz


class ResponseDocument(Document):
    quiz: Link[Quiz]
    responses: list[int]
    email: str
    name: str

    class Settings:
        indexes = [IndexModel("quiz", unique=False)]

    @property
    def score(self) -> int:
        correct = 0
        for i, response in enumerate(self.responses):
            if response == self.quiz.questions[i].correct:
                correct += 1
        return correct

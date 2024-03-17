from beanie import Document, Link
from pymongo import IndexModel
from trivia.documents.quiz import Quiz


class ResponseDocument(Document):
    quiz: Link[Quiz]
    responses: list[int]
    name: str
    _score: int | None = None  # _score is used as an index to store the score
    email: str | None = None

    class Settings:
        indexes = [
            IndexModel("quiz", unique=False),
            IndexModel(
                #
                "_score",
                partialFilterExpression={"_score": {"$exists": True}},
            ),
        ]

    def get_score(self) -> int:
        correct = 0
        for i, response in enumerate(self.responses):
            if response == self.quiz.questions[i].correct:
                correct += 1
        self._score = correct
        return correct

    @property
    def score(self) -> int:
        return self._score or self.get_score()

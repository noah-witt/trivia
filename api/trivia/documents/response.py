from beanie import Document, Link
from pymongo import IndexModel
from trivia.documents.quiz import Quiz


class ResponseDocument(Document):
    quiz: Link[Quiz]
    responses: list[int]
    email: str
    name: str
    _score: int | None = None  # _score is used as an index to store the score

    class Settings:
        indexes = [
            IndexModel("quiz", unique=False),
            IndexModel(
                #
                "_score",
                partialFilterExpression={"_score": {"$exists": True}},
            ),
        ]

    @property
    def score(self) -> int:
        correct = 0
        for i, response in enumerate(self.responses):
            if response == self.quiz.questions[i].correct:
                correct += 1
        self._score = correct
        return correct

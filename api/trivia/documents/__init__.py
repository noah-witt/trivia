import logging
from beanie import init_beanie

LOG = logging.getLogger("uvicorn.error")


async def initialize_db(*, db_url: str = "mongodb://mongo:27017/trivia"):
    from .quiz import Quiz
    from .response import ResponseDocument
    from ..auth.auth import UserInDB

    LOG.info("initializing db")
    DOCS = [Quiz, ResponseDocument, UserInDB]
    await init_beanie(
        document_models=DOCS,
        connection_string=db_url,
    )

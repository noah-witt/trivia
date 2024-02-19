import logging

from fastapi import FastAPI

FORMAT = "%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
LOG = logging.getLogger(__name__)

app = FastAPI(title="trivia api", prefix="/api")

@app.on_event("startup")
async def on_startup() -> None:
    """Initialize services on startup."""
    # import sfpdlog.auth.endpoints as auth_endpoints
    # import sfpdlog.endpoints as main_endpoints
    # import sfpdlog.score.endpoints as score_endpoints


@app.get("/api")
async def root():
    return {"message": "Hello World"}

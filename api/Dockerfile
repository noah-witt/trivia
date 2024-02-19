FROM python:3.11-bookworm as api
RUN mkdir -p /code/
COPY ./pyproject.toml ./pdm.lock /code/
WORKDIR /code
RUN PIP_DEFAULT_TIMEOUT=100 pip install pdm setuptools
RUN PIP_DEFAULT_TIMEOUT=100 pdm sync
COPY ./trivia /code/trivia
# COPY ./api/migrate.sh ./api/pytest.ini ./api/setup.cfg /code/
LABEL org.opencontainers.image.source https://github.com/noah-witt/trivia
ENTRYPOINT ["pdm", "run", "uvicorn", "trivia.main:app", "--reload", "--port", "80", "--host", "0.0.0.0", "--log-level", "debug"]

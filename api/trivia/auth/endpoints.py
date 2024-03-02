from datetime import timedelta
import functools
import logging
import os
from typing import Annotated

from fastapi import Depends, HTTPException

from trivia.auth.auth import authenticate_user
from ..main import app
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from .auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    CreateUser,
    Token,
    User,
    UserInDB,
    create_access_token,
    get_current_active_user,
)
import secrets

LOG = logging.getLogger("uvicorn.error")
LOG.warn("auth endpoints loaded")


@functools.cache
def get_secret_code() -> str:
    token_env = os.getenv("TOKEN_SECRET", None)
    if token_env:
        return token_env
    n = 30 * 3 // 4  # see note
    token = secrets.token_urlsafe(n)
    LOG.warning(f"Generated token: {token}")
    return token


@app.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/api/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.put("/api/users/add")
async def add_user(secret: str, user: CreateUser):
    if secret != get_secret_code():
        raise HTTPException(status_code=400, detail="Invalid secret")
    result = UserInDB.from_create_user(user)
    await result.save()
    return {
        "message": "User added successfully",
        "user": User.from_user_in_db(result).model_dump(),
    }

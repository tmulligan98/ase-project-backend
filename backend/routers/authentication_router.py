from fastapi import APIRouter, status, Depends, HTTPException, Response
from backend.authentication import (
    Token,
    create_access_token,
    authenticate_user,
    get_current_user,
)
from sqlalchemy.orm import Session
from backend.database_wrapper import get_db
from datetime import timedelta

from pydantic import BaseModel
from backend.utils import SETTINGS, init_logger
from typing import Dict

router = APIRouter()
logger = init_logger()


class AuthModel(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=dict)
async def login_for_access_token(
    body: AuthModel,
    response: Response,
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    """Route to fetch an access token, given a user email and password

    Parameters
    ----------
    body : AuthModel
        Body containing the Emergency Service Login details
    response : Response
        HTTP response
    db : Session, optional
        Current database session
    Returns
    -------
    _type_
        _description_

    Raises
    ------
    HTTPException
        _description_
    """

    user = authenticate_user(db, body.username, body.password)
    if not user:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=SETTINGS.auth_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires  # type: ignore
    )

    logger.info("Generated token...")

    # access_token = "123445656"

    return {"token": access_token}


@router.post("/users/me")
async def read_users_me(token: Token, db: Session = Depends(get_db)):
    return get_current_user(token.access_token, db=db)

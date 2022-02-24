from fastapi import APIRouter, status, Depends, HTTPException
from backend.authentication import Token, create_access_token, authenticate_user
from sqlalchemy.orm import Session
from backend.database_wrapper import get_db
from datetime import timedelta

from pydantic import BaseModel
from backend.utils import SETTINGS

router = APIRouter()


class AuthModel(BaseModel):
    username: str
    password: str


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: AuthModel,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=SETTINGS.auth_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires  # type: ignore
    )
    return {"access_token": access_token, "token_type": "bearer"}

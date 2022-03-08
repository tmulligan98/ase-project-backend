from datetime import timedelta, datetime
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend.database_wrapper import get_user_by_email, User
from typing import Optional
from backend.database_wrapper import SESSION_LOCAL
from .models import TokenData
from backend.utils import SETTINGS, verify_password
from typing import Union


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Function to create an access token, given a verified password

    Parameters
    ----------
    data : dict
        A dictionary containing the fields we want to encode (username)
    expires_delta : timedelta
        Variable to update the lifetime of the token

    Returns
    -------
    An encoded Javascript web token!

    """
    to_encode = data.copy()  # Takes a dictionary of userdata, copy it to be used
    if expires_delta:  # Update expiry time
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Add Field for expiry
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.auth_secret_key, algorithm=SETTINGS.crypto_algorithm
    )  # Create JWT from dict
    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str) -> Union[User, bool]:
    """Function to authenticate a user, given a database session, and user details

    Parameters
    ----------
    db : Session
        Database session
    email : str
        User email to verify
    password : str
        User password to verify

    Returns
    -------
    A user object from the database

    """
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str, db: SESSION_LOCAL) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, SETTINGS.auth_secret_key, algorithms=[SETTINGS.crypto_algorithm]
        )  # Decode user jwt token
        username: str = payload.get("sub")  # Get username
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(
        db=db, email=token_data.username
    )  # Username = email for now
    if user is None:
        raise credentials_exception
    return user

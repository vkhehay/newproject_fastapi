from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from resource import schemas
from resource import conf

SECRET_KEY = conf.settings.SECRET_KEY
ALGORITHM = conf.settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = conf.settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = playload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

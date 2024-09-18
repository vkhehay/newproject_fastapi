from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from resource import Token, db_config, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db_config.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={'WWW-Authenticate': "Bearer"},
    )

    token = Token.verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()

    return user

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from resource.db_config import get_db
from resource.hashing import Hash
from resource.Token import create_access_token

from resource import schemas, models

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.Login, db: Session = Depends(get_db)):
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.nickname == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Please input correct email')
    if not Hash.verify_pwd(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Incorrect password')

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

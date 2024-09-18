# from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from resource import schemas, db_config, models, hashing, oauth2

router = APIRouter(
    prefix='/user',
    tags=['USER'],
)


@router.post('/', response_model=schemas.PostUser)
def create_user(request: schemas.PostUser, db: Session = Depends(db_config.get_db)):
    password = hashing.Hash.bcrypt(request.password)
    request.password = password
    new_user = (models.User(**request.dict()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', status_code=status.HTTP_200_OK, response_model=schemas.GetUser)
def get_user_data(db: Session = Depends(db_config.get_db),
             current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user} not found')
    return user.first()


# @router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.GetUser)
# def get_user(user_id: int, db: Session = Depends(db_config.get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
#     return user.first()


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(db_config.get_db),
                current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id)
    user.delete(synchronize_session=False)
    db.commit()
    return {"message": 'User was delete'}

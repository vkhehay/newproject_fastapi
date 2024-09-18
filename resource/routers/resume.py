from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from resource import schemas, db_config, models, oauth2

router = APIRouter(
    prefix="/resume",
    tags=['Resume']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResume)
def create_resume(post: schemas.PostResume, db: Session = Depends(db_config.get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    resume = models.Resume(user_id=current_user.id, **post.dict())
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get('/', response_model=List[schemas.GetFullResume])
def get_all_resume(db: Session = Depends(db_config.get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    resume = db.query(models.Resume).filter(models.Resume.user_id == current_user.id).all()
    return resume


@router.get('/{id}', response_model=schemas.GetResume)
def get_resume_by_id(resume_id: int, db: Session = Depends(db_config.get_db),
                     current_user: int = Depends(oauth2.get_current_user)):
    resume_query = db.query(models.Resume).filter(models.Resume.id == resume_id)
    resume = resume_query.first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {resume_id} not found'
        )
    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="NOT AUTHORIZED TO PERFORM REQUEST")
    return resume


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: int, db: Session = Depends(db_config.get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    resume_query = db.query(models.Resume).filter(models.Resume.id == resume_id)
    resume = resume_query.first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {resume_id} not found'
        )
    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="NOT AUTHORIZED TO PERFORM REQUEST")
    resume_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f'Resume with id {resume_id} was deleted'}

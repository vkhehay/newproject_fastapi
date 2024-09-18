from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from resource import schemas, db_config, models, oauth2

router = APIRouter(
    prefix="/vacancy",
    tags=['Vacancy']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostVacancy)
def create_resume(post: schemas.PostVacancy, db: Session = Depends(db_config.get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    if current_user.id == 1:
        vacancy = models.Vacancies(**post.dict())
        db.add(vacancy)
        db.commit()
        db.refresh(vacancy)
        return vacancy
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You haven\'t administrator\'s rights')

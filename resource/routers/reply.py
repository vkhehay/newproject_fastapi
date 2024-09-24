from fastapi import APIRouter, Depends
from resource import schemas, db_config, models, oauth2
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, Session

router = APIRouter(
    prefix='/reply',
    tags=['Reply']
)


def vacancy_reply(vacancy_id: int, db=db_config.SessionFactory,
                  current_user: int = Depends(oauth2.get_current_user)):
    with db() as session:
        resume = select(models.Vacancies).filter(models.Vacancies.id == vacancy_id)
        res = session.execute(resume)
        result = res.scalar()
    return result


@router.post('/')
def reply_vacancy(resume_id: int, vacancy_id: int,
                  current_user: int = Depends(oauth2.get_current_user)):
    with db_config.SessionFactory() as session:
        resume_reply = session.get(models.Resume, resume_id)
        resume = resume_reply.vacancies_replied.append(vacancy_reply(vacancy_id))
        session.commit()
        return resume


def select_vacancy_reply(current_user: int = Depends(oauth2.get_current_user)):
    with db_config.SessionFactory() as session:
        query = (select(models.Resume, models.Resume.user_id)
                 .options(joinedload(models.Resume.worker))
                 .options(selectinload(models.Resume.vacancies_replied).load_only(models.Vacancies.title))
                 ).filter(models.Resume.user_id == current_user.id)
        res = session.execute(query)
        result_orm = res.unique().scalars().all()
        result_dto = [schemas.GetReply.model_validate(row, from_attributes=True) for row in result_orm]
        return result_dto


@router.get("/")
def get_resume(current_user: int = Depends(oauth2.get_current_user)):
    resume = select_vacancy_reply(current_user)
    print(resume)
    return resume

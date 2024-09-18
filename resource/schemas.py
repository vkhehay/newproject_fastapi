from typing import List
from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostUser(BaseModel):
    name: str
    nickname: str
    email: EmailStr
    phone: int
    password: str


class User(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_model = True


class Resume(BaseModel):
    position: str
    workload: str


class GetUser(User):
    resume: List[Resume]

    class Config:
        orm_model = True


class PostResume(BaseModel):
    position: str
    compensation: int
    workload: str


class GetFullResume(PostResume):
    created_at: datetime
    modified_at: datetime
    worker: User

    class Config:
        orm_model = True


class GetResume(Resume):
    worker: User

    class Config:
        orm_model = True


class Login(BaseModel):
    username: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | int


class PostVacancy(BaseModel):
    title: str
    compensation: int
    workload: str


class Vacancy(PostVacancy):
    pass


class GetReply(BaseModel):
    worker: "User"
    vacancies_replied: list["Vacancy"]


class Reply(BaseModel):
    pass

import enum
from typing import Optional, Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, text
from datetime import datetime

idpk = Annotated[int, mapped_column(primary_key=True, index=True, autoincrement=True)]
date_set = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[idpk]
    name: Mapped[str] = mapped_column(server_default="Ivan")
    nickname: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    phone: Mapped[int] = mapped_column(server_default=None)
    password: Mapped[str] = mapped_column(nullable=False)

    resume: Mapped[list["Resume"]] = relationship("Resume", back_populates="worker")


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[idpk]
    position: Mapped[str] = mapped_column(String, server_default="python developer")
    compensation: Mapped[Optional[int]] = mapped_column()
    workload: Mapped[Workload]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[date_set]
    modified_at: Mapped[date_set] = mapped_column(onupdate=datetime.now)

    worker = relationship("User", back_populates="resume")
    vacancies_replied: Mapped[list["Vacancies"]] = relationship(
        "Vacancies",
        back_populates="resumes_replied",
        secondary="vacancies_replies"
    )


class Vacancies(Base):
    __tablename__ = "vacancies"

    id: Mapped[idpk]
    title: Mapped[str]
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload] = mapped_column(nullable=True)

    resumes_replied: Mapped[list["Resume"]] = relationship(
        "Resume",
        back_populates='vacancies_replied',
        secondary="vacancies_replies")


class VacanciesReplies(Base):
    __tablename__ = 'vacancies_replies'

    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete='CASCADE'), primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete='CASCADE'), primary_key=True)


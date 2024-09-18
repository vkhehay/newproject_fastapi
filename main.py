# from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from resource import models
from resource.db_config import engine
from resource.routers import user, resume, vacancies, reply, authentic

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(authentic.router)
app.include_router(user.router)
app.include_router(resume.router)
app.include_router(vacancies.router)
app.include_router(reply.router)


@app.get('/', tags=["Main"])
def main():
    return {'message': 'hello work'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8888, reload=True)

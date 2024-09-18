from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from resource.conf import settings

engine = create_engine(url=settings.DATABASE_URL,
                       echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


# with engine.connect() as conn:
#     res = conn.execute(text("select id from users"))
#     print(f'{res}')

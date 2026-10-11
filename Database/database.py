from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(engine)

def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import (Column, Integer,
                        String, Boolean, DateTime)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email_id = Column(String(150), unique=True, nullable=False)
    verification_code = Column(String(150), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

engine = create_engine('postgresql://dbuser:users@localhost/users')


Base.metadata.create_all(engine)
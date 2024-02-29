from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime, Integer


Base = declarative_base()


class User(Base):
    __table_args__ = ({"schema": "auth"},)
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(256))
    password = Column(String(256))

    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now())
    deleted_at = Column(DateTime(timezone=False))


from sqlalchemy import Boolean, Column, Integer, String

from core.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_hash = Column(String(200), index=True)
    name = Column(String(20))
    nickname = Column(String(20))
    tone = Column(String(20))
    interview = Column(String(20))

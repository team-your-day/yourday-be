from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime

from core.db import Base
from core.utils.timezone import kst_now


class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    content = Column(Text)
    saved_at = Column(DateTime)
    created_at = Column(DateTime, default=kst_now)
    updated_at = Column(DateTime, default=kst_now, onupdate=kst_now)

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime

from core.db import Base
from core.utils.timezone import kst_now


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    diary_id = Column(String(20), index=True)
    content = Column(Text)
    is_ai = Column(Boolean, default=False)
    created_at = Column(DateTime, default=kst_now)

import hashlib
import json
from typing import Optional

from app.diary.models.diary import Diary
from app.diary.repositories.diary import DiaryRepository
from core.db import Transactional


class DiaryService:
    def __init__(self):
        self.diary_repo = DiaryRepository(Diary)

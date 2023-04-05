from fastapi import APIRouter

from api.chat.resources import chat_router
from api.diary.resources import diary_router
from api.user.resources import user_router

router = APIRouter()
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(diary_router, prefix="/diary", tags=["Diary"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])

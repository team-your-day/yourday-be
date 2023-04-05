import hashlib
import json
from typing import Optional

from app.user.enums.user import ToneEnum, InterviewTypeEnum
from app.user.models.user import User
from app.user.repositories.user import UserRepository
from app.user.schemas.user import UserSchema
from core.db import Transactional


class UserService:
    def __init__(self):
        self.user_repo = UserRepository(User)

    async def get_user_by_user_id(self, user_id: int) -> Optional[UserSchema]:
        return await self.user_repo.get_user(user_id)

    async def get_user_by_user_hash(self, user_hash: str) -> Optional[UserSchema]:
        return await self.user_repo.get_user_by_user_hash(user_hash)

    @Transactional()
    async def get_or_create_user(
        self,
        name: str,
        nickname: str,
        tone: ToneEnum,
        interview: InterviewTypeEnum,
    ) -> UserSchema:
        user_hash = str(hashlib.sha1(json.dumps(a, sort_keys=True).encode()).hexdigest())
        user = await self.user_repo.get_user_by_user_hash(user_hash)
        if user:
            return user

        return await self.user_repo.save_user(
            user_hash,
            name,
            nickname,
            tone,
            interview,
        )

    @Transactional()
    async def update_user_info(
        self,
        user_id: int,
        name: Optional[str],
        nickname: Optional[str],
        tone: Optional[ToneEnum],
        interview: Optional[InterviewTypeEnum],
    ) -> Optional[UserSchema]:
        return await self.user_repo.update_user_info(
            user_id,
            name,
            nickname,
            tone,
            interview,
        )

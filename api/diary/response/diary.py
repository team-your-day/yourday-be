from typing import List

from pydantic import BaseModel

from app.diary.schemas.diary import DiarySchema
from app.user.schemas.user import UserSchema
from core.utils.timezone import kst_now


class DiaryListResponse(BaseModel):
    diary: List[DiarySchema]

    class Config:
        schema_extra = {
            "example": {
                "diary": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "content": "맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다. 맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다.",
                        "created_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                ]
            }
        }


class DiaryResponse(BaseModel):
    diart: DiarySchema

    class Config:
        schema_extra = {
            "example": {
                "diary": {
                    "id": 1,
                    "user_id": 1,
                    "content": "맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다. 맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다. 페퍼로니 피자는 언제 먹어도 맛있다.맛있는 피자를 먹었다.",
                    "created_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": kst_now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            }
        }

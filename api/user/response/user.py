from pydantic import BaseModel

from app.user.schemas.user import UserSchema


class UserInfoResponse(BaseModel):
    user: UserSchema

    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "user_hash": "user_hash",
                    "name": "yunjae",
                    "nickname": "ai nickname",
                    "tone": "calm",
                    "interview": "low",
                },
            }
        }


class UserLoginResponse(BaseModel):
    user: UserSchema
    access_token: str

    class Config:
        schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "user_hash": "user_hash",
                    "name": "yunjae",
                    "nickname": "ai nickname",
                    "tone": "calm",
                    "interview": "low",
                },
                "access_token": "token"
            }
        }

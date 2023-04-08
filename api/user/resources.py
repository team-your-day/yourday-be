from fastapi import APIRouter, Path, Response, Depends, Body
from starlette.requests import Request

from api.user.request.user import SaveUserInfoRequest, UpdateUserInfoRequest
from api.user.response.user import UserInfoResponse, UserLoginResponse
from app.user.services.user import UserService
from core.exceptions import BadRequestException, UnauthorizedException, CustomException
from core.exceptions.schema import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.utils import TokenHelper

user_router = APIRouter()


@user_router.post(
    "/signup",
    response_model=UserLoginResponse,
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="유저 회원가입 API",
)
async def save_user(
    request: Request,
    body: SaveUserInfoRequest,
):
    """
    모든 값(name, nickname, tone, interview)이 동일한 유저가 있다면, create 하지 않고 access_token을 내려줍니다.
    """
    user = await UserService().get_or_create_user(
        body.name, body.nickname, body.tone, body.interview,
    )
    return {
        "user": user,
        "access_token": TokenHelper.encode(payload={"user_id": user.id})
    }


@user_router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="유저 로그인 API",
)
async def login_user(
    request: Request,
    user_hash: str = Body(..., description="유저 해시값"),
):
    user = await UserService().get_user_by_user_hash(user_hash)
    return {
        "user": user,
        "access_token": TokenHelper.encode(payload={"user_id": user.id})
    }


@user_router.get(
    "/info",
    response_model=UserInfoResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    summary="유저 정보 조회 API",
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
        401: {
            "description": UnauthorizedException.message,
            "model": ExceptionResponseSchema,
        },
    },
)
async def get_user_info(
    request: Request,
):
    user = await UserService().get_user_by_user_id(user_id=request.user.id)
    return {"user": user}


@user_router.patch(
    "/info",
    response_model=UserInfoResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    summary="유저 정보 수정 API",
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
        401: {
            "description": UnauthorizedException.message,
            "model": ExceptionResponseSchema,
        },
    },
)
async def update_user_info(request: Request, body: UpdateUserInfoRequest):
    user = await UserService().update_user_info(
        request.user.id,
        body.name,
        body.nickname,
        body.tone,
        body.interview,
    )
    return {"data": user}

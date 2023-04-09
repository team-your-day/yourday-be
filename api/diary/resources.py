from fastapi import APIRouter, Path, Response, Depends, Body
from starlette.requests import Request

from api.diary.request.diary import UpdateDiaryRequestSerializer
from api.diary.response.diary import DiaryResponse, DiaryListResponse
from app.diary.services.diary import DiaryService
from core.exceptions import BadRequestException, UnauthorizedException
from core.exceptions.schema import ExceptionResponseSchema
from core.fastapi.dependencies.permission import IsAuthenticated, PermissionDependency
from core.utils.timezone import kst_now

diary_router = APIRouter()


@diary_router.get(
    "/{month}/{day}",
    response_model=DiaryListResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="일기 조회 API",
)
async def get_diary(
    request: Request,
    month: str = Path(...),
    day: str = Path(..., description="0이면 해당 month의 데이터를 전체 조회합니다.")
):
    """
    day가 0이면 해당 month의 데이터를 전체 조회합니다.
    month는 0이 아닌 값이 들어와야 합니다.
    """
    diary_service = DiaryService()
    diary_list = await diary_service.get_diary(request.user.id, int(month), int(day))
    return {"diary": diary_list}


@diary_router.post(
    "/{month}/{day}",
    response_model=DiaryResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    responses={
        400: {
            "description": BadRequestException.message,
            "model": ExceptionResponseSchema,
        },
    },
    summary="일기 생성 API (채팅 완료 버튼 클릭 시 호출)",
)
async def create_diary(
    request: Request,
    month: str = Path(...),
    day: str = Path(...)
):
    diary_service = DiaryService()
    diary = await diary_service.create_diary(request.user.id, int(month), int(day))
    return {"diary": diary}


@diary_router.patch(
    "/{month}/{day}",
    response_model=DiaryResponse,
    dependencies=[
        Depends(PermissionDependency([IsAuthenticated]))
    ],
    summary="일기 수정 API",
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
async def update_diary(
    request: Request,
    month: str = Path(...),
    day: str = Path(...),
    body: UpdateDiaryRequestSerializer = Body(...)
):
    diary_service = DiaryService()
    diary = await diary_service.update_diary(
        request.user.id,
        int(month),
        int(day),
        body.content
    )
    return {"diary": diary}

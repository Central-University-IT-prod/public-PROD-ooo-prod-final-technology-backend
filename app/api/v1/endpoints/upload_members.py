from fastapi import APIRouter, status, BackgroundTasks

from core.config import Config
from core.dependencies import UOW
from core.dependencies import current_admin_or_error
from services.upload_members import UploadMembersService
from schemas.upload_members import UploadMembersRequest
from services.email_ import email_service

router = APIRouter(
    prefix="/upload-members",
    tags=["upload-members"],
)


@router.post('', status_code=status.HTTP_200_OK)
async def upload_members(
    uow: UOW,
    admin: current_admin_or_error,
    schema: UploadMembersRequest,
    background_task: BackgroundTasks,
):
    emails, event_title = await UploadMembersService().upload_members(uow, admin_id=admin.id, schema=schema)
    background_task.add_task(email_service.send_list,
                             emails,
                             event_title,
                             'Вас пригласили в олимпиаду',
                             f'Здравствуйте! Вас пригласили в олимпиаду {event_title}. Пожалуйста, скачайте '
                             f'приложение по ссылке: {Config.APP_URL}.')

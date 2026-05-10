from fastapi import HTTPException, status
from openapi_server.apis.notifications_api_base import BaseNotificationsApi
from openapi_server.models.notification_response import NotificationResponse
from openapi_server.models.send_draw_notifications_request import SendDrawNotificationsRequest

from app.db.session import AsyncSessionMaker
from app.repositories.event import EventRepository
from app.repositories.notification import NotificationRepository
from app.services.notification import NotificationService


class NotificationsApiImpl(BaseNotificationsApi):
    async def send_draw_notifications(
        self,
        send_draw_notifications_request: SendDrawNotificationsRequest,
    ) -> NotificationResponse:
        async with AsyncSessionMaker() as session:
            service = NotificationService(
                repository=NotificationRepository(session),
                event_repository=EventRepository(session),
            )

            event_id = getattr(send_draw_notifications_request, "event_id", None)
            if event_id is None:
                event_id = getattr(send_draw_notifications_request, "eventId", None)

            try:
                await service.send_draw_notifications(event_id)
            except ValueError as exc:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

        return NotificationResponse(
            success=True,
            message="Уведомления успешно отправлены",
        )

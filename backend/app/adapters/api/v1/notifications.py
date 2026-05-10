from openapi_server.apis.notifications_api_base import BaseNotificationsApi
from openapi_server.models.draw_results_notification_request import DrawResultsNotificationRequest
from openapi_server.models.notification_response import NotificationResponse

from app.services.notification import NotificationService


class NotificationsApiImpl(BaseNotificationsApi):
    def __init__(self) -> None:
        self._service = NotificationService()

    async def send_draw_results_notification(
        self,
        draw_results_notification_request: DrawResultsNotificationRequest,
    ) -> NotificationResponse:
        result = await self._service.send_draw_results_notification(draw_results_notification_request)
        return NotificationResponse.model_validate(result)

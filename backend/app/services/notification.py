from app.services.send_mails import send_email
from app.repositories.notification import NotificationRepository
from app.repositories.event import EventRepository


class NotificationService:
    """Business logic for notifications after draw."""

    def __init__(
        self,
        repository: NotificationRepository,
        event_repository: EventRepository,
    ) -> None:
        self._repository = repository
        self._event_repository = event_repository

    async def send_draw_notifications(self, event_id: int) -> None:
        event = await self._event_repository.get_by_id(event_id)
        if not event:
            raise ValueError(f"Event with id {event_id} not found")

        groups = await self._repository.get_notification_payload(event_id)

        for group in groups:
            topic = self._extract_topic(group)
            if not topic:
                continue

            recipients = self._extract_emails(group)
            if not recipients:
                continue

            requirements = self._extract_requirements(topic)

            subject = (
                f"[{event.name} {event.event_date.year}] "
                f"{group.name} - Результаты жеребьевки"
            )

            body = self._build_body(
                event_name=event.name,
                year=event.event_date.year,
                group_name=group.name,
                topic_name=topic.name,
                requirements=requirements,
            )

            for email in recipients:
                send_email(
                    to=email,
                    subject=subject,
                    body=body,
                )

    def _extract_topic(self, group):
        if not getattr(group, "group_topics", None):
            return None
        return group.group_topics[0].topic

    def _extract_emails(self, group):
        emails = []

        for gp in getattr(group, "group_participants", []):
            participant = getattr(gp, "participant", None)

            if not participant or not getattr(participant, "person", None):
                continue

            if not participant.is_notification_allowed:
                continue

            email = participant.person.email
            if email:
                emails.append(email)

        return list(set(emails))

    def _extract_requirements(self, topic):
        tr_list = getattr(topic, "technical_requirements", None)
        if not tr_list:
            return "Требования не указаны"

        tr = tr_list[0]

        parts = []

        if tr.format:
            parts.append(f"Формат: {tr.format}")

        if tr.sizes:
            parts.append(f"Размеры: {tr.sizes}")

        pc_list = getattr(tr, "posters_content", None)
        if pc_list:
            pc = pc_list[0]

            if pc.words_amount:
                parts.append(f"Количество слов: {pc.words_amount}")

            if pc.images_amount:
                parts.append(f"Количество изображений: {pc.images_amount}")

        return "\n".join(parts)

    def _build_body(
        self,
        event_name: str,
        year: int,
        group_name: str,
        topic_name: str,
        requirements: str,
    ) -> str:
        return f"""
Уведомление о результатах жеребьёвки

Мероприятие: {event_name}
Год проведения: {year}

Группа: {group_name}
Назначенная тема: {topic_name}

Технические требования:
{requirements}

Пожалуйста, ознакомьтесь с требованиями и приступайте к подготовке работы.
"""

"""
Юнит-тесты для NotificationService (бизнес-логика уведомлений)
Ветка: ZHER-15
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest


class TestNotificationService:
    """Тесты для NotificationService"""

    @pytest.fixture
    def mock_notification_repo(self):
        repo = Mock()
        repo.get_notification_payload = AsyncMock()
        return repo

    @pytest.fixture
    def mock_event_repo(self):
        repo = Mock()
        repo.get_by_id = AsyncMock()
        return repo

    @pytest.fixture
    def service(self, mock_notification_repo, mock_event_repo):
        from app.services.notification import NotificationService

        return NotificationService(repository=mock_notification_repo, event_repository=mock_event_repo)

    # TC-SRV-01: Успешная отправка
    @pytest.mark.asyncio
    async def test_srv01_send_success(self, service, mock_notification_repo, mock_event_repo):
        """Успешная отправка уведомлений"""
        # Arrange
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group()
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            # Act
            await service.send_draw_notifications(event_id=1)

            # Assert
            assert mock_send_email.call_count == 2

    # TC-SRV-02: Event не найден
    @pytest.mark.asyncio
    async def test_srv02_event_not_found(self, service, mock_event_repo):
        """Ошибка при отсутствии события"""
        mock_event_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Event with id 999 not found"):
            await service.send_draw_notifications(event_id=999)

    # TC-SRV-03: Группа без темы
    @pytest.mark.asyncio
    async def test_srv03_group_without_topic(self, service, mock_notification_repo, mock_event_repo):
        """Группа без темы пропускается"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = Mock()
        mock_group.group_topics = []
        mock_group.name = "No Topic Group"
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            mock_send_email.assert_not_called()

    # TC-SRV-04: Участник без email
    @pytest.mark.asyncio
    async def test_srv04_participant_without_email(self, service, mock_notification_repo, mock_event_repo):
        """Участник без email пропускается"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group()
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            assert mock_send_email.call_count == 2

    # TC-SRV-05: Дубликаты email
    @pytest.mark.asyncio
    async def test_srv05_duplicate_emails(self, service, mock_notification_repo, mock_event_repo):
        """Одинаковые email отправляются 1 раз"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        same_email = "duplicate@example.com"

        participant1 = self._create_mock_participant(email=same_email)
        participant2 = self._create_mock_participant(email=same_email)

        mock_group = self._create_mock_group()
        mock_group.group_participants = [
            self._create_mock_group_participant(participant1),
            self._create_mock_group_participant(participant2),
        ]
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            assert mock_send_email.call_count == 1

    # ========== Вспомогательные методы ==========

    def _create_mock_participant(self, email: str = "test@example.com", notification_allowed: bool = True):
        person = Mock()
        person.email = email
        participant = Mock()
        participant.person = person
        participant.is_notification_allowed = Mock(return_value=notification_allowed)
        return participant

    def _create_mock_group_participant(self, participant):
        gp = Mock()
        gp.participant = participant
        return gp

    def _create_mock_group(self):
        topic = Mock()
        topic.name = "Test Topic"
        topic.technical_requirements = []

        group_topic = Mock()
        group_topic.topic = topic

        participant1 = self._create_mock_participant(email="test1@example.com")
        participant2 = self._create_mock_participant(email="test2@example.com")

        gp1 = self._create_mock_group_participant(participant1)
        gp2 = self._create_mock_group_participant(participant2)

        group = Mock()
        group.name = "Test Group"
        group.group_topics = [group_topic]
        group.group_participants = [gp1, gp2]

        return group

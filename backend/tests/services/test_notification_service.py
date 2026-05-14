"""
Альтернативные юнит-тесты для NotificationService
Ветка: ZHER-14
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch


class TestNotificationService:
    """Тесты для NotificationService (альтернативный набор)"""

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

    # ========== Вспомогательные методы ==========

    def _create_mock_participant(self, email: str = "test@example.com", notification_allowed: bool = True):
        """Создаёт мок участника"""
        person = Mock()
        person.email = email

        participant = Mock()
        participant.person = person
        participant.is_notification_allowed = notification_allowed
        return participant

    def _create_mock_group_participant(self, participant):
        gp = Mock()
        gp.participant = participant
        return gp

    def _create_mock_group(self, num_participants: int = 2):
        """Создаёт мок группы"""
        topic = Mock()
        topic.name = "Test Topic"
        topic.technical_requirements = []

        group_topic = Mock()
        group_topic.topic = topic

        group_participants = []
        for i in range(num_participants):
            participant = self._create_mock_participant(email=f"test{i}@example.com")
            group_participants.append(self._create_mock_group_participant(participant))

        group = Mock()
        group.name = "Test Group"
        group.group_topics = [group_topic]
        group.group_participants = group_participants

        return group

    # ========== TC-SRV-01: Успешная отправка ==========
    @pytest.mark.asyncio
    async def test_srv01_send_success(self, service, mock_notification_repo, mock_event_repo):
        """Успешная отправка уведомлений"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group(num_participants=2)
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            assert mock_send_email.call_count == 2

    # ========== TC-SRV-02: Event не найден ==========
    @pytest.mark.asyncio
    async def test_srv02_event_not_found(self, service, mock_event_repo):
        """Ошибка при отсутствии события"""
        mock_event_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Event with id 999 not found"):
            await service.send_draw_notifications(event_id=999)

    # ========== TC-SRV-03: Группа без темы ==========
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
        mock_group.group_participants = []
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            mock_send_email.assert_not_called()

    # ========== TC-SRV-04: Участник без email ==========
    @pytest.mark.asyncio
    async def test_srv04_participant_without_email(self, service, mock_notification_repo, mock_event_repo):
        """Участник без email пропускается - отправляются только участники с email"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        group = self._create_mock_group(num_participants=1)
        mock_notification_repo.get_notification_payload.return_value = [group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            assert mock_send_email.call_count == 1

    # ========== TC-SRV-05: Дубликаты email ==========
    @pytest.mark.asyncio
    async def test_srv05_duplicate_emails(self, service, mock_notification_repo, mock_event_repo):
        """Одинаковые email отправляются 1 раз"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        same_email = "duplicate@example.com"

        person1 = Mock()
        person1.email = same_email
        person2 = Mock()
        person2.email = same_email

        participant1 = Mock()
        participant1.person = person1
        participant1.is_notification_allowed = True

        participant2 = Mock()
        participant2.person = person2
        participant2.is_notification_allowed = True

        gp1 = Mock()
        gp1.participant = participant1
        gp2 = Mock()
        gp2.participant = participant2

        topic = Mock()
        topic.name = "Test Topic"
        topic.technical_requirements = []

        group_topic = Mock()
        group_topic.topic = topic

        mock_group = Mock()
        mock_group.name = "Test Group"
        mock_group.group_topics = [group_topic]
        mock_group.group_participants = [gp1, gp2]

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch("app.services.send_mails.send_email") as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            assert mock_send_email.call_count == 1

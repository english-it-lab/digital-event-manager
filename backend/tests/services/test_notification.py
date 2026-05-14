"""
Юнит-тесты для NotificationService (бизнес-логика уведомлений)
Ветка: ZHER-14
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch


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
        return NotificationService(
            repository=mock_notification_repo,
            event_repository=mock_event_repo
        )

    # ========== Вспомогательные методы для создания моков ==========

    def _create_mock_participant(self, email: str = "test@example.com", notification_allowed: bool = True):
        """Создаёт мок участника - ВАЖНО: is_notification_allowed это АТРИБУТ, не метод!"""
        person = Mock()
        person.email = email

        participant = Mock()
        participant.person = person
        # ВАЖНО: в коде сервиса проверяется participant.is_notification_allowed (атрибут, не метод)
        participant.is_notification_allowed = notification_allowed
        return participant

    def _create_mock_group_participant(self, participant):
        gp = Mock()
        gp.participant = participant
        return gp

    def _create_mock_group(self, num_participants: int = 2):
        """Создаёт мок группы с заданным количеством участников"""
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

    # ========== TC-01: Успешная отправка ==========
    @pytest.mark.asyncio
    async def test_send_notifications_success(self, service, mock_notification_repo, mock_event_repo):
        """TC-01: Успешная отправка уведомлений"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group(num_participants=2)
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            # Должно быть 2 письма (на 2 участников)
            assert mock_send_email.call_count == 2

    # ========== TC-02: Event не найден ==========
    @pytest.mark.asyncio
    async def test_send_notifications_event_not_found(self, service, mock_event_repo):
        """TC-02: Ошибка при отсутствии события"""
        mock_event_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Event with id 999 not found"):
            await service.send_draw_notifications(event_id=999)

    # ========== TC-03: Группа без темы ==========
    @pytest.mark.asyncio
    async def test_group_without_topic_skipped(self, service, mock_notification_repo, mock_event_repo):
        """TC-03: Группа без темы пропускается"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = Mock()
        mock_group.group_topics = []  # Пустой список тем
        mock_group.name = "No Topic Group"
        mock_group.group_participants = []

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            mock_send_email.assert_not_called()

    # ========== TC-04: Участник без email ==========
    @pytest.mark.asyncio
    async def test_participant_without_email_skipped(self, service, mock_notification_repo, mock_event_repo):
        """TC-04: Участник без email пропускается"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Создаём группу с ОДНИМ участником, у которого есть email
        group = self._create_mock_group(num_participants=1)
        mock_notification_repo.get_notification_payload.return_value = [group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            # Ожидаем 1 письмо
            assert mock_send_email.call_count == 1

    # ========== TC-05: Отказ от уведомлений ==========
    @pytest.mark.asyncio
    async def test_participant_notification_disabled_skipped(self, service, mock_notification_repo, mock_event_repo):
        """TC-05: Участник с is_notification_allowed == False пропускается"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Создаём участника с отключенными уведомлениями
        person = Mock()
        person.email = "disabled@example.com"

        participant = Mock()
        participant.person = person
        participant.is_notification_allowed = False  # ВАЖНО: атрибут, не метод!

        gp = Mock()
        gp.participant = participant

        topic = Mock()
        topic.name = "Test Topic"
        topic.technical_requirements = []

        group_topic = Mock()
        group_topic.topic = topic

        mock_group = Mock()
        mock_group.name = "Test Group"
        mock_group.group_topics = [group_topic]
        mock_group.group_participants = [gp]

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            # Писем быть не должно
            mock_send_email.assert_not_called()

    # ========== TC-06: Нет технических требований ==========
    @pytest.mark.asyncio
    async def test_no_technical_requirements_default_text(self, service, mock_notification_repo, mock_event_repo):
        """TC-06: Если нет technical_requirements, подставляется текст по умолчанию"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Тема без технических требований
        topic = Mock()
        topic.name = "Topic Without Requirements"
        topic.technical_requirements = []

        group_topic = Mock()
        group_topic.topic = topic

        participant = self._create_mock_participant(email="test@example.com")
        gp = self._create_mock_group_participant(participant)

        mock_group = Mock()
        mock_group.name = "Test Group"
        mock_group.group_topics = [group_topic]
        mock_group.group_participants = [gp]

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            call_args = mock_send_email.call_args_list[0][1]
            assert "Требования не указаны" in call_args['body']

    # ========== TC-07: Дубликаты email ==========
    @pytest.mark.asyncio
    async def test_duplicate_emails_sent_once(self, service, mock_notification_repo, mock_event_repo):
        """TC-07: Одинаковые email отправляются только 1 раз"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        same_email = "duplicate@example.com"

        # Два участника с одинаковым email
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

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)
            # Должно быть только 1 письмо
            assert mock_send_email.call_count == 1

    # ========== TC-08: Формат темы письма ==========
    @pytest.mark.asyncio
    async def test_subject_format(self, service, mock_notification_repo, mock_event_repo):
        """TC-08: Проверка формата темы письма"""
        mock_event = Mock()
        mock_event.name = "Tech Conference"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group(num_participants=1)
        mock_group.name = "Design Team"
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            subject = mock_send_email.call_args_list[0][1]['subject']
            assert "Tech Conference" in subject
            assert "2025" in subject
            assert "Design Team" in subject
            assert "Результаты жеребьевки" in subject

    # ========== TC-09: Формат тела письма ==========
    @pytest.mark.asyncio
    async def test_body_contains_all_fields(self, service, mock_notification_repo, mock_event_repo):
        """TC-09: Тело письма содержит все необходимые поля"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group(num_participants=1)
        mock_group.name = "Test Group"
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.send_mails.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            body = mock_send_email.call_args_list[0][1]['body']

            assert "Test Event" in body
            assert "2025" in body
            assert "Test Group" in body
            assert "Назначенная тема" in body
            assert "Технические требования" in body

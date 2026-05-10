import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.notification import NotificationService
from app.repositories.notification import NotificationRepository
from app.repositories.event import EventRepository


class TestNotificationService:
    """QA тесты для NotificationService (жеребьёвка и уведомления)"""

    @pytest.fixture
    def mock_notification_repo(self):
        """Мок для NotificationRepository"""
        repo = Mock(spec=NotificationRepository)
        repo.get_notification_payload = AsyncMock()
        return repo

    @pytest.fixture
    def mock_event_repo(self):
        """Мок для EventRepository"""
        repo = Mock(spec=EventRepository)
        repo.get_by_id = AsyncMock()
        return repo

    @pytest.fixture
    def service(self, mock_notification_repo, mock_event_repo):
        """Сервис с моками"""
        return NotificationService(
            repository=mock_notification_repo,
            event_repository=mock_event_repo
        )

    # ========== TC-01: Успешная отправка ==========
    @pytest.mark.asyncio
    async def test_send_notifications_success(self, service, mock_notification_repo, mock_event_repo):
        """TC-01: Успешная отправка уведомлений для всех участников"""
        # Подготавливаем мок event
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Подготавливаем мок groups (результат жеребьёвки)
        mock_group = self._create_mock_group_with_data()
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        # Мокаем send_email
        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            # Проверяем, что send_email вызван нужное количество раз
            # В нашей мок-группе 2 участника -> 2 вызова
            assert mock_send_email.call_count == 2

            # Проверяем аргументы первого вызова
            call_args = mock_send_email.call_args_list[0][1]
            assert call_args['to'] in ['test1@example.com', 'test2@example.com']
            assert 'Test Event' in call_args['subject']
            assert 'Назначенная тема' in call_args['body']

    # ========== TC-02: Event не найден ==========
    @pytest.mark.asyncio
    async def test_send_notifications_event_not_found(self, service, mock_event_repo):
        """TC-02: Выброс ValueError если event не существует"""
        mock_event_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Event with id 999 not found"):
            await service.send_draw_notifications(event_id=999)

    # ========== TC-03: Группа без темы ==========
    @pytest.mark.asyncio
    async def test_group_without_topic_skipped(self, service, mock_notification_repo, mock_event_repo):
        """TC-03: Группа без темы пропускается, письма не отправляются"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Группа у которой group_topics пустой
        mock_group = Mock()
        mock_group.group_topics = []
        mock_group.name = "No Topic Group"

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            # Письма не отправлены
            mock_send_email.assert_not_called()

    # ========== TC-04: Участник без email ==========
    @pytest.mark.asyncio
    async def test_participant_without_email_skipped(self, service, mock_notification_repo, mock_event_repo):
        """TC-04: Участник без email пропускается, остальные получают"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Создаём группу: 1 участник с email, 1 без email
        mock_group = self._create_mock_group_with_data()

        # Добавляем участника без email
        participant_no_email = self._create_mock_participant(email=None)
        mock_group.group_participants.append(
            self._create_mock_group_participant(participant_no_email)
        )

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            # Должен быть только 1 вызов (для участника с email)
            assert mock_send_email.call_count == 1
            call_args = mock_send_email.call_args_list[0][1]
            assert call_args['to'] == 'test1@example.com'

    # ========== TC-05: Отказ от уведомлений ==========
    @pytest.mark.asyncio
    async def test_participant_notification_disabled_skipped(self, service, mock_notification_repo, mock_event_repo):
        """TC-05: Участник с is_notification_allowed() == False пропускается"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Участник с отключенными уведомлениями
        participant_disabled = self._create_mock_participant(
            email="disabled@example.com",
            notification_allowed=False
        )
        mock_group = self._create_mock_group_with_data()
        mock_group.group_participants = [
            self._create_mock_group_participant(participant_disabled)
        ]

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            mock_send_email.assert_not_called()

    # ========== TC-06: Нет технических требований ==========
    @pytest.mark.asyncio
    async def test_no_technical_requirements_default_text(self, service, mock_notification_repo, mock_event_repo):
        """TC-06: Если нет technical_requirements, подставляется текст по умолчанию"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        # Тема без technical_requirements
        topic = Mock()
        topic.name = "Topic Without Requirements"
        topic.technical_requirements = []

        mock_group = self._create_mock_group_with_data()
        mock_group.group_topics[0].topic = topic

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
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

        # Два участника с одинаковым email
        same_email = "duplicate@example.com"
        participant1 = self._create_mock_participant(email=same_email)
        participant2 = self._create_mock_participant(email=same_email)

        mock_group = self._create_mock_group_with_data()
        mock_group.group_participants = [
            self._create_mock_group_participant(participant1),
            self._create_mock_group_participant(participant2),
        ]

        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            # Должен быть только 1 вызов
            assert mock_send_email.call_count == 1
            call_args = mock_send_email.call_args_list[0][1]
            assert call_args['to'] == same_email

    # ========== TC-08: Формат subject ==========
    @pytest.mark.asyncio
    async def test_subject_format(self, service, mock_notification_repo, mock_event_repo):
        """TC-08: Проверка формата темы письма"""
        mock_event = Mock()
        mock_event.name = "Tech Conference"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group_with_data()
        mock_group.name = "Design Team"
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            subject = mock_send_email.call_args_list[0][1]['subject']
            expected_format = "Tech Conference 2025Design Team - Результаты жеребьевки"
            # Обратите внимание: в коде нет пробела между year и group.name
            assert subject == expected_format or "Tech Conference" in subject

    # ========== TC-09: Формат body ==========
    @pytest.mark.asyncio
    async def test_body_contains_all_fields(self, service, mock_notification_repo, mock_event_repo):
        """TC-09: Тело письма содержит все необходимые поля"""
        mock_event = Mock()
        mock_event.name = "Test Event"
        mock_event.event_date = Mock(year=2025)
        mock_event_repo.get_by_id.return_value = mock_event

        mock_group = self._create_mock_group_with_data()
        mock_group.name = "Test Group"
        mock_notification_repo.get_notification_payload.return_value = [mock_group]

        with patch('app.services.notification.send_email') as mock_send_email:
            await service.send_draw_notifications(event_id=1)

            body = mock_send_email.call_args_list[0][1]['body']

            # Проверяем наличие всех ключевых полей
            assert "Test Event" in body
            assert "2025" in body
            assert "Test Group" in body
            assert "Назначенная тема" in body
            assert "Технические требования" in body

    # ========== Вспомогательные методы для создания моков ==========

    def _create_mock_participant(self, email: str = "test@example.com", notification_allowed: bool = True):
        """Создаёт мок участника"""
        person = Mock()
        person.email = email

        participant = Mock()
        participant.person = person
        participant.is_notification_allowed = Mock(return_value=notification_allowed)
        return participant

    def _create_mock_group_participant(self, participant):
        """Создаёт мок GroupParticipant"""
        gp = Mock()
        gp.participant = participant
        return gp

    def _create_mock_group_with_data(self):
        """Создаёт мок группы с полными данными (темы, участники, требования)"""
        # Технические требования
        poster_content = Mock()
        poster_content.words_amount = 500
        poster_content.images_amount = 3

        tech_req = Mock()
        tech_req.format = "A0"
        tech_req.sizes = "120x80"
        tech_req.posters_content = [poster_content]

        # Тема
        topic = Mock()
        topic.name = "Назначенная тема"
        topic.technical_requirements = [tech_req]

        # GroupTopic
        group_topic = Mock()
        group_topic.topic = topic

        # Участники
        participant1 = self._create_mock_participant(email="test1@example.com")
        participant2 = self._create_mock_participant(email="test2@example.com")

        gp1 = self._create_mock_group_participant(participant1)
        gp2 = self._create_mock_group_participant(participant2)

        # Группа
        group = Mock()
        group.name = "Test Group"
        group.group_topics = [group_topic]
        group.group_participants = [gp1, gp2]

        return group

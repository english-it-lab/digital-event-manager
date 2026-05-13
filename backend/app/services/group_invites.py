from fastapi import HTTPException, status

from app.core.config import settings
from app.models import Group
from app.repositories.group import GroupRepository
from app.repositories.group_participant import GroupParticipantRepository
from app.repositories.participant import ParticipantRepository
from app.schemas import InviteTokenResponse
from app.services.jwt import JwtService


class GroupInviteService:
    GROUP_ID_KEY = "group_id"

    def __init__(
        self,
        jwt_service: JwtService,
        group_repository: GroupRepository,
        participant_repository: ParticipantRepository,
        group_participant_repository: GroupParticipantRepository,
    ) -> None:
        self._jwt_service = jwt_service
        self._group_repository = group_repository
        self._participant_repository = participant_repository
        self._group_participant_repository = group_participant_repository

    async def create_invite_token(self, group_id: int, person_id: int) -> InviteTokenResponse:
        participant = await self._group_participant_repository.get_participant_by_group_and_person(
            group_id=group_id, person_id=person_id
        )
        if participant is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not participant.is_group_leader:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        payload = {self.GROUP_ID_KEY: group_id}
        token = self._jwt_service.create_jwt(payload, settings.jwt_ttl_minutes)
        return InviteTokenResponse(token=token)

    async def join_by_token(self, token: str, person_id: int) -> Group:
        payload = self._jwt_service.decode_jwt(token)

        group = await self._group_repository.get_group_by_id(payload.get(self.GROUP_ID_KEY))
        await self._participant_repository.create_participant(person_id)
        group = await self._group_repository.increment_count(group)

        return group

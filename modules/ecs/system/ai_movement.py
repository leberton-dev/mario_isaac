from typing import override

from .base import System
from ..entity_manager import EntityManager
from ..component import VelocityComponent, TransformComponent, AIControlledComponent


class AIMovementSystem(System):
    def __init__(self, entity_manager: EntityManager, player_id: int) -> None:
        super().__init__(entity_manager)
        self._player_id: int = player_id

    @override
    def update(self) -> None:
        player_transform = self._entity_manager.get_component_from_entity(self._player_id, TransformComponent)
        assert isinstance(player_transform, TransformComponent)
        entities = self._entity_manager.get_entities_with_components([VelocityComponent, TransformComponent, AIControlledComponent])
        if len(entities) == 0:
            return
        for key in entities.keys():
            vel = self._entity_manager.get_component_from_entity(key, VelocityComponent)
            tra = self._entity_manager.get_component_from_entity(key, TransformComponent)
            assert isinstance(vel, VelocityComponent)
            assert isinstance(tra, TransformComponent)
            direction = self._get_direction(player_transform, tra)
            tra.x += direction[0]
            tra.y += direction[1]

    def _get_direction(self, player_transform: TransformComponent, ai_transform: TransformComponent) -> tuple[int, int]:
        dir_x = 0
        dir_y = 0
        if player_transform.x < ai_transform.x:
            dir_x = -1
        elif player_transform.x > ai_transform.x:
            dir_x = 1

        if player_transform.y < ai_transform.y:
            dir_y = -1
        elif player_transform.y > ai_transform.y:
            dir_y = 1

        return dir_x, dir_y



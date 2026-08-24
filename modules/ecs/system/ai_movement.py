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
        player_transform = self._entity_manager.get_component(self._player_id, TransformComponent)
        assert isinstance(player_transform, TransformComponent)
        entities = self._entity_manager.get_entities_with_components([VelocityComponent, TransformComponent, AIControlledComponent])
        if len(entities) == 0:
            return
        for key in entities.keys():
            velocity = self._entity_manager.get_component(key, VelocityComponent)
            transform = self._entity_manager.get_component(key, TransformComponent)
            assert isinstance(velocity, VelocityComponent)
            assert isinstance(transform, TransformComponent)
            direction = self._direction_to_player(player_transform, transform)
            transform.x += direction[0]
            transform.y += direction[1]

    def _direction_to_player(self, player_transform: TransformComponent, ai_transform: TransformComponent) -> tuple[int, int]:
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



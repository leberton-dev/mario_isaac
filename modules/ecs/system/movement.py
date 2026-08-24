from typing import override

from .base import System
from ..entity_manager import EntityManager
from ..component import VelocityComponent, TransformComponent


class MovementSystem(System):
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:
        entities = self._entity_manager.get_entities_with_components([VelocityComponent, TransformComponent])
        if len(entities) == 0:
            return
        for key in entities.keys():
            velocity = self._entity_manager.get_component(key, VelocityComponent)
            transform = self._entity_manager.get_component(key, TransformComponent)
            assert isinstance(velocity, VelocityComponent)
            assert isinstance(transform, TransformComponent)
            transform.x += velocity.vel_x
            transform.y += velocity.vel_y


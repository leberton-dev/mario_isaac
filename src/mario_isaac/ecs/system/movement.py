from typing import override

from ..component import TransformComponent, VelocityComponent
from ..entity_manager import EntityManager
from .base import System


class MovementSystem(System):
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:
        entities = self._entity_manager.get_entities_with_components([VelocityComponent, TransformComponent])
        if len(entities) == 0:
            return
        for key in entities:
            velocity = self._entity_manager.get_component(key, VelocityComponent)
            transform = self._entity_manager.get_component(key, TransformComponent)
            transform.x += velocity.vel_x
            transform.y += velocity.vel_y


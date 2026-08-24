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
            vel = self._entity_manager.get_component_from_entity(key, VelocityComponent)
            tra = self._entity_manager.get_component_from_entity(key, TransformComponent)
            assert isinstance(vel, VelocityComponent)
            assert isinstance(tra, TransformComponent)
            tra.x += vel.vel_x
            tra.y += vel.vel_y


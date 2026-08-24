import pygame
from typing import override

from .base import System
from ..entity_manager import EntityManager
from ..component import VelocityComponent

class InputSystem(System):
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:
        entities = self._entity_manager.get_entities_with_component(VelocityComponent)
        if len(entities) == 0:
            return
        keys = pygame.key.get_pressed()
        for key in entities.keys():
            vel = self._entity_manager.get_component_from_entity(key, VelocityComponent)
            assert isinstance(vel, VelocityComponent)
            vel.vel_x = vel.speed if keys[pygame.K_d] else -vel.speed if keys[pygame.K_a] else 0
            vel.vel_y = vel.speed if keys[pygame.K_s] else -vel.speed if keys[pygame.K_w] else 0


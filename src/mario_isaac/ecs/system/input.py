from typing import override

import pygame

from ..component import PlayerControlledComponent, VelocityComponent
from ..entity_manager import EntityManager
from .base import System


class InputSystem(System):
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:

        entities = self._entity_manager.get_entities_with_components([VelocityComponent, PlayerControlledComponent])
        if len(entities) == 0:
            return

        keys = pygame.key.get_pressed()
        for key in entities:

            velocity = self._entity_manager.get_component(key, VelocityComponent)

            velocity.vel_x = velocity.speed if keys[pygame.K_d] else -velocity.speed if keys[pygame.K_a] else 0
            velocity.vel_y = velocity.speed if keys[pygame.K_s] else -velocity.speed if keys[pygame.K_w] else 0


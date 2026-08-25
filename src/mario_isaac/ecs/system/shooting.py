from typing import override

import pygame

from mario_isaac.ecs.component import (
    CollisionComponent,
    ProjectileComponent,
    TransformComponent,
    VelocityComponent,
)
from mario_isaac.ecs.entity_manager import EntityManager
from mario_isaac.ecs.system.base import System


class ShootingSystem(System):
    FIRE_COOLDOWN_FRAMES: int = 15
    PROJECTILE_SPEED: int = 8
    PROJECTILE_DAMAGE: int = 1
    PROJECTILE_LIFETIME_FRAMES: int = 40
    PROJECTILE_SIZE: int = 8

    def __init__(self, entity_manager: EntityManager, player_id: int) -> None:
        super().__init__(entity_manager)
        self._player_id: int = player_id
        self._cooldown: int = 0

    @override
    def update(self) -> None:
        if self._cooldown > 0:
            self._cooldown -= 1

        direction = self._aim_direction()
        if direction is None or self._cooldown > 0:
            return

        self._spawn_projectile(direction)
        self._cooldown = self.FIRE_COOLDOWN_FRAMES

    def _aim_direction(self) -> tuple[float, float] | None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            return (1, 0)
        if keys[pygame.K_LEFT]:
            return (-1, 0)
        if keys[pygame.K_DOWN]:
            return (0, 1)
        if keys[pygame.K_UP]:
            return (0, -1)
        return None

    def _spawn_projectile(self, direction: tuple[float, float]) -> None:
        player_transform = self._entity_manager.get_component(self._player_id, TransformComponent)

        projectile_id = self._entity_manager.create_entity()
        self._entity_manager.add_component(
            projectile_id,
            TransformComponent(self.PROJECTILE_SIZE, self.PROJECTILE_SIZE, player_transform.x, player_transform.y)
        )
        self._entity_manager.add_component(
            projectile_id,
            VelocityComponent(int(direction[0] * self.PROJECTILE_SPEED), int(direction[1] * self.PROJECTILE_SPEED), self.PROJECTILE_SPEED)
        )
        self._entity_manager.add_component(projectile_id, CollisionComponent(self.PROJECTILE_SIZE, self.PROJECTILE_SIZE))
        self._entity_manager.add_component(projectile_id, ProjectileComponent(self.PROJECTILE_DAMAGE, self._player_id, self.PROJECTILE_LIFETIME_FRAMES))


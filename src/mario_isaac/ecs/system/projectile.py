from typing import TYPE_CHECKING, override

import pygame

from mario_isaac.core import TILE_SIZE
from mario_isaac.ecs.component import (
    CollisionComponent,
    HealthComponent,
    ProjectileComponent,
    TransformComponent,
)
from mario_isaac.ecs.entity_manager import EntityManager
from mario_isaac.ecs.system.base import System

if TYPE_CHECKING:
    from mario_isaac.room import RoomGrid


class ProjectileSystem(System):
    def __init__(self, entity_manager: EntityManager, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._room_grid: RoomGrid = room_grid

    @override
    def update(self) -> None:
        wall_rects = [pygame.Rect(pos.px_x, pos.px_y, TILE_SIZE, TILE_SIZE) for pos in self._room_grid.current_room.walls]

        for projectile_id in self._entity_manager.get_entities_with_component(ProjectileComponent):
            projectile = self._entity_manager.get_component(projectile_id, ProjectileComponent)
            transform = self._entity_manager.get_component(projectile_id, TransformComponent)
            collision = self._entity_manager.get_component(projectile_id, CollisionComponent)

            projectile.lifetime_frames -= 1
            if projectile.lifetime_frames <= 0:
                self._entity_manager.remove_entity(projectile_id)
                continue

            rect = pygame.Rect(transform.x, transform.y, collision.width, collision.height)

            if rect.collidelist(wall_rects) != -1:
                self._entity_manager.remove_entity(projectile_id)
                continue

            hit_enemy = self._find_hit_enemy(rect)
            if hit_enemy is not None:
                enemy_health = self._entity_manager.get_component(hit_enemy, HealthComponent)
                _ = enemy_health.damage(projectile.damage)
                if not enemy_health.alive:
                    self._entity_manager.remove_entity(hit_enemy)
                    self._room_grid.current_room.remove_enemy(hit_enemy)
                self._entity_manager.remove_entity(projectile_id)

    def _find_hit_enemy(self, rect: pygame.Rect) -> int | None:
        for enemy_id in self._room_grid.current_room.enemy_ids:
            enemy_transform = self._entity_manager.get_component(enemy_id, TransformComponent)
            enemy_collision = self._entity_manager.get_component(enemy_id, CollisionComponent)

            enemy_rect = pygame.Rect(enemy_transform.x, enemy_transform.y, enemy_collision.width, enemy_collision.height)
            if rect.colliderect(enemy_rect):
                return enemy_id

        return None






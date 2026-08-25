from typing import TYPE_CHECKING, override

import pygame

from ..component import CollisionComponent, TransformComponent, VelocityComponent
from ..entity_manager import EntityManager
from .base import System
from .collision_resolution import resolve_aabb_collision

if TYPE_CHECKING:
    from ...room import RoomGrid


class EntityCollisionSystem(System):
    def __init__(self, entity_manager: EntityManager, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._room_grid: RoomGrid = room_grid

    @override
    def update(self) -> None:
        entity_ids = list(self._room_grid.current_room.enemy_ids) 
        entity_rects = [self._entity_rect(entity_id) for entity_id in entity_ids]

        for idx, entity_id in enumerate(entity_ids):
            transform = self._entity_manager.get_component(entity_id, TransformComponent)
            velocity = self._entity_manager.get_component(entity_id, VelocityComponent)

            old_pos = (int(transform.x - velocity.vel_x), int(transform.y - velocity.vel_y))
            rect = entity_rects.pop(idx)

            transform.x, transform.y = resolve_aabb_collision(rect, old_pos, entity_rects)

            entity_rects.insert(idx, rect)

    def _entity_rect(self, entity_id: int) -> pygame.Rect:
        transform = self._entity_manager.get_component(entity_id, TransformComponent)
        collision = self._entity_manager.get_component(entity_id, CollisionComponent)
        return pygame.Rect(transform.x, transform.y, collision.width, collision.height)



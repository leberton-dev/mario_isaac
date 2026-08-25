from typing import TYPE_CHECKING, override

import pygame

from ...core import TILE_SIZE
from ..component import CollisionComponent, TransformComponent, VelocityComponent
from ..entity_manager import EntityManager
from .base import System
from .collision_resolution import resolve_aabb_collision

if TYPE_CHECKING:
    from ...room import RoomGrid


class WallCollisionSystem(System):
    def __init__(self, entity_manager: EntityManager, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._room_grid: RoomGrid = room_grid

    @override
    def update(self) -> None:
        wall_rects = [pygame.Rect(pos.px_x, pos.px_y, TILE_SIZE, TILE_SIZE) for pos in self._room_grid.current_room.walls]

        entities = self._entity_manager.get_entities_with_components([TransformComponent, VelocityComponent, CollisionComponent])
        for key in entities:
            transform = self._entity_manager.get_component(key, TransformComponent)
            velocity = self._entity_manager.get_component(key, VelocityComponent)
            collision = self._entity_manager.get_component(key, CollisionComponent)

            old_pos = (int(transform.x - velocity.vel_x), int(transform.y - velocity.vel_y))
            rect = pygame.Rect(transform.x, transform.y, collision.width, collision.height)

            transform.x, transform.y = resolve_aabb_collision(rect, old_pos, wall_rects)

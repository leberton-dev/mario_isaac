import pygame
from typing import override, TYPE_CHECKING

from .base import System
from ..entity_manager import EntityManager
from ..component import TransformComponent, VelocityComponent, CollisionComponent
if TYPE_CHECKING:
    from ...room import RoomGrid


class EntityCollisionSystem(System):
    def __init__(self, entity_manager: EntityManager, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._room_grid: "RoomGrid" = room_grid

    @override
    def update(self) -> None:
        entity_rects: list[pygame.Rect] = []
        entity_ids: list[int] = []

        for entity_id in self._room_grid.current_room.enemy_ids:

            entity_ids.append(entity_id)

            transform = self._entity_manager.get_component(entity_id, TransformComponent)
            collision = self._entity_manager.get_component(entity_id, CollisionComponent)
            assert isinstance(transform, TransformComponent)
            assert isinstance(collision, CollisionComponent)

            rect = pygame.Rect(transform.x, transform.y, collision.width, collision.height)
            entity_rects.append(rect)

        for idx, entity_id in enumerate(entity_ids):

            transform = self._entity_manager.get_component(entity_id, TransformComponent)
            velocity = self._entity_manager.get_component(entity_id, VelocityComponent)
            collision = self._entity_manager.get_component(entity_id, CollisionComponent)
            assert isinstance(transform, TransformComponent)
            assert isinstance(velocity, VelocityComponent)
            assert isinstance(collision, CollisionComponent)

            old_x = transform.x - velocity.vel_x
            old_y = transform.y - velocity.vel_y

            rect = entity_rects.pop(idx)
            if rect.collidelist(entity_rects) == -1:
                entity_rects.insert(idx, rect)
                continue

            rect_x_reverted = pygame.Rect(old_x, transform.y, collision.width, collision.height)
            rect_y_reverted = pygame.Rect(transform.x, old_y, collision.width, collision.height)

            if rect_x_reverted.collidelist(entity_rects) == -1:
                transform.x = old_x
            elif rect_y_reverted.collidelist(entity_rects) == -1:
                transform.y = old_y
            else:
                transform.x = old_x
                transform.y = old_y

            entity_rects.insert(idx, rect)

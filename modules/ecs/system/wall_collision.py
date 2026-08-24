import pygame
from typing import override, TYPE_CHECKING

from .base import System
from ..entity_manager import EntityManager
from ..component import TransformComponent, VelocityComponent
if TYPE_CHECKING:
    from ...room import RoomGrid


class WallCollisionSystem(System):
    def __init__(self, entity_manager: EntityManager, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._room_grid: "RoomGrid" = room_grid

    @override
    def update(self) -> None:
        walls_rect: list[pygame.Rect] = []
        for pos in self._room_grid.room.walls:
            walls_rect.append(pygame.Rect(pos.tiled_x, pos.tiled_y, 32, 32))
        entities = self._entity_manager.get_entities_with_components([TransformComponent, VelocityComponent])
        for key in entities.keys():
            transform = self._entity_manager.get_component_from_entity(key, TransformComponent)
            velocity = self._entity_manager.get_component_from_entity(key, VelocityComponent)
            assert isinstance(transform, TransformComponent)
            assert isinstance(velocity, VelocityComponent)

            old_x = transform.x - velocity.vel_x
            old_y = transform.y - velocity.vel_y
            rect = pygame.Rect(transform.x, transform.y, transform.width, transform.height)
            if rect.collidelist(walls_rect) == -1:
                continue

            rect_x_reverted = pygame.Rect(old_x, transform.y, transform.width, transform.height)
            rect_y_reverted = pygame.Rect(transform.x, old_y, transform.width, transform.height)

            if rect_x_reverted.collidelist(walls_rect) == -1:
                transform.x = old_x
            elif rect_y_reverted.collidelist(walls_rect) == -1:
                transform.y = old_y
            else:
                transform.x = old_x
                transform.y = old_y

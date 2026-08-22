from abc import ABC, abstractmethod
from typing import override, TYPE_CHECKING
import pygame

from .entity_manager import EntityManager
from .component import TransformComponent, VelocityComponent, SpriteComponent
if TYPE_CHECKING:
    from ..room import RoomGrid, Position


class System(ABC):
    def __init__(self, entity_manager: EntityManager) -> None:
        self._entity_manager: EntityManager = entity_manager

    @abstractmethod
    def update(self) -> None:
        pass

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

class RenderSystem(System):
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        entities = self._entity_manager.get_entities_with_components([TransformComponent, SpriteComponent])
        for key in entities.keys():
            tra = self._entity_manager.get_component_from_entity(key, TransformComponent)
            spr = self._entity_manager.get_component_from_entity(key, SpriteComponent)
            assert isinstance(tra, TransformComponent)
            assert isinstance(spr, SpriteComponent)
            _ = surface.blit(spr.sprites[spr.current_sprite][f"frame_{spr.current_frame}"], tra.pos)
            spr.set_next_frame()
            
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

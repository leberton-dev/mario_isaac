import math
from typing import TYPE_CHECKING, override

from ..component import (
    AIControlledComponent,
    CollisionComponent,
    TransformComponent,
    VelocityComponent,
)
from ..entity_manager import EntityManager
from .base import System

if TYPE_CHECKING:
    from ...room import RoomGrid


class AIMovementSystem(System):

    SEEK_WEIGHT: float = 1.0
    SEPARATION_WEIGHT: float = 1.5

    def __init__(self, entity_manager: EntityManager, player_id: int, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._player_id: int = player_id
        self._room_grid: RoomGrid = room_grid

    @override
    def update(self) -> None:

        player_transform = self._entity_manager.get_component(self._player_id, TransformComponent)
        assert isinstance(player_transform, TransformComponent)

        entities = self._entity_manager.get_entities_with_components([VelocityComponent, TransformComponent, AIControlledComponent, CollisionComponent])
        if len(entities) == 0:
            return

        for key in entities:

            velocity = self._entity_manager.get_component(key, VelocityComponent)
            transform = self._entity_manager.get_component(key, TransformComponent)
            collision = self._entity_manager.get_component(key, CollisionComponent)
            assert isinstance(velocity, VelocityComponent)
            assert isinstance(transform, TransformComponent)
            assert isinstance(collision, CollisionComponent)

            other_entities: list[int] = self._room_grid.current_room.enemy_ids + [self._player_id]
            other_entities.remove(key)

            push = self._separation_from_others(other_entities, transform, collision)
            direction = self._direction_to_player(player_transform, transform)

            velocity.vel_x = (direction[0] * self.SEEK_WEIGHT + push[0] * self.SEPARATION_WEIGHT)
            velocity.vel_y = (direction[1] * self.SEEK_WEIGHT + push[1] * self.SEPARATION_WEIGHT)

            magnitude = math.hypot(velocity.vel_x, velocity.vel_y)
            if magnitude > velocity.speed:
                velocity.vel_x = velocity.vel_x / magnitude * velocity.speed
                velocity.vel_y = velocity.vel_y / magnitude * velocity.speed

    def _direction_to_player(self, player_transform: TransformComponent, ai_transform: TransformComponent) -> tuple[float, float]:
        dx = player_transform.x - ai_transform.x
        dy = player_transform.y - ai_transform.y

        dist = math.hypot(dx, dy)
        if dist > 0:
            dx = dx / dist
            dy = dy / dist

        return dx, dy

    def _separation_from_others(self, other_entities: list[int], transform: TransformComponent, collision: CollisionComponent) -> tuple[float, float]:
        push_x: float = 0
        push_y: float = 0

        for other_id in other_entities:

            other_transform = self._entity_manager.get_component(other_id, TransformComponent)
            assert isinstance(other_transform, TransformComponent)

            other_x = other_transform.x - transform.x
            other_y = other_transform.y - transform.y

            distance = math.hypot(other_x, other_y) or 1
            overlap = collision.width - distance

            if overlap > 0:
                push_x -= (other_x / distance) * overlap
                push_y -= (other_y / distance) * overlap

        return push_x, push_y






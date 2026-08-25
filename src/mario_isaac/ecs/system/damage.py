import math
from typing import TYPE_CHECKING, override

from mario_isaac.ecs.component import (
    CollisionComponent,
    HealthComponent,
    TransformComponent,
)
from mario_isaac.ecs.entity_manager import EntityManager
from mario_isaac.ecs.system.base import System

if TYPE_CHECKING:
    from mario_isaac.room import RoomGrid


class DamageSystem(System):
    CONTACT_DAMAGE = 1

    def __init__(self, entity_manager: EntityManager, player_id: int, room_grid: "RoomGrid") -> None:
        super().__init__(entity_manager)
        self._player_id: int = player_id
        self._room_grid: RoomGrid = room_grid

    @override
    def update(self) -> None:
        for entity_id in self._entity_manager.get_entities_with_component(HealthComponent):
            health = self._entity_manager.get_component(entity_id, HealthComponent)
            health.tick_invulnerability()

        player_health = self._entity_manager.get_component(self._player_id, HealthComponent)
        player_transform = self._entity_manager.get_component(self._player_id, TransformComponent)
        player_collision = self._entity_manager.get_component(self._player_id, CollisionComponent)

        for enemy_id in self._room_grid.current_room.enemy_ids:
            enemy_transform = self._entity_manager.get_component(enemy_id, TransformComponent)
            enemy_collision = self._entity_manager.get_component(enemy_id, CollisionComponent)
            
            dx = enemy_transform.x - player_transform.x
            dy = enemy_transform.y - player_transform.y
            distance = math.hypot(dx, dy)

            contact_distance = (player_collision.width + enemy_collision.width) / 2
            if distance < contact_distance and player_health.damage(self.CONTACT_DAMAGE):
                # temporary console feedback
                print(f"Player hit! HP: {player_health.hp}/{player_health.max}")

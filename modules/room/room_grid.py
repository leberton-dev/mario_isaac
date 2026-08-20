import pygame

from .room import Room
from ..ecs import EntityManager, TransformComponent
from ..asset_manager import AssetManager

class RoomGrid:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager, player_id: int) -> None:
        self._asset_manager: AssetManager = asset_manager
        self._entity_manager: EntityManager = entity_manager
        self._player: int = player_id
        self._rooms: list[Room] = []
        self._create_rooms()

    @property
    def room(self) -> Room:
        return self._rooms[len(self._rooms) - 1]

    def _create_rooms(self) -> None:
        for _ in range(100):
            self._rooms.append(Room(self._asset_manager, self._entity_manager))

    def update(self) -> None:
        if self.room.doors_open and self._is_player_on_door():
            _ = self._rooms.pop()

    def draw(self, surface: pygame.Surface) -> None:
        self.room.draw(surface)

    def _is_player_on_door(self) -> bool:
        tra = self._entity_manager.get_component_from_entity(self._player, TransformComponent)
        assert isinstance(tra, TransformComponent)
        pos = tra.x // 32, tra.y // 32
        return self.room.is_on_door(pos)


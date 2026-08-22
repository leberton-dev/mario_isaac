import random
import pygame

from .room import Room
from ..ecs import EntityManager, TransformComponent
from ..asset_manager import AssetManager


_DIRECTIONS: dict[str, tuple[int ,int]] = {
    "left": (-1, 0),
    "right": (1, 0),
    "top": (0, -1),
    "bottom": (0, 1),
}

class RoomGrid:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager, player_id: int) -> None:
        self._asset_manager: AssetManager = asset_manager
        self._entity_manager: EntityManager = entity_manager
        self._player: int = player_id
        self._rooms: dict[tuple[int, int], Room] = {} 
        self._current_pos: tuple[int, int] = (0, 0)
        self._create_rooms()

    @property
    def room(self) -> Room:
        return self._rooms[self._current_pos]

    def _create_rooms(self) -> None:
        positions: set[tuple[int, int]] = {(0, 0)}
        frontier: list[tuple[int, int]] = [ (0, 0) ]
        room_count = 10

        while len(positions) < room_count and frontier:
            current = random.choice(frontier)
            direction = random.choice(list(_DIRECTIONS.values()))
            new_pos = (current[0] + direction[0], current[1] + direction[1])

            if new_pos in positions:
                continue

            positions.add(new_pos)
            frontier.append(new_pos)

            if random.random() < 0.5:
                frontier.remove(current)

        for pos in positions:
            doors: set[str] = set()
            for name, direction in _DIRECTIONS.items():
                neighbor = (pos[0] + direction[0], pos[1] + direction[1])
                if neighbor in positions:
                    doors.add(name)
            self._rooms[pos] = Room(self._asset_manager, self._entity_manager, doors)

    def update(self) -> None:
        if self.room.doors_open and self._is_player_on_door():
            direction = self._get_door_direction()
            self._current_pos = (self._current_pos[0] + direction[0], self._current_pos[1] + direction[1])
            self._place_player_on_door()

    def _get_door_direction(self) -> tuple[int, int]:
        tra = self._entity_manager.get_component_from_entity(self._player, TransformComponent)
        assert isinstance(tra, TransformComponent)
        pos = tra.x // 32, tra.y // 32
        if pos[0] == 0:
            return _DIRECTIONS["left"]
        elif pos[0] == 19:
            return _DIRECTIONS["right"]
        elif pos[1] == 0:
            return _DIRECTIONS["top"]
        else:
            return _DIRECTIONS["bottom"]

    def draw(self, surface: pygame.Surface) -> None:
        self.room.draw(surface)

    def _place_player_on_door(self) -> None:
        tra = self._entity_manager.get_component_from_entity(self._player, TransformComponent)
        assert isinstance(tra, TransformComponent)
        pos = tra.x // 32, tra.y // 32
        if pos[0] == 0:
            tra.x = 18 * 32
        elif pos[0] == 19:
            tra.x = 32
        elif pos[1] == 0:
            tra.y = 9 * 32
        elif pos[1] == 10:
            tra.y = 32

    def _is_player_on_door(self) -> bool:
        tra = self._entity_manager.get_component_from_entity(self._player, TransformComponent)
        assert isinstance(tra, TransformComponent)
        pos = tra.x // 32, tra.y // 32
        return self.room.is_on_door(pos)


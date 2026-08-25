import random

import pygame

from ..core import TILE_SIZE, AssetManager
from ..ecs import EntityManager, TransformComponent
from .room import Room

_DIR_OFFSETS: dict[str, tuple[int ,int]] = {
    "left": (-1, 0),
    "right": (1, 0),
    "top": (0, -1),
    "bottom": (0, 1),
}

_ROOM_COUNT = 10

class RoomGrid:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager, player_id: int) -> None:
        self._asset_manager: AssetManager = asset_manager
        self._entity_manager: EntityManager = entity_manager
        self._player_id: int = player_id
        self._rooms: dict[tuple[int, int], Room] = {} 
        self._room_pos: tuple[int, int] = (0, 0)
        self._create_rooms()

    @property
    def current_room(self) -> Room:
        return self._rooms[self._room_pos]

    def _create_rooms(self) -> None:
        positions: set[tuple[int, int]] = {(0, 0)}
        frontier: list[tuple[int, int]] = [ (0, 0) ]

        while len(positions) < _ROOM_COUNT and frontier:
            new_pos, origin_pos = self._next_room_pos(frontier)
            if new_pos in positions:
                continue

            positions.add(new_pos)
            frontier.append(new_pos)
            if random.random() < 0.5:
                frontier.remove(origin_pos)
        self._generate_rooms_with_doors(positions)

    def _generate_rooms_with_doors(self, positions: set[tuple[int, int]]) -> None:
        for room_pos in positions:
            doors: set[str] = set()
            for dir_name, offset in _DIR_OFFSETS.items():
                neighbor = (room_pos[0] + offset[0], room_pos[1] + offset[1])
                if neighbor in positions:
                    doors.add(dir_name)
            self._rooms[room_pos] = Room(self._asset_manager, self._entity_manager, doors)

    def _next_room_pos(self, frontier: list[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        origin = random.choice(frontier)
        offset = random.choice(list(_DIR_OFFSETS.values()))
        return (origin[0] + offset[0], origin[1] + offset[1]), origin

    def update(self) -> None:
        if self.current_room.doors_open and self._is_player_on_door():
            offset = self._get_door_direction()
            self._room_pos = (self._room_pos[0] + offset[0], self._room_pos[1] + offset[1])
            self._place_player_on_door()
            self._rooms[self._room_pos].create_enemies()

    def _get_door_direction(self) -> tuple[int, int]:
        transform = self._entity_manager.get_component(self._player_id, TransformComponent)
        tile_pos = transform.x // TILE_SIZE, transform.y // TILE_SIZE
        if tile_pos[0] == 0:
            return _DIR_OFFSETS["left"]
        elif tile_pos[0] == 19:
            return _DIR_OFFSETS["right"]
        elif tile_pos[1] == 0:
            return _DIR_OFFSETS["top"]
        else:
            return _DIR_OFFSETS["bottom"]

    def draw(self, surface: pygame.Surface) -> None:
        self.current_room.draw(surface)

    def _place_player_on_door(self) -> None:
        transform = self._entity_manager.get_component(self._player_id, TransformComponent)
        tile_pos = transform.x // TILE_SIZE, transform.y // TILE_SIZE
        if tile_pos[0] == 0:
            transform.x = 18 * TILE_SIZE
        elif tile_pos[0] == 19:
            transform.x = TILE_SIZE
        elif tile_pos[1] == 0:
            transform.y = 9 * TILE_SIZE
        elif tile_pos[1] == 10:
            transform.y = TILE_SIZE

    def _is_player_on_door(self) -> bool:
        transform = self._entity_manager.get_component(self._player_id, TransformComponent)
        tile_pos = transform.x // TILE_SIZE, transform.y // TILE_SIZE
        return self.current_room.is_on_door(tile_pos)


import pygame
import random
from typing import NamedTuple

from ..ecs import EntityManager, TransformComponent, SpriteComponent, VelocityComponent
from ..asset_manager import AssetManager

class Size(NamedTuple):
    width: int
    height: int

class Position(NamedTuple):
    x: int
    y: int

    @property
    def tup(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def tiled_tup(self) -> tuple[int, int]:
        return self.tiled_x, self.tiled_y

    @property
    def tiled_x(self) -> int:
        return self.x*32

    @property
    def tiled_y(self) -> int:
        return self.y*32

class Room:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager, doors_dir: set[str]) -> None:
        self._entity_manager: EntityManager = entity_manager
        self._asset_manager: AssetManager = asset_manager
        self._size: Size = Size(20, 11)
        self._textures: list[list[pygame.Surface]] = []
        self._doors: list[Position] = []
        self._doors_dir: set[str] = doors_dir
        self._enemies: list[int] = []
        self._walls: list[Position] = []
        self._spawned_enemies: bool = False
        self._design_room()
        self._create_doors()
        self._create_walls()

    @property
    def doors_open(self) -> bool:
        return len(self._enemies) == 0

    @property
    def walls(self) -> list[Position]:
        if self.doors_open:
            return self._walls
        return self._walls + self._doors

    @property
    def enemies_ids(self) -> list[int]:
        return self._enemies

    def create_enemies(self) -> None:
        if self._spawned_enemies:
            return

        enemy_count = random.randint(3, 6)
        for _ in range(enemy_count):
            id = self._entity_manager.create_entity()
            pos_x = random.randint(1, 18)
            pos_y = random.randint(1, 9)
            self._entity_manager.add_component(id, TransformComponent(32, 32, pos_x*32, pos_y*32))
            self._entity_manager.add_component(id, SpriteComponent(self._asset_manager.enemy_frames))
            self._entity_manager.add_component(id, VelocityComponent(0, 0, 2))
            self._enemies.append(id)
        self._spawned_enemies = True

    def _design_room(self) -> None:
        stone = self._asset_manager.room_frames["floor"]["stone_0"]
        stonebrick = self._asset_manager.room_frames["floor"]["stone_1"]
        for _ in range(self._size.width):
            row: list[pygame.Surface] = []
            for _ in range(self._size.height):
                row.append(random.choice([stone, stonebrick]))
            self._textures.append(row)

    def is_on_door(self, pos: tuple[int, int]) -> bool:
        # print(f"[DEBUG] Position = {pos} in {self._doors}")
        return pos in self._doors

    def _create_doors(self) -> None:
        if "left" in self._doors_dir:
            self._doors.append(Position(0, 5))
        if "right" in self._doors_dir:
            self._doors.append(Position(19, 5))
        if "top" in self._doors_dir:
            self._doors.append(Position(10, 0))
        if "bottom" in self._doors_dir:
            self._doors.append(Position(10, 10))

    def _create_walls(self) -> None:
        for x in range(self._size.width):
            for y in range(self._size.height):
                if (x == 0 or x == self._size.width - 1) and (x, y) not in self._doors:
                    self._walls.append(Position(x, y))
                elif (y == 0 or y == self._size.height - 1) and (x, y) not in self._doors:
                    self._walls.append(Position(x, y))

    def draw(self, surface: pygame.Surface) -> None:
        for x in range(self._size.width):
            for y in range(self._size.height):
                _ = surface.blit(self._textures[x][y], (x*32, y*32))
        for wall in self._walls:
            _ = surface.blit(self._asset_manager.room_frames["wall"]["first"], wall.tiled_tup)
        for door in self._doors:
            if self.doors_open:
                _ = surface.blit(self._asset_manager.room_frames["door"]["open"], door.tiled_tup)
            else:
                _ = surface.blit(self._asset_manager.room_frames["door"]["closed"], door.tiled_tup)

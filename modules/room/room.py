import pygame
import random

from ..ecs import EntityManager
from ..asset_manager import AssetManager

class Room:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager) -> None:
        self._entity_manager: EntityManager = entity_manager
        self._asset_manager: AssetManager = asset_manager
        self._size: tuple[int, int] = 20, 11
        self._textures: list[list[pygame.Surface]] = []
        self._doors: list[tuple[int, int]] = []
        self._enemies: list[int] = []
        self._design_room()
        self._create_doors()

    @property
    def doors_open(self) -> bool:
        return len(self._enemies) == 0

    def _design_room(self) -> None:
        stone = self._asset_manager.room_frames["floor"]["stone_0"]
        stonebrick = self._asset_manager.room_frames["floor"]["stone_1"]
        for _ in range(self._size[0]):
            row: list[pygame.Surface] = []
            for _ in range(self._size[1]):
                row.append(random.choice([stone, stonebrick]))
            self._textures.append(row)

    def is_on_door(self, pos: tuple[int, int]) -> bool:
        # print(f"[DEBUG] Position = {pos} in {self._doors}")
        return pos in self._doors

    def _create_doors(self) -> None:
        y = random.randint(4, 8)
        self._doors.append((0, y))
        self._doors.append((19, y))

        x = random.randint(10, 15)
        self._doors.append((x, 0))
        self._doors.append((x, 10))

    def draw(self, surface: pygame.Surface) -> None:
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                _ = surface.blit(self._textures[x][y], (x*32, y*32))
        for door in self._doors:
            if self.doors_open:
                _ = surface.blit(self._asset_manager.room_frames["door"]["open"], (door[0]*32, door[1]*32))
            else:
                _ = surface.blit(self._asset_manager.room_frames["door"]["closed"], (door[0]*32, door[1]*32))


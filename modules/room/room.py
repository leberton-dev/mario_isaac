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
        self._design_room()

    def _design_room(self) -> None:
        stone = self._asset_manager.room_frames["floor"]["stone_0"]
        stonebrick = self._asset_manager.room_frames["floor"]["stone_1"]
        for _ in range(self._size[0]):
            row: list[pygame.Surface] = []
            for _ in range(self._size[1]):
                row.append(random.choice([stone, stonebrick]))
            self._textures.append(row)

    def draw(self, surface: pygame.Surface) -> None:
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                _ = surface.blit(self._textures[x][y], (x*32, y*32))



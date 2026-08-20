import pygame
from ..ecs import EntityManager
from ..asset_manager import AssetManager

class Room:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager) -> None:
        self._entity_manager: EntityManager = entity_manager
        self._asset_manager: AssetManager = asset_manager
        self._size: tuple[int, int] = 20, 11

    def draw(self, surface: pygame.Surface) -> None:
        stone = self._asset_manager.room_frames["floor"]["stone_0"]
        for x in range(self._size[0]):
            for y in range(self._size[1]):
                _ = surface.blit(stone, (x*32, y*32))



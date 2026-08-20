import pygame

from ..ecs import EntityManager
from ..asset_manager import AssetManager
from .room import Room

class Floor:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager) -> None:
        self._current_room: Room = Room(asset_manager, entity_manager)

    def draw(self, surface: pygame.Surface) -> None:
        self._current_room.draw(surface)



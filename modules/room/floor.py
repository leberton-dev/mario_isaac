import pygame

from ..ecs import EntityManager, TransformComponent
from ..asset_manager import AssetManager
from .room import Room
from .room_grid import RoomGrid

class Floor:
    def __init__(self, asset_manager: AssetManager, entity_manager: EntityManager, player_id: int) -> None:
        self._asset_manager: AssetManager = asset_manager
        self._entity_manager: EntityManager = entity_manager
        self._room_grid: RoomGrid = RoomGrid(asset_manager, entity_manager, player_id)

    @property
    def room_grid(self) -> RoomGrid:
        return self._room_grid

    def draw(self, surface: pygame.Surface) -> None:
        self._room_grid.draw(surface)

    def update(self) -> None:
        self._room_grid.update()


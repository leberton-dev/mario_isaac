from pathlib import Path

import pygame

from .constants import TILE_SIZE

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

class AssetManager:
    def __init__(self) -> None:
        self.player_frames: dict[str, dict[str, pygame.Surface]] = {}
        self.room_frames: dict[str, dict[str, pygame.Surface]] = {}
        self.enemy_frames: dict[str, dict[str, pygame.Surface]] = {}
        self._init_player_frames()
        self._init_room_frames()
        self._init_enemy_frames()

    def _strip_from_sheet(self, sheet: pygame.Surface, origin: list[int], frame_size: list[int], columns: int, rows: int=1) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []

        for j in range(rows):
            for i in range(columns):
                location = (origin[0]+frame_size[0]*i, origin[1]+frame_size[1]*j)
                frames.append(sheet.subsurface(pygame.Rect(location, frame_size)))
        return frames

    def _init_player_frames(self) -> None:
        sheet: pygame.Surface = pygame.image.load(_ASSETS_DIR / "player" / "player.png").convert_alpha()
        idle: list[pygame.Surface] = self._strip_from_sheet(sheet, [0, 0], [32, 32], 2)

        self.player_frames["idle"] = {}
        self.player_frames["idle"]["frame_0"] = pygame.transform.scale(idle[0], (TILE_SIZE, TILE_SIZE))
        self.player_frames["idle"]["frame_1"] = pygame.transform.scale(idle[1], (TILE_SIZE, TILE_SIZE))

    def _init_enemy_frames(self) -> None:
        sheet: pygame.Surface = pygame.image.load(_ASSETS_DIR / "enemy.png").convert_alpha()
        idle: list[pygame.Surface] = self._strip_from_sheet(sheet, [0, 0], [16, 16], 3)

        self.enemy_frames["idle"] = {}
        self.enemy_frames["idle"]["frame_0"] = pygame.transform.scale(idle[0], (TILE_SIZE, TILE_SIZE))
        self.enemy_frames["idle"]["frame_1"] = pygame.transform.scale(idle[1], (TILE_SIZE, TILE_SIZE))
        self.enemy_frames["idle"]["frame_2"] = pygame.transform.scale(idle[2], (TILE_SIZE, TILE_SIZE))

    def _init_room_frames(self) -> None:
        stone = pygame.image.load(_ASSETS_DIR / "room" / "floor_stone.png").convert_alpha()
        stonebrick = pygame.image.load(_ASSETS_DIR / "room" / "stone_brick.png").convert_alpha()
        door_open = pygame.image.load(_ASSETS_DIR / "room" / "door_open.png").convert_alpha()
        door_closed = pygame.image.load(_ASSETS_DIR / "room" / "door_closed.png").convert_alpha()
        wall = pygame.image.load(_ASSETS_DIR / "room" / "wall.png").convert_alpha()

        self.room_frames["floor"] = {}
        self.room_frames["floor"]["stone_0"] = pygame.transform.scale(stone, (TILE_SIZE, TILE_SIZE))
        self.room_frames["floor"]["stone_1"] = pygame.transform.scale(stonebrick, (TILE_SIZE, TILE_SIZE))

        self.room_frames["door"] = {}
        self.room_frames["door"]["open"] = pygame.transform.scale(door_open, (TILE_SIZE, TILE_SIZE))
        self.room_frames["door"]["closed"] = pygame.transform.scale(door_closed, (TILE_SIZE, TILE_SIZE))

        self.room_frames["wall"] = {}
        self.room_frames["wall"]["first"] = pygame.transform.scale(wall, (TILE_SIZE, TILE_SIZE))

import pygame

class AssetManager:
    def __init__(self) -> None:
        self.player_frames: dict[str, dict[str, pygame.Surface]] = {}
        self.room_frames: dict[str, dict[str, pygame.Surface]] = {}
        self._init_player()
        self._init_room_frames()

    def _strip_from_sheet(self, sheet: pygame.Surface, origin: list[int], frame_size: list[int], columns: int, rows: int=1) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []

        for j in range(rows):
            for i in range(columns):
                location = (origin[0]+frame_size[0]*i, origin[1]+frame_size[1]*j)
                frames.append(sheet.subsurface(pygame.Rect(location, frame_size)))
        return frames

    def _init_player(self) -> None:
        sheet: pygame.Surface = pygame.image.load("assets/player/player.png").convert_alpha()
        idle: list[pygame.Surface] = self._strip_from_sheet(sheet, [0, 0], [16, 16], 3)

        self.player_frames["idle"] = {}
        self.player_frames["idle"]["frame_0"] = pygame.transform.scale(idle[0], (32, 32))
        self.player_frames["idle"]["frame_1"] = pygame.transform.scale(idle[1], (32, 32))
        self.player_frames["idle"]["frame_2"] = pygame.transform.scale(idle[2], (32, 32))

    def _init_room_frames(self) -> None:
        stone = pygame.image.load("assets/room/floor_stone.png").convert_alpha()
        stonebrick = pygame.image.load("assets/room/stone_brick.png").convert_alpha()
        door = pygame.image.load("assets/room/door.png").convert_alpha()

        self.room_frames["floor"] = {}
        self.room_frames["floor"]["stone_0"] = pygame.transform.scale(stone, (32, 32))
        self.room_frames["floor"]["stone_1"] = pygame.transform.scale(stonebrick, (32, 32))
        self.room_frames["door"] = {}
        self.room_frames["door"]["door"] = pygame.transform.scale(door, (32, 32))

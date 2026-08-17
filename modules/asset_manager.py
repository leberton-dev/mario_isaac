import pygame

class AssetManager:
    def __init__(self) -> None:
        self.player_frames: dict[str, dict[str, pygame.Surface]] = {}
        self._init_player()

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
        self.player_frames["idle"]["frame_1"] = idle[0]
        self.player_frames["idle"]["frame_2"] = idle[1]
        self.player_frames["idle"]["frame_3"] = idle[2]


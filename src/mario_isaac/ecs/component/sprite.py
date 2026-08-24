import pygame

from .base import Component


class SpriteComponent(Component):
    def __init__(self, sprites: dict[str, dict[str, pygame.Surface]]) -> None:
        self.sprites: dict[str, dict[str, pygame.Surface]] = sprites
        self.current_sprite: str = "idle"
        self.current_frame: int = 0
        self.last_frame_time: int = pygame.time.get_ticks()

    def set_next_frame(self) -> None:
        if pygame.time.get_ticks() > self.last_frame_time + 750:
            self.last_frame_time = pygame.time.get_ticks()
            self.current_frame += 1
            if self.current_frame >= len(self.sprites[self.current_sprite]):
                self.current_frame = 0


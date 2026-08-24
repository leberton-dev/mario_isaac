import pygame


class Button:
    def __init__(self, surface: pygame.Surface, width: int, height: int) -> None:
        self._surface: pygame.Surface = surface
        self._rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, width, height)

    def set_pos(self, x: int, y: int) -> None:
        self._rect.topleft = x,y

    def pressed(self, mouse: tuple[int, int]):
        return self._rect.collidepoint(mouse)

    def draw(self, color: pygame.Color) -> None:
        _ = pygame.draw.rect(self._surface, color, self._rect)

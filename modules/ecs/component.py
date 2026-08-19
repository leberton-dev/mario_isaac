from abc import ABC
import pygame

class Component(ABC):
    pass

class TransformComponent(Component):
    def __init__(self, width: int, height: int, x: int, y: int) -> None:
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

class VelocityComponent(Component):
    def __init__(self, vel_x: int, vel_y: int, speed: int) -> None:
        self.vel_x: int = vel_x
        self.vel_y: int = vel_y
        self.speed: int = speed

class SpriteComponent(Component):
    def __init__(self, sprites: dict[str, dict[str, pygame.Surface]]) -> None:
        self.sprites: dict[str, dict[str, pygame.Surface]] = sprites
        self.current_sprite: str = "idle"
        self.current_frame: int = 0

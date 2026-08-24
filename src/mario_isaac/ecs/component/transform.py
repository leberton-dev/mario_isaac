from .base import Component


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


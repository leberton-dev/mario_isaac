from .base import Component


class TransformComponent(Component):
    def __init__(self, width: int, height: int, x: float, y: float) -> None:
        self.width: int = width
        self.height: int = height
        self.x: float = x
        self.y: float = y

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y


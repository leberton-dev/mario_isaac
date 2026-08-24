from .base import Component


class CollisionComponent(Component):
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

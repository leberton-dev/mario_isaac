from .base import Component


class VelocityComponent(Component):
    def __init__(self, vel_x: int, vel_y: int, speed: int) -> None:
        self.vel_x: float = vel_x
        self.vel_y: float = vel_y
        self.speed: int = speed


from mario_isaac.ecs.component.base import Component


class ProjectileComponent(Component):
    def __init__(self, damage: int, owner: int, lifetime_frames: int) -> None:
        self.damage: int = damage
        self.owner: int = owner
        self.lifetime_frames: int = lifetime_frames

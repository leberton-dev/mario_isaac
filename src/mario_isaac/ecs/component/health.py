from mario_isaac.ecs.component.base import Component


class HealthComponent(Component):
    def __init__(self, max_hp: int, invulnerability_duration: int = 60) -> None:
        self._max_hp: int = max_hp
        self._current_hp: int = max_hp
        self._invulnerability_duration: int = invulnerability_duration
        self._invulnerability_frames: int = 0

    @property
    def hp(self) -> int:
        return self._current_hp

    @property
    def max(self) -> int:
        return self._max_hp

    @property
    def alive(self) -> bool:
        return self._current_hp > 0

    def damage(self, amount: int) -> bool:
        if self._invulnerability_frames > 0:
            return False

        self._current_hp = max(0, self._current_hp - amount)
        self._invulnerability_frames = self._invulnerability_duration
        return True

    def tick_invulnerability(self) -> None:
        if self._invulnerability_frames > 0:
            self._invulnerability_frames -= 1


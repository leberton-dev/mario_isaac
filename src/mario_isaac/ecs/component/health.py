from .base import Component


class HealthComponent(Component):
    INVULNERABILITY_FRAMES = 60

    def __init__(self, max_hp: int) -> None:
        self._max_hp: int = max_hp
        self._current_hp: int = max_hp
        self._invulnverability_frames: int = 0

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
        if self._invulnverability_frames > 0:
            return False

        self._current_hp = max(0, self._current_hp - amount)
        self._invulnverability_frames = self.INVULNERABILITY_FRAMES
        return True

    def tick_invulnerability(self) -> None:
        if self._invulnverability_frames > 0:
            self._invulnverability_frames -= 1


from typing import override

import pygame

from mario_isaac.core import AssetManager, Config, EventBus
from mario_isaac.scene.scene import Scene

RESUME_REQUESTED_EVENT_KEY = pygame.event.custom_type()


class PauseScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config) -> None:
        super().__init__(surface, asset_manager, bus, config)
        self._font: pygame.font.Font = pygame.font.Font(None, 24)

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._event_bus.emit(RESUME_REQUESTED_EVENT_KEY, {})

    @override
    def update(self) -> None:
        pass

    @override
    def draw(self) -> None:
        _ = self._surface.fill((30, 30, 30))
        text = self._font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=self._surface.get_rect().center)
        _ = self._surface.blit(text, rect)

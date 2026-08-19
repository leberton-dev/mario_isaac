import pygame
from typing import override

from .scene import Scene
from ..asset_manager import AssetManager
from ..event_bus import EventBus
from ..config import Config
from ..button import Button

PLAY_PRESSED_EVENT_KEY = pygame.event.custom_type()

class MenuScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config) -> None:
        super().__init__(surface, asset_manager, bus, config)
        self._play_button: Button = Button(self._surface, 500, 100)
        self._play_button.setCords(500, self._surface.get_size()[1] // 5)

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self._play_button.pressed(mouse):
                self._event_bus.emit(pygame.event.Event(PLAY_PRESSED_EVENT_KEY), {"scene": "hello"})

    @override
    def update(self) -> None:
        pass

    @override
    def draw(self) -> None:
        _ = self._surface.fill((0, 255, 0))
        self._play_button.draw(pygame.Color(255, 255, 255))


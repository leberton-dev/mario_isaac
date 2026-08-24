import pygame
from typing import override

from .scene import Scene
from ..core import AssetManager, Config, EventBus
from ..button import Button

PLAY_PRESSED_EVENT_KEY = pygame.event.custom_type()

class MenuScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config) -> None:
        super().__init__(surface, asset_manager, bus, config)
        screen_size = self._surface.get_size()
        width = screen_size[0]//2
        height = screen_size[1]//8
        self._play_button: Button = Button(self._surface, width, height)
        self._play_button.set_pos((screen_size[0] - width)//2, screen_size[1] // 6)

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._play_button.pressed(event.pos):
                self._event_bus.emit(PLAY_PRESSED_EVENT_KEY, {"scene": "hello"})

    @override
    def update(self) -> None:
        pass

    @override
    def draw(self) -> None:
        _ = self._surface.fill((0, 255, 0))
        self._play_button.draw(pygame.Color(255, 255, 255))


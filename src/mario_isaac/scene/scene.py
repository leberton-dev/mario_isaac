from abc import ABC, abstractmethod

import pygame

from ..core import AssetManager, Config, EventBus


class Scene(ABC):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config) -> None:
        self._surface: pygame.Surface = surface
        self._asset_manager: AssetManager = asset_manager
        self._event_bus: EventBus = bus
        self._config: Config = config

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


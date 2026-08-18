import pygame
from abc import ABC, abstractmethod
from .asset_manager import AssetManager
from .event_bus import EventBus
from .config import Config

PLAY_PRESSED_EVENT_KEY = pygame.event.custom_type()

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

class MenuScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config) -> None:
        super().__init__(surface, asset_manager, bus, config)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                self._event_bus.emit(pygame.event.Event(PLAY_PRESSED_EVENT_KEY), {"scene": "hello"})

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self._surface.fill((0, 255, 0))

class PlayScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config) -> None:
        super().__init__(surface, asset_manager, bus, config)
        self._asset_manager: AssetManager = asset_manager
        self._player_surf: pygame.Surface = self._asset_manager.player_frames["idle"]["frame_1"]
        self._player_rect: pygame.Rect = self._player_surf.get_rect()

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self._player_rect = self._player_rect.move(0, -10)
        elif keys[pygame.K_s]:
            self._player_rect = self._player_rect.move(0, 10)
        elif keys[pygame.K_a]:
            self._player_rect = self._player_rect.move(-10, 0)
        elif keys[pygame.K_d]:
            self._player_rect = self._player_rect.move(10, 0)

    def draw(self) -> None:
        _ = self._surface.fill((255, 0, 0))
        _ = self._surface.blit(self._player_surf, self._player_rect)

class SceneManager:
    def __init__(self) -> None:
        self._scenes: list[Scene] = []

    @property
    def scene(self) -> Scene:
        return self._scenes[len(self._scenes) - 1]

    def add(self, scene: Scene) -> None:
        self._scenes.append(scene)

    def pop(self) -> None:
        _ = self._scenes.pop()


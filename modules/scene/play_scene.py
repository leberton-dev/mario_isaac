import pygame
from typing import override

from .scene import Scene
from ..asset_manager import AssetManager
from ..event_bus import EventBus
from ..config import Config

from ..ecs import EntityManager, TransformComponent, VelocityComponent, SpriteComponent, System, MovementSystem, InputSystem, RenderSystem


class PlayScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config, entity_manager: EntityManager) -> None:
        super().__init__(surface, asset_manager, bus, config)
        self._asset_manager: AssetManager = asset_manager
        self._entity_manager: EntityManager = EntityManager()
        self._player: int = self._entity_manager.create_entity()
        self._entity_manager.add_component(self._player, TransformComponent(16, 16, 150, 150))
        self._entity_manager.add_component(self._player, VelocityComponent(0, 0, 5))
        self._entity_manager.add_component(self._player, SpriteComponent(self._asset_manager.player_frames))
        self._systems: list[System] = [MovementSystem(self._entity_manager), InputSystem(self._entity_manager)]
        self._drawSystem: RenderSystem = RenderSystem(self._entity_manager)

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @override
    def update(self) -> None:
        for system in self._systems:
            system.update()

    @override
    def draw(self) -> None:
        _ = self._surface.fill((255, 0, 0))
        self._drawSystem.draw(self._surface)



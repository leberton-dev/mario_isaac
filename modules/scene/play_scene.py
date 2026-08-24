import pygame
from typing import override

from .scene import Scene
from ..asset_manager import AssetManager
from ..event_bus import EventBus
from ..config import Config

from ..ecs import EntityManager, TransformComponent, VelocityComponent, SpriteComponent, System, MovementSystem, InputSystem, RenderSystem, WallCollisionSystem, PlayerControlledComponent
from ..room import Floor, Position


class PlayScene(Scene):
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager, bus: EventBus, config: Config, entity_manager: EntityManager) -> None:
        super().__init__(surface, asset_manager, bus, config)
        self._asset_manager: AssetManager = asset_manager
        self._entity_manager: EntityManager = EntityManager()
        self._player: int = self._entity_manager.create_entity()
        self._entity_manager.add_component(self._player, TransformComponent(32, 32, 150, 150))
        self._entity_manager.add_component(self._player, VelocityComponent(0, 0, 5))
        self._entity_manager.add_component(self._player, SpriteComponent(self._asset_manager.player_frames))
        self._entity_manager.add_component(self._player, PlayerControlledComponent())
        self._floor: Floor = Floor(self._asset_manager, self._entity_manager, self._player)
        self._systems: list[System] = [
            InputSystem(self._entity_manager),
            MovementSystem(self._entity_manager),
            WallCollisionSystem(self._entity_manager, self._floor.room_grid),
        ]
        self._render_system: RenderSystem = RenderSystem(self._entity_manager)

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @override
    def update(self) -> None:
        for system in self._systems:
            system.update()
        self._floor.update()

    @override
    def draw(self) -> None:
        _ = self._surface.fill((255, 0, 0))
        self._floor.draw(self._surface)
        self._render_system.draw(self._surface, [self._player] + self._floor.room_grid.room.enemies_ids)


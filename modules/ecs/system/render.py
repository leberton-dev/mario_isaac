import pygame
from typing import override

from .base import System
from ..entity_manager import EntityManager
from ..component import TransformComponent, SpriteComponent


class RenderSystem(System):
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        entities = self._entity_manager.get_entities_with_components([TransformComponent, SpriteComponent])
        for key in entities.keys():
            tra = self._entity_manager.get_component_from_entity(key, TransformComponent)
            spr = self._entity_manager.get_component_from_entity(key, SpriteComponent)
            assert isinstance(tra, TransformComponent)
            assert isinstance(spr, SpriteComponent)
            _ = surface.blit(spr.sprites[spr.current_sprite][f"frame_{spr.current_frame}"], tra.pos)
            spr.set_next_frame()
            

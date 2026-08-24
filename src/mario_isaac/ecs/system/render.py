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

    def draw(self, surface: pygame.Surface, entities_id: list[int]) -> None:
        entities = self._entity_manager.get_entities_with_components([TransformComponent, SpriteComponent])
        for key in entities.keys():
            if key not in entities_id:
                continue
            transform = self._entity_manager.get_component(key, TransformComponent)
            sprite = self._entity_manager.get_component(key, SpriteComponent)
            assert isinstance(transform, TransformComponent)
            assert isinstance(sprite, SpriteComponent)
            _ = surface.blit(sprite.sprites[sprite.current_sprite][f"frame_{sprite.current_frame}"], transform.pos)
            sprite.set_next_frame()
            

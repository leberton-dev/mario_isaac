from typing import override

import pygame

from mario_isaac.ecs.component import ProjectileComponent, TransformComponent
from mario_isaac.ecs.entity_manager import EntityManager
from mario_isaac.ecs.system.base import System


class ProjectileRenderSystem(System):
    RADIUS: int = 4
    COLOR: tuple[int, int, int] = (255, 255, 0)
    def __init__(self, entity_manager: EntityManager) -> None:
        super().__init__(entity_manager)

    @override
    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        for entity_id in self._entity_manager.get_entities_with_components([ProjectileComponent, TransformComponent]):
            transform = self._entity_manager.get_component(entity_id, TransformComponent)
            center = (int(transform.x), int(transform.y))
            _ = pygame.draw.circle(surface, self.COLOR, center, self.RADIUS)


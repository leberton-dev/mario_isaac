from typing import Any

import pygame

from .core import AssetManager, Config, EventBus
from .ecs import EntityManager
from .scene import PLAY_PRESSED_EVENT_KEY, MenuScene, PlayScene, SceneManager


def _on_play_pressed(data: dict[str, Any]) -> None:                                 # pyright: ignore[reportExplicitAny]
    print(f"play pressed, payload={data}")

def main() -> None:
    _ = pygame.init()

    config = Config()
    config.load()

    screen: pygame.Surface = pygame.display.set_mode(config.screen.size)
    virtual_screen: pygame.Surface = pygame.Surface(config.virtual_screen.size)
    scale = min(config.screen.width/config.virtual_screen.width, config.screen.height/config.virtual_screen.height)
    scaled_size = (int(config.virtual_screen.width * scale), int(config.virtual_screen.height * scale))
    offset = ((config.screen.width - scaled_size[0]) // 2, (config.screen.height - scaled_size[1]) // 2)
    running: bool = True
    clock = pygame.time.Clock()
    scene_manager = SceneManager()
    asset_manager = AssetManager()
    event_bus = EventBus()
    menu_scene: MenuScene = MenuScene(virtual_screen, asset_manager, event_bus, config)
    play_scene: PlayScene = PlayScene(virtual_screen, asset_manager, event_bus, config, EntityManager())
    scene_manager.add(menu_scene)
    event_bus.subscribe(PLAY_PRESSED_EVENT_KEY, _on_play_pressed)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == PLAY_PRESSED_EVENT_KEY:
                scene_manager.add(play_scene)
            else:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    event.pos = (int((event.pos[0] - offset[0]) / scale), int((event.pos[1] - offset[1]) / scale))
                scene_manager.current_scene.handle_event(event)
        
        scene_manager.current_scene.update()

        scene_manager.current_scene.draw()

        _ = screen.fill((0, 0, 0))
        scaled_virtual_screen: pygame.Surface = pygame.transform.scale(virtual_screen, scaled_size)
        _ = screen.blit(scaled_virtual_screen, offset)

        pygame.display.flip()

        _ = clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

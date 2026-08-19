import pygame
from .asset_manager import AssetManager
from .config import Config
from .event_bus import EventBus
from .scene import PlayScene, MenuScene, SceneManager, PLAY_PRESSED_EVENT_KEY
from typing import Any
from .ecs import EntityManager

def _say_hello(data: dict[str, Any]) -> None:
    print('Hello')

def main() -> None:
    _ = pygame.init()

    config = Config()
    config.load()

    screen: pygame.Surface = pygame.display.set_mode(config.screen.size)
    running: bool = True
    clock = pygame.time.Clock()
    scene_manager = SceneManager()
    asset_manager = AssetManager()
    event_bus = EventBus()
    menu_scene: MenuScene = MenuScene(screen, asset_manager, event_bus, config)
    play_scene: PlayScene = PlayScene(screen, asset_manager, event_bus, config, EntityManager())
    scene_manager.add(menu_scene)
    event_bus.subscribe(PLAY_PRESSED_EVENT_KEY, _say_hello)                         # pyright: ignore[reportArgumentType]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == PLAY_PRESSED_EVENT_KEY:
                scene_manager.add(play_scene)
            else:
                scene_manager.scene.handle_event(event)
        
        scene_manager.scene.update()

        scene_manager.scene.draw()
        pygame.display.flip()

        _ = clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

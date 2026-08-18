import pygame
from .asset_manager import AssetManager
from .config import Config
from .event_bus import EventBus
from .scene_manager import PlayScene, SceneManager

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
    play_scene: PlayScene = PlayScene(screen, asset_manager, event_bus, config)
    scene_manager.add(play_scene)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene_manager.scene.handle_event(event)
        
        scene_manager.scene.update()

        scene_manager.scene.draw()
        pygame.display.flip()

        _ = clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

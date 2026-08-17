import pygame
from .asset_manager import AssetManager
from .config import Config
from .event_bus import EventBus

moved_data = {"moved": False}

def _player_moved(data: dict[str, bool]) -> None:
    moved_data["moved"] = data["moved"]
    print(f"'moved_data' is set so {moved_data["moved"]}")

def main() -> None:
    _ = pygame.init()

    config = Config()
    config.load()

    screen: pygame.Surface = pygame.display.set_mode(config.screen.size)
    running: bool = True
    manager = AssetManager()
    player_surf = manager.player_frames["idle"]["frame_1"]
    player_rect = player_surf.get_rect()
    clock = pygame.time.Clock()

    bus = EventBus()
    moved_right_event = pygame.event.custom_type()
    bus.subscribe(moved_right_event, _player_moved)                                 # pyright: ignore[reportArgumentType]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            bus.emit(pygame.event.Event(moved_right_event), {"moved": True})
            player_rect = player_rect.move(0, -10)
        elif keys[pygame.K_s]:
            bus.emit(pygame.event.Event(moved_right_event), {"moved": True})
            player_rect = player_rect.move(0, 10)
        elif keys[pygame.K_a]:
            bus.emit(pygame.event.Event(moved_right_event), {"moved": True})
            player_rect = player_rect.move(-10, 0)
        elif keys[pygame.K_d]:
            bus.emit(pygame.event.Event(moved_right_event), {"moved": True})
            player_rect = player_rect.move(10, 0)
        else:
            bus.emit(pygame.event.Event(moved_right_event), {"moved": False})

        _ = screen.fill((0, 0, 0))
        _ = screen.blit(player_surf, player_rect)
        pygame.display.flip()
        _ = clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()

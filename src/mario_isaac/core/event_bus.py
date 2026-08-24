import pygame
from typing import Callable, Any


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[int, list[Callable[[dict[str, Any]], None]]] = {}     # pyright: ignore[reportExplicitAny]

    def subscribe(self, event_type: int, callback: Callable[[dict[str, Any]], None]) -> None:  # pyright: ignore[reportExplicitAny]
        self._listeners.setdefault(event_type, []).append(callback)

    def emit(self, event_type: int, payload: dict[str, Any]) -> None:               # pyright: ignore[reportExplicitAny]
        for callback in self._listeners.get(event_type, []):
            callback(payload)
        _ = pygame.event.post(pygame.event.Event(event_type, **payload))            # pyright: ignore[reportAny]


import pygame
from typing import Callable, Any


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[int, list[Callable[[pygame.event.Event], None]]] = {}

    def subscribe(self, event_type: int, callback: Callable[[pygame.event.Event], None]) -> None:
        self._listeners.setdefault(event_type, []).append(callback)

    def emit(self, event: pygame.event.Event, payload: dict[str, Any]) -> None:     # pyright: ignore[reportExplicitAny]
        for callback in self._listeners.get(event.type, []):
            callback(payload)                                                       # pyright: ignore[reportArgumentType]





from abc import ABC, abstractmethod

from ..entity_manager import EntityManager


class System(ABC):
    def __init__(self, entity_manager: EntityManager) -> None:
        self._entity_manager: EntityManager = entity_manager

    @abstractmethod
    def update(self) -> None:
        pass


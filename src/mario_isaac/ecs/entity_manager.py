from typing import cast

from .component import Component


class EntityManager:
    def __init__(self) -> None:
        self._last: int = 0
        self._entities: set[int] = set()
        self._components: dict[type[Component], dict[int, Component]] = {}

    @property
    def last(self) -> int:
        return self._last

    def create_entity(self) -> int:
        self._last += 1
        self._entities.add(self._last)
        return self._last

    def add_component(self, entity: int, component: Component) -> None:
        if entity not in self._entities:
            return 
        self._components.setdefault(type(component), {})[entity] = component


    def get_component[T: Component](self, entity: int, comp_type: type[T]) -> T:
        try:
            component = self._components[comp_type][entity]
        except KeyError:
            raise ValueError("Component does not exist in the EntityManager")
        return cast(T, component)

    def get_entities_with_component(self, comp_type: type[Component]) -> list[int]:
        return list(self._components.get(comp_type, {}))

    def get_entities_with_components(self, comp_types: list[type[Component]]) -> list[int]:
        if not comp_types:
            return []
        entity_sets = [set(self._components.get(comp_type, {})) for comp_type in comp_types]
        return list(set.intersection(*entity_sets))

    def remove_entity(self, entity_id: int) -> None:
        self._entities.discard(entity_id)
        for components in self._components.values():
            components.pop(entity_id, None)



from .component import Component


class EntityManager:
    def __init__(self) -> None:
        self._last: int = 0
        self._components: dict[int, list[Component]] = {}

    @property
    def last(self) -> int:
        return self._last

    def create_entity(self) -> int:
        self._last += 1
        self._components[self._last] = []
        return self._last

    def add_component(self, entity: int, component: Component) -> None:
        if entity > self._last:
            return 

        components = self._components[entity]
        if component not in components:
            self._components[entity].append(component)

    def get_component(self, entity: int, comp_type: type[Component]) -> Component:
        for comp in self._components[entity]:
            if isinstance(comp, comp_type):
                return comp
        raise ValueError("Component does not exist in the EntityManager")

    def get_entities_with_component(self, component: type[Component]) -> dict[int, list[Component]]:
        entities: dict[int, list[Component]] = {}
        for key, value in self._components.items():
            if any(isinstance(val, component) for val in value):
                entities[key] = value
        return entities

    def get_entities_with_components(self, components: list[type[Component]]) -> dict[int, list[Component]]:
        entities: dict[int, list[Component]] = {}
        for key, value in self._components.items():
            if all(any(isinstance(val, comp_type) for val in value) for comp_type in components):
                entities[key] = value
        return entities

    def remove_entity(self, entity_id: int) -> None:
        _ = self._components.pop(entity_id, None)



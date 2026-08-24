import pytest

from mario_isaac.ecs.component import TransformComponent, VelocityComponent
from mario_isaac.ecs.entity_manager import EntityManager


def test_create_entity_returns_incrementing_ids():
    manager = EntityManager()
    assert manager.create_entity() == 1
    assert manager.create_entity() == 2


def test_add_and_get_component():
    manager = EntityManager()
    entity = manager.create_entity()
    transform = TransformComponent(32, 32, 0, 0)
    manager.add_component(entity, transform)

    assert manager.get_component(entity, TransformComponent) is transform


def test_get_component_raises_when_missing():
    manager = EntityManager()
    entity = manager.create_entity()

    with pytest.raises(ValueError):
        _ = manager.get_component(entity, TransformComponent)


def test_add_component_ignores_unknown_entity():
    manager = EntityManager()
    manager.add_component(999, TransformComponent(32, 32, 0, 0))
    # no exception expected -- add_component silently no-ops for an
    # entity id that was never created ( entity > self._last )


def test_add_component_does_not_duplicate_same_instance():
    manager = EntityManager()
    entity = manager.create_entity()
    transform = TransformComponent(32, 32, 0, 0)

    manager.add_component(entity, transform)
    manager.add_component(entity, transform)

    entities = manager.get_entities_with_component(TransformComponent)
    assert len(entities) == 1


def test_get_entities_with_component_filters_correctly():
    manager = EntityManager()
    with_transform = manager.create_entity()
    manager.add_component(with_transform, TransformComponent(32, 32, 0, 0))

    without_transform = manager.create_entity()
    manager.add_component(without_transform, VelocityComponent(0, 0, 5))

    result = manager.get_entities_with_component(TransformComponent)

    assert with_transform in result
    assert without_transform not in result


def test_remove_entity():
    manager = EntityManager()
    entity = manager.create_entity()
    manager.add_component(entity, TransformComponent(32, 32, 0, 0))

    manager.remove_entity(entity)

    assert manager.get_entities_with_component(TransformComponent) == {}


@pytest.mark.xfail(reason="add_component crashes with KeyError after remove_entity", strict=True)
def test_add_component_after_remove_entity_does_not_crash():
    manager = EntityManager()
    entity = manager.create_entity()
    manager.remove_entity(entity)

    manager.add_component(entity, TransformComponent(32, 32, 0, 0))


import pygame

from mario_isaac.ecs.system.collision_resolution import resolve_aabb_collision


def test_no_collision_keep_new_position():
    rect = pygame.Rect(10, 0, 4, 4)

    result = resolve_aabb_collision(rect, old_pos=(0, 0), obstacles=[])
    assert result == (10, 0)


def test_collision_reverts_x_when_x_axis_is_the_problem():
    rect = pygame.Rect(10, 10, 4, 4)
    obstacle = pygame.Rect(10, 10, 4, 4)

    result = resolve_aabb_collision(rect, old_pos=(0, 10), obstacles=[obstacle])
    assert result == (0, 10)


def test_collision_reverts_y_when_y_axis_is_the_problem():
    rect = pygame.Rect(10, 10, 4, 4)
    obstacle = pygame.Rect(0, 10, 20, 4)

    result = resolve_aabb_collision(rect, old_pos=(10, 0), obstacles=[obstacle])
    assert result == (10, 0)


def test_collision_reverts_both_axes_when_neither_alone_resolves_it():
    rect = pygame.Rect(10, 10, 4, 4)
    obstacle = pygame.Rect(0, 0, 20, 20)

    result = resolve_aabb_collision(rect, old_pos=(0, 0), obstacles=[obstacle])
    assert result == (0, 0)


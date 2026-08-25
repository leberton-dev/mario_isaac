import pygame


def resolve_aabb_collision(
        rect: pygame.Rect,
        old_pos: tuple[float, float],
        obstacles: list[pygame.Rect]
    ) -> tuple[float, float]:

    if rect.collidelist(obstacles) == -1:
        return rect.x, rect.y

    old_x, old_y = old_pos
    rect_x_reverted = pygame.Rect(old_x, rect.y, rect.width, rect.height)
    rect_y_reverted = pygame.Rect(rect.x, old_y, rect.width, rect.height)

    if rect_x_reverted.collidelist(obstacles) == -1:
        return old_x, rect.y
    elif rect_y_reverted.collidelist(obstacles) == -1:
        return rect.x, old_y
    else:
        return old_x, old_y

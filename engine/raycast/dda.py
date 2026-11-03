from __future__ import annotations

import math

from ..maths.constants import EPS
from ..world.grid import Grid
from .hit import Hit
from .ray import Ray


def cast(grid: Grid, ray: Ray, max_steps: int | None = None) -> Hit | None:
    n = grid.n
    cells = grid.cells
    solid = grid.solid
    if max_steps is None:
        max_steps = 2 * n + 4

    px, py = ray.ox, ray.oy
    dx = ray.dx if abs(ray.dx) > EPS else EPS
    dy = ray.dy if abs(ray.dy) > EPS else EPS

    map_x = int(px)
    map_y = int(py)
    delta_x = abs(1.0 / dx)
    delta_y = abs(1.0 / dy)

    if dx < 0:
        step_x = -1
        side_x = (px - map_x) * delta_x
    else:
        step_x = 1
        side_x = (map_x + 1.0 - px) * delta_x
    if dy < 0:
        step_y = -1
        side_y = (py - map_y) * delta_y
    else:
        step_y = 1
        side_y = (map_y + 1.0 - py) * delta_y

    side = 0
    hit = False
    for _ in range(max_steps):
        if side_x < side_y:
            side_x += delta_x
            map_x += step_x
            side = 0
        else:
            side_y += delta_y
            map_y += step_y
            side = 1
        if not (0 <= map_x < n and 0 <= map_y < n):
            return None
        if cells[map_y][map_x] == solid:
            hit = True
            break
    if not hit:
        return None

    if side == 0:
        perp = (map_x - px + (1 - step_x) / 2) / dx
        wall_hit = py + perp * dy
    else:
        perp = (map_y - py + (1 - step_y) / 2) / dy
        wall_hit = px + perp * dx

    wall_x = wall_hit - math.floor(wall_hit)
    if (side == 0 and dx > 0) or (side == 1 and dy < 0):
        wall_x = 1.0 - wall_x

    return Hit(
        cell_x=map_x,
        cell_y=map_y,
        side=side,
        perp=max(0.01, perp),
        wall_x=wall_x,
    )

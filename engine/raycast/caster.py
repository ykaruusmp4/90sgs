from __future__ import annotations

from typing import Iterator

from ..camera.camera import Camera
from ..world.grid import Grid
from .dda import cast
from .hit import Hit
from .ray import Ray


def cast_column(grid: Grid, camera: Camera, screen_x: int, screen_w: int) -> Hit | None:
    d = camera.ray_dir(screen_x, screen_w)
    return cast(grid, Ray(camera.x, camera.y, d.x, d.y))


def cast_row(grid: Grid, camera: Camera, screen_w: int) -> Iterator[tuple[int, Hit | None]]:
    px, py = camera.x, camera.y
    for x in range(screen_w):
        d = camera.ray_dir(x, screen_w)
        yield x, cast(grid, Ray(px, py, d.x, d.y))

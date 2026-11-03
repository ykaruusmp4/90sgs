from __future__ import annotations

import math

from ..maths.constants import PI
from ..maths.vec2 import Vec2
from .plane import make_plane, projection_inverse


class Camera:
    __slots__ = ("x", "y", "angle", "direction", "plane", "fov")

    def __init__(self, x: float = 0.0, y: float = 0.0, angle: float = 0.0, fov: float = math.pi / 3):
        self.x = x
        self.y = y
        self.angle = angle
        self.direction = Vec2.from_angle(angle)
        self.fov = fov
        self.plane = make_plane(self.direction, fov)

    def move_to(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def translate(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy

    def set_angle(self, angle: float) -> None:
        self.angle = angle
        self.direction = Vec2.from_angle(angle)
        self.plane = make_plane(self.direction, self.fov)

    def rotate(self, delta: float) -> None:
        self.set_angle(self.angle + delta)

    def set_fov(self, fov: float) -> None:
        self.fov = fov
        self.plane = make_plane(self.direction, fov)

    def ray_dir(self, screen_x: int, screen_w: int) -> Vec2:
        t = 2.0 * (screen_x + 0.5) / screen_w - 1.0
        return Vec2(
            self.direction.x + self.plane.x * t,
            self.direction.y + self.plane.y * t,
        )

    def project(self, wx: float, wy: float) -> tuple[float, float]:
        dx = wx - self.x
        dy = wy - self.y
        inv = projection_inverse(self.plane, self.direction)
        tx = inv * (self.direction.y * dx - self.direction.x * dy)
        ty = inv * (-self.plane.y * dx + self.plane.x * dy)
        return tx, ty


def screen_column(camera: Camera, wx: float, wy: float, width: int) -> tuple[float, float] | None:
    tx, ty = camera.project(wx, wy)
    if ty < 0.01:
        return None
    screen_x = width * 0.5 * (1.0 + tx / ty)
    return screen_x, ty

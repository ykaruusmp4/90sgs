"""Vetor 2D imutável. Use em câmera, direções de raio e posições de spawn.

Posições "quentes" (player/monstro no update) podem continuar em floats soltos
pra evitar alocar por frame — Vec2 é imutável de propósito.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .constants import EPS


@dataclass(frozen=True, slots=True)
class Vec2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, o: "Vec2") -> "Vec2":
        return Vec2(self.x + o.x, self.y + o.y)

    def __sub__(self, o: "Vec2") -> "Vec2":
        return Vec2(self.x - o.x, self.y - o.y)

    def __mul__(self, k: float) -> "Vec2":
        return Vec2(self.x * k, self.y * k)

    def __rmul__(self, k: float) -> "Vec2":
        return self * k

    def __truediv__(self, k: float) -> "Vec2":
        return Vec2(self.x / k, self.y / k)

    def __neg__(self) -> "Vec2":
        return Vec2(-self.x, -self.y)

    def dot(self, o: "Vec2") -> float:
        return self.x * o.x + self.y * o.y

    def cross(self, o: "Vec2") -> float:
        return self.x * o.y - self.y * o.x

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def length_sq(self) -> float:
        return self.x * self.x + self.y * self.y

    def normalized(self) -> "Vec2":
        L = self.length()
        return Vec2(self.x / L, self.y / L) if L > EPS else Vec2()

    def rotated(self, a: float) -> "Vec2":
        c, s = math.cos(a), math.sin(a)
        return Vec2(self.x * c - self.y * s, self.x * s + self.y * c)

    def perpendicular(self) -> "Vec2":
        return Vec2(-self.y, self.x)

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    @classmethod
    def from_angle(cls, a: float, length: float = 1.0) -> "Vec2":
        return cls(math.cos(a) * length, math.sin(a) * length)

    @classmethod
    def lerp(cls, a: "Vec2", b: "Vec2", t: float) -> "Vec2":
        return cls(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t)


ZERO = Vec2()
X_AXIS = Vec2(1.0, 0.0)
Y_AXIS = Vec2(0.0, 1.0)

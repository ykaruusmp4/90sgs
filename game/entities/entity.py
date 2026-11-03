from __future__ import annotations

from engine.physics import Body


class Entity:
    __slots__ = ("body", "ativo")

    def __init__(self, x: float, y: float, radius: float = 14.0):
        self.body = Body(x, y, radius)
        self.ativo = True

    @property
    def x(self) -> float:
        return self.body.x

    @x.setter
    def x(self, value: float) -> None:
        self.body.x = value

    @property
    def y(self) -> float:
        return self.body.y

    @y.setter
    def y(self, value: float) -> None:
        self.body.y = value

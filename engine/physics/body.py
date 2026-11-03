"""Corpo físico: posição, velocidade e raio de colisão.

Convenção de unidades: `vx/vy` em **px por frame a 60fps**. Multiplicar por
`dt * 60` converte pra px neste frame. Bate com a engine original, onde
`vel_terminal()` retornava px/s e o update usava `k = dt * 60`.
"""

from __future__ import annotations


class Body:
    __slots__ = ("x", "y", "vx", "vy", "radius")

    def __init__(self, x: float = 0.0, y: float = 0.0, radius: float = 14.0):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.radius = radius

    def stop(self) -> None:
        self.vx = 0.0
        self.vy = 0.0

    def __repr__(self) -> str:
        return f"Body(x={self.x:.1f}, y={self.y:.1f}, v=({self.vx:.2f}, {self.vy:.2f}), r={self.radius})"

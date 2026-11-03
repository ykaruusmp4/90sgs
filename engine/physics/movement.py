"""Movimento com colisão: sub-passos (evita tunneling) + slide por eixo.

Mesmo algoritmo da `mover_com_colisao` original: divide o deslocamento em
tamanhos ≤ 12px, testa x e y separadamente, zera a velocidade no eixo que
bateu (permite deslizar).
"""

from __future__ import annotations

import math

from ..world.grid import Grid
from .body import Body
from .collision import circle_vs_grid

MAX_STEP = 12.0
VEL_ZERO = 0.05


def move_body(body: Body, grid: Grid, block_size: float, dt: float) -> None:
    k = dt * 60.0
    mx = body.vx * k
    my = body.vy * k
    if abs(body.vx) < VEL_ZERO:
        mx = 0.0
    if abs(body.vy) < VEL_ZERO:
        my = 0.0

    passos = max(1, math.ceil(max(abs(mx), abs(my)) / MAX_STEP))
    sx = mx / passos
    sy = my / passos

    for _ in range(passos):
        if sx:
            if circle_vs_grid(body.x + sx, body.y, body.radius, grid, block_size):
                body.vx = 0.0
                sx = 0.0
            else:
                body.x += sx
        if sy:
            if circle_vs_grid(body.x, body.y + sy, body.radius, grid, block_size):
                body.vy = 0.0
                sy = 0.0
            else:
                body.y += sy

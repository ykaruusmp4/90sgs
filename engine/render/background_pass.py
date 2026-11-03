from __future__ import annotations

import pygame as pg

from ..maths.scalars import clamp


def draw(
    surf: pg.Surface,
    background: pg.Surface,
    *,
    bob_y: float = 0.0,
    tilt: float = 0.0,
    margin: int = 24,
) -> None:
    w = surf.get_width()
    h = surf.get_height()
    limit = margin - 1
    meio_x = w / 2.0
    blit = surf.blit

    for x in range(w):
        desloc = round(bob_y + (x - meio_x) * tilt * 0.012)
        desloc = int(clamp(desloc, -limit, limit))
        blit(background, (x, 0), (x, margin - desloc, 1, h))

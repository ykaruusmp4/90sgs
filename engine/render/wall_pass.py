from __future__ import annotations

import math

import pygame as pg

from ..camera.camera import Camera
from ..maths.scalars import clamp
from ..raycast.caster import cast_column
from ..raycast.hit import Hit
from ..world.grid import Grid
from .shading import wall_fog
from .zbuffer import INF, ZBuffer


def draw(
    surf: pg.Surface,
    grid: Grid,
    camera: Camera,
    texture: pg.Surface,
    zbuffer: ZBuffer,
    *,
    bob_y: float = 0.0,
    tilt: float = 0.0,
    margin: int = 24,
) -> None:
    w = surf.get_width()
    h = surf.get_height()
    tex_w = texture.get_width()
    tex_h = texture.get_height()
    limit = margin - 1
    meio_x = w / 2.0
    blit = surf.blit

    for x in range(w):
        hit = cast_column(grid, camera, x, w)
        if hit is None:
            zbuffer[x] = INF
            continue
        zbuffer[x] = hit.perp
        _draw_column(surf, hit, x, w, h, tex_w, tex_h, bob_y, tilt, limit, meio_x, texture, blit)


def _draw_column(
    surf: pg.Surface,
    hit: Hit,
    x: int,
    screen_w: int,
    screen_h: int,
    tex_w: int,
    tex_h: int,
    bob_y: float,
    tilt: float,
    limit: int,
    meio_x: float,
    texture: pg.Surface,
    blit,
) -> None:
    desloc = round(bob_y + (x - meio_x) * tilt * 0.012)
    desloc = int(clamp(desloc, -limit, limit))

    altura_linha = screen_h / hit.perp
    topo = screen_h / 2.0 - altura_linha / 2.0 + desloc
    y0 = max(0, int(topo))
    y1 = min(screen_h, int(topo + altura_linha))
    if y1 <= y0:
        return

    tx = min(tex_w - 1, int(hit.wall_x * tex_w))

    v0 = (y0 - topo) / altura_linha * tex_h
    v1 = (y1 - topo) / altura_linha * tex_h
    sy = max(0, min(tex_h - 1, int(v0)))
    sh = max(1, min(tex_h - sy, math.ceil(v1) - sy))

    fatia = pg.transform.scale(texture.subsurface((tx, sy, 1, sh)), (1, y1 - y0))
    fator = wall_fog(hit.perp, hit.side)
    if fator < 1.0:
        s = int(255 * fator)
        fatia.fill((s, s, s), special_flags=pg.BLEND_RGB_MULT)
    blit(fatia, (x, y0))

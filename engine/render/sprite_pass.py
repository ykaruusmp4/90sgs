"""Billboards: sprites projetados no mundo com clip por z-buffer.

O chamador monta a lista de `Billboard` (já escala + tinge cada Surface),
passa por `draw_billboards`, e o pass cuida de:
  1. Ordenar far-to-near (painter).
  2. Recortar colunas onde a parede está na frente.

Primitivos (`line_height`, `ground_y`, `horizon_y`) cobrem a matemática
de projeção que a original tinha inline nos `_orb`/`_monstro`.
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame as pg

from .zbuffer import ZBuffer


@dataclass
class Billboard:
    perp: float
    screen_x: float
    surface: pg.Surface
    anchor_y: float
    anchor: str = "bottom"  # "bottom" | "center" | "top"
    flags: int = 0


def line_height(screen_h: int, perp: float) -> float:
    """Altura em pixels de uma parede unitária nessa distância perpendicular."""
    return screen_h / perp


def horizon_y(screen_h: int) -> float:
    return screen_h / 2.0


def ground_y(screen_h: int, perp: float, ground_frac: float = 0.5) -> float:
    """Y do 'chão' na tela nessa distância. `ground_frac=0.5` = base da parede."""
    return screen_h / 2.0 + (screen_h / perp) * ground_frac


def blit_visible(
    surf: pg.Surface,
    spr: pg.Surface,
    x0: int,
    y0: int,
    width: int,
    perp: float,
    zbuffer: ZBuffer,
    flags: int = 0,
) -> None:
    """Blita só os trechos de colunas onde `perp < zbuffer[col]`."""
    altura = spr.get_height()
    screen_w = surf.get_width()
    zb = zbuffer.data
    col = max(0, x0)
    fim = min(screen_w, x0 + width)
    while col < fim:
        if perp >= zb[col]:
            col += 1
            continue
        ini = col
        while col < fim and perp < zb[col]:
            col += 1
        surf.blit(spr, (ini, y0), (ini - x0, 0, col - ini, altura), special_flags=flags)


def draw_billboards(surf: pg.Surface, items: list[Billboard], zbuffer: ZBuffer) -> None:
    """Desenha a lista já ordenada far-to-near."""
    for it in items:
        w = it.surface.get_width()
        h = it.surface.get_height()
        x0 = int(it.screen_x - w / 2)
        if it.anchor == "bottom":
            y0 = int(it.anchor_y - h)
        elif it.anchor == "top":
            y0 = int(it.anchor_y)
        else:
            y0 = int(it.anchor_y - h / 2)
        blit_visible(surf, it.surface, x0, y0, w, it.perp, zbuffer, it.flags)

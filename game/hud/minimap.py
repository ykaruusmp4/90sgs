import math

import pygame as pg

from engine.world import Grid


def draw_minimap(
    surf: pg.Surface, grid: Grid, px: float, py: float, angle: float, fov: float, block_size: float, scale: int = 2
) -> None:
    """Desenha o minimapa no canto superior direito.
    Recebe px, py em pixels (posição do player)."""
    n = grid.n
    w = n * scale
    ox = surf.get_width() - w - 4
    oy = 4

    pg.draw.rect(surf, (14, 14, 16), (ox, oy, w, w))

    for y in range(n):
        for x in range(n):
            if grid.cells[y][x] == grid.solid:
                pg.draw.rect(surf, (60, 60, 65), (ox + x * scale, oy + y * scale, scale, scale))

    cx = px / block_size
    cy = py / block_size
    p_x = ox + cx * scale
    p_y = oy + cy * scale

    comp = 6
    for ang in (angle - fov / 2, angle + fov / 2):
        pg.draw.line(surf, (0, 255, 255), (p_x, p_y), (p_x + math.cos(ang) * comp, p_y + math.sin(ang) * comp), 1)

    pg.draw.rect(surf, (255, 255, 0), (int(p_x), int(p_y), max(scale, 2), max(scale, 2)))

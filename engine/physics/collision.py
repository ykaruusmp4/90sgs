"""Colisão círculo × grid (células sólidas).

Só considera a vizinhança 3x3 ao redor da célula atual — o raio do corpo é
sempre menor que `block_size / 2` na prática (14 < 32), então nada além disso
pode intersectar. Fora do grid = sólido (mesmo tratamento do original).
"""

from __future__ import annotations

from ..world.grid import Grid


def circle_vs_grid(px: float, py: float, radius: float, grid: Grid, block_size: float) -> bool:
    cx = int(px // block_size)
    cy = int(py // block_size)
    r2 = radius * radius
    cells = grid.cells
    n = grid.n
    solid = grid.solid

    for my in range(cy - 1, cy + 2):
        for mx in range(cx - 1, cx + 2):
            dentro = 0 <= mx < n and 0 <= my < n
            livre = dentro and cells[my][mx] != solid
            if livre:
                continue
            x0 = mx * block_size
            y0 = my * block_size
            qx = x0 if px < x0 else (x0 + block_size if px > x0 + block_size else px)
            qy = y0 if py < y0 else (y0 + block_size if py > y0 + block_size else py)
            dx = px - qx
            dy = py - qy
            if dx * dx + dy * dy < r2:
                return True
    return False

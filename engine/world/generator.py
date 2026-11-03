from __future__ import annotations

import hashlib
import random

from .cell import FLOOR, WALL
from .grid import Grid
from .queries import free_regions, largest_region

ITERACOES_SUAVIZAR = 4
LIMIAR_VIZINHOS = 4
MINIMO_LIVRE = 40
TAMANHO_CAVADO_FALLBACK = 8


def seed_to_int(seed: str | int) -> int:
    if isinstance(seed, int):
        return seed
    return int(hashlib.md5(seed.encode("utf-8")).hexdigest(), 16)


def generate(seed: str | int, size: int = 32, density: float = 0.45) -> Grid:
    rng = random.Random(seed_to_int(seed))
    cells = _random_fill(rng, size, density)
    for _ in range(ITERACOES_SUAVIZAR):
        cells = _smooth(cells)
    grid = Grid(cells, solid=WALL)
    _keep_largest_region(grid)
    _ensure_minimum_free(grid)
    return grid


def _random_fill(rng: random.Random, size: int, density: float) -> list[list[int]]:
    cells: list[list[int]] = []
    for y in range(size):
        row = []
        for x in range(size):
            borda = x == 0 or x == size - 1 or y == 0 or y == size - 1
            row.append(WALL if borda or rng.random() < density else FLOOR)
        cells.append(row)
    return cells


def _smooth(cells: list[list[int]]) -> list[list[int]]:
    n = len(cells)
    novo = [row[:] for row in cells]
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            vizinhos = 0
            for dy in (-1, 0, 1):
                row = cells[y + dy]
                for dx in (-1, 0, 1):
                    vizinhos += row[x + dx]
            novo[y][x] = WALL if vizinhos > LIMIAR_VIZINHOS else FLOOR
    return novo


def _keep_largest_region(grid: Grid) -> None:
    regioes = free_regions(grid)
    if not regioes:
        return
    maior_idx = max(range(len(regioes)), key=lambda i: len(regioes[i]))
    cells = grid.cells
    for i, regiao in enumerate(regioes):
        if i == maior_idx:
            continue
        for x, y in regiao:
            cells[y][x] = WALL


def _ensure_minimum_free(grid: Grid) -> None:
    if grid.free_count() >= MINIMO_LIVRE:
        return
    n = grid.n
    meio = n // 2
    metade = TAMANHO_CAVADO_FALLBACK // 2
    cells = grid.cells
    for y in range(meio - metade, meio + metade):
        for x in range(meio - metade, meio + metade):
            cells[y][x] = FLOOR

from __future__ import annotations

from collections import deque

from .grid import Grid

DIRS4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def bfs_distances(grid: Grid, origin: tuple[int, int]) -> dict[tuple[int, int], int]:
    cells = grid.cells
    n = grid.n
    solid = grid.solid
    ox, oy = origin
    dist = {origin: 0}
    fila = deque([origin])
    while fila:
        cx, cy = fila.popleft()
        d = dist[(cx, cy)] + 1
        for dx, dy in DIRS4:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < n and cells[ny][nx] != solid and (nx, ny) not in dist:
                dist[(nx, ny)] = d
                fila.append((nx, ny))
    return dist


def free_regions(grid: Grid) -> list[list[tuple[int, int]]]:
    cells = grid.cells
    n = grid.n
    solid = grid.solid
    visitado = [[False] * n for _ in range(n)]
    regioes: list[list[tuple[int, int]]] = []
    for y0 in range(n):
        for x0 in range(n):
            if cells[y0][x0] == solid or visitado[y0][x0]:
                continue
            fila = deque([(x0, y0)])
            visitado[y0][x0] = True
            regiao = []
            while fila:
                cx, cy = fila.popleft()
                regiao.append((cx, cy))
                for dx, dy in DIRS4:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < n and 0 <= ny < n and cells[ny][nx] != solid and not visitado[ny][nx]:
                        visitado[ny][nx] = True
                        fila.append((nx, ny))
            regioes.append(regiao)
    return regioes


def largest_region(grid: Grid) -> list[tuple[int, int]] | None:
    regioes = free_regions(grid)
    return max(regioes, key=len) if regioes else None


def find_start_cell(grid: Grid) -> tuple[int, int]:
    n = grid.n
    cells = grid.cells
    solid = grid.solid

    for y in range(n // 2, n):
        for x in range(n // 2, n):
            if cells[y][x] != solid:
                vizinhos_livres = 0
                for dx, dy in DIRS4:
                    if 0 <= x + dx < n and 0 <= y + dy < n and cells[y + dy][x + dx] != solid:
                        vizinhos_livres += 1
                if vizinhos_livres >= 2:
                    return x, y

    for y in range(n):
        for x in range(n):
            if cells[y][x] != solid:
                return x, y
    return n // 2, n // 2


def has_line_of_sight(x0: float, y0: float, x1: float, y1: float, grid: Grid, block_size: float) -> bool:
    dx = x1 - x0
    dy = y1 - y0
    d = (dx * dx + dy * dy) ** 0.5
    if d < 1e-3:
        return True
    passos = max(2, int(d / (block_size / 8.0)))
    inv = 1.0 / passos
    for i in range(1, passos):
        t = i * inv
        px = x0 + dx * t
        py = y0 + dy * t
        if grid.is_solid(int(px // block_size), int(py // block_size)):
            return False
    return True

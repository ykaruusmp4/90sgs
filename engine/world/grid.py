from __future__ import annotations

from typing import Iterator

from .cell import FLOOR, WALL, Cell


class Grid:
    __slots__ = ("cells", "n", "solid")

    def __init__(self, cells: list[list[Cell]], solid: Cell = WALL):
        if not cells or not cells[0]:
            raise ValueError("grid vazio")
        n = len(cells)
        if any(len(row) != n for row in cells):
            raise ValueError("grid precisa ser quadrado")
        self.cells = cells
        self.n = n
        self.solid = solid

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.n and 0 <= y < self.n

    def is_free(self, x: int, y: int) -> bool:
        return 0 <= x < self.n and 0 <= y < self.n and self.cells[y][x] != self.solid

    def is_solid(self, x: int, y: int) -> bool:
        return not self.is_free(x, y)

    def get(self, x: int, y: int, default: Cell = WALL) -> Cell:
        if 0 <= x < self.n and 0 <= y < self.n:
            return self.cells[y][x]
        return default

    def set(self, x: int, y: int, value: Cell) -> None:
        self.cells[y][x] = value

    def iter_free(self) -> Iterator[tuple[int, int]]:
        cells = self.cells
        solid = self.solid
        for y in range(self.n):
            row = cells[y]
            for x in range(self.n):
                if row[x] != solid:
                    yield x, y

    def iter_solid(self) -> Iterator[tuple[int, int]]:
        cells = self.cells
        solid = self.solid
        for y in range(self.n):
            row = cells[y]
            for x in range(self.n):
                if row[x] == solid:
                    yield x, y

    def free_count(self) -> int:
        cells = self.cells
        solid = self.solid
        return sum(1 for row in cells for v in row if v != solid)

    @classmethod
    def filled(cls, n: int, fill: Cell = FLOOR) -> "Grid":
        return cls([[fill] * n for _ in range(n)])

    def __repr__(self) -> str:
        return f"Grid(n={self.n}, free={self.free_count()})"

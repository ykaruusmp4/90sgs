"""Valores de célula do grid — a original usava `0`/`1` soltos por todo lado.

Manter como int (não Enum) é de propósito: o hot path do raycaster faz
`cells[my][mx] == WALL` por coluna, e Enum.attr tem custo de lookup.
"""

FLOOR = 0
WALL = 1

Cell = int

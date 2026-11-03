"""Física: corpos, colisão círculo×grid e movimento com slide."""

from .body import Body
from .collision import circle_vs_grid
from .movement import move_body

__all__ = ["Body", "circle_vs_grid", "move_body"]

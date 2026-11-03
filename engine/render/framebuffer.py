"""Framebuffer virtual — a `pygame.Surface` que os passes desenham.

Não confundir com a `pipeline.py`, que faz o upload pra GPU. Aqui é só o
"buffer lógico" e o acesso aos bytes pra upload.
"""

from __future__ import annotations

import pygame as pg


class FrameBuffer:
    __slots__ = ("width", "height", "surface")

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = pg.Surface((width, height))

    def clear(self, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.surface.fill(color)

    def to_bytes(self, formato: str = "RGBA") -> bytes:
        """Bytes pra upload de textura. `flip_y=True` porque pygame é top-down."""
        return pg.image.tobytes(self.surface, formato, True)

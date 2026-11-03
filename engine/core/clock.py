"""Clock com clamp de dt — evita salto de física em lag spike.

O clamp em `max_dt` (default 1/30) bate com o `min(tick/1000, 1/30)` da
engine original. Se um frame demorar 200ms, o jogo avança só 33ms.
"""

from __future__ import annotations

import pygame as pg


class Clock:
    __slots__ = ("_clock", "target_fps", "max_dt")

    def __init__(self, target_fps: int = 60, max_dt: float = 1.0 / 30.0):
        self._clock = pg.time.Clock()
        self.target_fps = target_fps
        self.max_dt = max_dt

    def tick(self) -> float:
        """Avança um frame. Devolve `dt` em segundos, clampado em `max_dt`."""
        return min(self._clock.tick(self.target_fps) / 1000.0, self.max_dt)

    @property
    def fps(self) -> int:
        return int(self._clock.get_fps())

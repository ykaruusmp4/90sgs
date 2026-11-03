from __future__ import annotations

import pygame as pg


class Clock:
    __slots__ = ("_clock", "target_fps", "max_dt")

    def __init__(self, target_fps: int = 60, max_dt: float = 1.0 / 30.0):
        self._clock = pg.time.Clock()
        self.target_fps = target_fps
        self.max_dt = max_dt

    def tick(self) -> float:
        return min(self._clock.tick(self.target_fps) / 1000.0, self.max_dt)

    @property
    def fps(self) -> int:
        return int(self._clock.get_fps())

from __future__ import annotations

import pygame as pg

from .clock import Clock


def run(app, clock: Clock) -> None:
    while app.running:
        dt = clock.tick()
        app.frame(dt)
        pg.display.flip()

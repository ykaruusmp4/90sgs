"""Loop principal. Só coordena: tick → frame → present.

Toda a lógica pesada mora em `App.frame`. Este módulo existe pra ser o lugar
onde "rodar pra sempre" acontece — e onde dá pra trocar `pg.display.flip()`
por algo mais exótico (ex.: `flip()` só a cada N frames) sem tocar em App.
"""

from __future__ import annotations

import pygame as pg

from .clock import Clock


def run(app, clock: Clock) -> None:
    while app.running:
        dt = clock.tick()
        app.frame(dt)
        pg.display.flip()

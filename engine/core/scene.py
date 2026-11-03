from __future__ import annotations

import pygame as pg


class Scene:
    __slots__ = ("app",)

    def __init__(self, app):
        self.app = app

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pg.Surface) -> None:
        pass

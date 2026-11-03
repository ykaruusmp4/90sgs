import pygame as pg

from engine.core import Scene


class GameOverScene(Scene):
    __slots__ = ("mensagem",)

    def __init__(self, app):
        super().__init__(app)
        self.mensagem = "GAME OVER"

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key in (pg.K_RETURN, pg.K_KP_ENTER, pg.K_ESCAPE):
            self.app.scene_manager.change("MENU")

    def draw(self, surface: pg.Surface) -> None:
        t = pg.time.get_ticks() / 1000.0
        self.app.hud.draw_fim(surface, self.mensagem, t)

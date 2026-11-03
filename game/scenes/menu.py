import pygame as pg

from engine.core import Scene


class MenuScene(Scene):
    __slots__ = ("opcao",)

    def __init__(self, app):
        super().__init__(app)
        self.opcao = 0

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_UP):
                self.opcao = (self.opcao - 1) % 3
                if self.app.audio:
                    self.app.audio.tocar("blip")
            elif event.key in (pg.K_s, pg.K_DOWN):
                self.opcao = (self.opcao + 1) % 3
                if self.app.audio:
                    self.app.audio.tocar("blip")
            elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                if self.app.audio:
                    self.app.audio.tocar("select")
                if self.opcao == 0:
                    self.app.change_scene("HOWTO")
                elif self.opcao == 1:
                    self.app.crt_on = not self.app.crt_on
                else:
                    self.app.stop()
            elif event.key == pg.K_ESCAPE:
                self.app.stop()

    def draw(self, surface: pg.Surface) -> None:
        t = pg.time.get_ticks() / 1000.0
        crt_txt = f"CRT {'ON' if self.app.crt_on else 'OFF'}"
        opcoes = ["START", crt_txt, "EXIT"]

        # Pega a seed do app se existir, senão usa a padrão
        seed_str = getattr(self.app, "seed", "x9z2r7w1")

        self.app.hud.draw_menu(surface, "90 SECONDS", opcoes, self.opcao, t, seed=seed_str)

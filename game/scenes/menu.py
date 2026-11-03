import pygame as pg

from engine.core import Scene

SECRET_CODE = [pg.K_RIGHT, pg.K_RIGHT, pg.K_DOWN, pg.K_DOWN, pg.K_DOWN, pg.K_LEFT, pg.K_LEFT]


class MenuScene(Scene):
    __slots__ = ("opcao", "secret_unlocked", "historico")

    def __init__(self, app):
        super().__init__(app)
        self.opcao = 0
        self.secret_unlocked = False
        self.historico = []

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT):
                self.historico.append(event.key)
                if len(self.historico) > len(SECRET_CODE):
                    self.historico.pop(0)

                if self.historico == SECRET_CODE:
                    if not self.secret_unlocked:
                        self.secret_unlocked = True
                        if self.app.audio:
                            self.app.audio.tocar("select")

            num_opcoes = 4 if self.secret_unlocked else 3

            if event.key in (pg.K_w, pg.K_UP):
                self.opcao = (self.opcao - 1) % num_opcoes
                if self.app.audio:
                    self.app.audio.tocar("blip")
            elif event.key in (pg.K_s, pg.K_DOWN):
                self.opcao = (self.opcao + 1) % num_opcoes
                if self.app.audio:
                    self.app.audio.tocar("blip")
            elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                if self.app.audio:
                    self.app.audio.tocar("select")

                if self.opcao == 0:
                    self.app.scene_manager.change("HOWTO")
                elif self.opcao == 1:
                    self.app.scene_manager.change("OPTIONS")
                elif self.opcao == 2:
                    self.app.stop()
                elif self.opcao == 3 and self.secret_unlocked:
                    self.app.scene_manager.change("FONT_TEST")
            elif event.key == pg.K_ESCAPE:
                self.app.stop()

    def draw(self, surface: pg.Surface) -> None:
        t = pg.time.get_ticks() / 1000.0
        opcoes = ["START", "OPTIONS", "EXIT"]

        if self.secret_unlocked:
            opcoes.append("$font_test")

        seed_str = "---"
        jogo_scene = self.app.scene_manager.scenes.get("JOGO")
        if jogo_scene and jogo_scene.world and jogo_scene.world.seed:
            seed_str = jogo_scene.world.seed

        self.app.hud.draw_menu(surface, "90 SECONDS", opcoes, self.opcao, t, seed=seed_str)

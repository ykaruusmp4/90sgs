import pygame as pg

from engine.core import Scene
from engine.render import put_text, put_text_centered, put_text_wave
from game.hud.hud import AZUL, BRANCO, CINZA, VERDE, VERMELHO


class HowToScene(Scene):
    __slots__ = ()

    def __init__(self, app):
        super().__init__(app)

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.app.change_scene("MENU")
            elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                if self.app.audio:
                    self.app.audio.tocar("select")
                self.app.scenes["JOGO"].iniciar_novo_jogo()
                self.app.change_scene("JOGO")

    def draw(self, surface: pg.Surface) -> None:
        t = pg.time.get_ticks() / 1000.0
        surface.fill((10, 10, 12))
        hud = self.app.hud

        put_text_wave(surface, hud.font, "COMO JOGAR", 22, t, color_idx=VERMELHO)

        put_text_centered(surface, hud.font, "OBJETIVO", 60, color_idx=VERDE)
        put_text_centered(surface, hud.font, "COLETE OS 3 ORBS", 74, color_idx=BRANCO)
        put_text_centered(surface, hud.font, "E FUJA DOS MONSTROS", 84, color_idx=BRANCO)

        put_text_centered(surface, hud.font, "CONTROLES", 110, color_idx=VERDE)

        controles = [
            ("W/S", "ANDAR"),
            ("A/D", "STRAFE"),
            ("MOUSE", "OLHAR"),
            ("SHIFT", "CORRER"),
            ("M", "MUDO"),
            ("ESC", "MENU"),
        ]
        y = 124
        for esq, acao in controles:
            put_text(surface, hud.font, esq, 30, y, color_idx=CINZA)
            put_text(surface, hud.font, acao, 140, y, color_idx=BRANCO)
            y += 11

        if int(t * 2) % 2 == 0:
            put_text_centered(surface, hud.font, "ENTER PARA COMECAR", surface.get_height() - 20, color_idx=AZUL)
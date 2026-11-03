import pygame as pg

from engine.core import Scene
from engine.render import put_char, put_text, put_text_centered
from game.hud.hud import BRANCO, CINZA, VERDE, VERMELHO


class FontTestScene(Scene):
    __slots__ = ()

    def __init__(self, app):
        super().__init__(app)

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_ESCAPE, pg.K_RETURN, pg.K_KP_ENTER):
                if self.app.audio:
                    self.app.audio.tocar("select")
                self.app.scene_manager.change("MENU")

    def draw(self, surface: pg.Surface) -> None:
        surface.fill((10, 10, 12))
        hud = self.app.hud

        put_text_centered(surface, hud.font, "FONT TEST", 4, color_idx=VERMELHO, escala=2)
        put_text_centered(surface, hud.font, "ESC PARA VOLTAR", 24, color_idx=CINZA)

        blocos = [
            ("1234567890", VERDE),
            ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", BRANCO),
            ("abcdefghijklmnopqrstuvwxyz", BRANCO),
            ("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~", CINZA),
            ("ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ", BRANCO),
        ]

        y = 40
        for texto, cor in blocos:
            put_text(surface, hud.font, texto, 8, y, color_idx=cor)
            y += 14

        put_text(surface, hud.font, "TODOS OS CARACTERES E ICONES DO ARQUIVO:", 8, y + 6, color_idx=VERMELHO)
        y += 20

        todos_os_chars = [chr(c) for c in sorted(hud.font.data.keys()) if c not in (10, 13, 32)]
        string_todos = "".join(todos_os_chars)

        x = 8
        for ch in string_todos:
            if x > surface.get_width() - 12:
                x = 8
                y += 12

            if ch not in ("\n", "\r"):
                put_char(surface, hud.font, ch, x, y, color_idx=VERDE)

            x += 10

import pygame as pg

from engine.core import Scene
from engine.render import put_text
from game.config.constants import TOTAL_NIVEIS
from game.hud.hud import BRANCO, CINZA

T_FADE_OUT = 0.45
T_ANTES = 0.30
T_ROLL = 0.30
T_DEPOIS = 0.50
T_FADE_IN = 0.45

T_INICIO_PRETO = T_FADE_OUT
T_INICIO_FADE_IN = T_FADE_OUT + T_ANTES + T_ROLL + T_DEPOIS
T_TOTAL = T_INICIO_FADE_IN + T_FADE_IN

ESP = 7
ALTURA_ROLL = 12


class TransitionScene(Scene):
    __slots__ = ("t", "de", "para", "carregado")

    def __init__(self, app):
        super().__init__(app)
        self.t = 0.0
        self.de = 1
        self.para = 2
        self.carregado = False

    def iniciar(self, de: int, para: int) -> None:
        self.t = 0.0
        self.de = de
        self.para = para
        self.carregado = False

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.app.change_scene("MENU")

    def update(self, dt: float) -> None:
        self.t += dt
        if not self.carregado and self.t >= T_INICIO_PRETO:
            self.app.scenes["JOGO"].load_level(self.para)
            if self.app.audio:
                self.app.audio.tocar("nivel")
            self.carregado = True
        if self.t >= T_TOTAL:
            self.app.change_scene("JOGO")

    def _cena(self, surface: pg.Surface, brilho: float) -> None:
        self.app.scenes["JOGO"].draw(surface)
        v = int(255 * max(0.0, min(1.0, brilho)))
        if v < 255:
            surface.fill((v, v, v), special_flags=pg.BLEND_RGB_MULT)

    def _numero(self, surface: pg.Surface, u: float) -> None:
        hud = self.app.hud
        if u < T_ANTES:
            k = 0.0
        elif u < T_ANTES + T_ROLL:
            k = (u - T_ANTES) / T_ROLL
            k = 1.0 - (1.0 - k) ** 2
        else:
            k = 1.0

        novo, velho = str(self.para), str(self.de)
        sufixo = f"/{TOTAL_NIVEIS}"
        largura_total = (len(novo) + len(sufixo)) * ESP - (ESP - 8)
        x0 = (surface.get_width() - largura_total) // 2
        y = surface.get_height() // 2 - 4
        x_sufixo = x0 + len(novo) * ESP

        dy = round(k * ALTURA_ROLL)
        x_velho = x0 + (len(novo) - len(velho)) * ESP

        surface.set_clip(pg.Rect(x0, y, len(novo) * ESP + 1, 8))
        put_text(surface, hud.font, velho, x_velho, y - dy, color_idx=CINZA)
        put_text(surface, hud.font, novo, x0, y + ALTURA_ROLL - dy, color_idx=BRANCO)
        surface.set_clip(None)

        put_text(surface, hud.font, sufixo, x_sufixo, y, color_idx=CINZA)

    def draw(self, surface: pg.Surface) -> None:
        t = self.t
        if t < T_INICIO_PRETO:
            self._cena(surface, 1.0 - t / T_FADE_OUT)
        elif t < T_INICIO_FADE_IN:
            surface.fill((0, 0, 0))
            self._numero(surface, t - T_INICIO_PRETO)
        else:
            self._cena(surface, (t - T_INICIO_FADE_IN) / T_FADE_IN)

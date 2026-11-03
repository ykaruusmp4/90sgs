import math
import random

import pygame as pg

from engine.core import Scene
from engine.render import put_text, put_text_centered, radial_glow
from game.config.constants import ALTURA_VIRTUAL, CORES_ORB, LARGURA_VIRTUAL, TOTAL_NIVEIS
from game.hud.hud import AMARELO, BRANCO, CINZA, COR_SOMBRA

TITULO = "VOCÊ VENCEU!!"
ESP = 7
CORES_CONFETE = [
    (255, 220, 60),
    (255, 70, 70),
    (80, 200, 255),
    (255, 90, 220),
    (255, 255, 255),
    (255, 150, 40),
    (120, 255, 120),
]
N_CONFETES = 90


class Confete:
    __slots__ = ("x", "y", "vy", "fase", "freq", "amp", "cor")


def _sortear(rng: random.Random, y: float) -> Confete:
    c = Confete()
    c.x = rng.uniform(0, LARGURA_VIRTUAL)
    c.y = y
    c.vy = rng.uniform(35, 90)
    c.fase = rng.uniform(0, math.tau)
    c.freq = rng.uniform(2.0, 5.0)
    c.amp = rng.uniform(3, 14)
    c.cor = rng.choice(CORES_CONFETE)
    return c


def _gerar_fundo() -> pg.Surface:
    surf = pg.Surface((LARGURA_VIRTUAL, ALTURA_VIRTUAL))
    topo, base = (8, 40, 22), (26, 112, 48)
    for y in range(ALTURA_VIRTUAL):
        k = y / (ALTURA_VIRTUAL - 1)
        pg.draw.line(
            surf, tuple(int(topo[i] + (base[i] - topo[i]) * k) for i in range(3)), (0, y), (LARGURA_VIRTUAL - 1, y)
        )
    return surf


class VictoryScene(Scene):
    __slots__ = ("t", "confetes", "fundo", "rng", "brilhos")

    def __init__(self, app):
        super().__init__(app)
        self.rng = random.Random()
        self.fundo = _gerar_fundo()
        self.brilhos = [radial_glow(c) for c in CORES_ORB]
        self.t = 0.0
        self.confetes = []

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        self.t = 0.0
        self.confetes = [
            _sortear(self.rng, self.rng.uniform(-ALTURA_VIRTUAL, ALTURA_VIRTUAL)) for _ in range(N_CONFETES)
        ]

    def handle_event(self, event: pg.event.Event) -> None:
        if self.t < 0.5:
            return
        if event.type == pg.KEYDOWN and event.key in (pg.K_RETURN, pg.K_KP_ENTER, pg.K_ESCAPE):
            self.app.scene_manager.change("MENU")

    def update(self, dt: float) -> None:
        self.t += dt
        for c in self.confetes:
            c.y += c.vy * dt
            if c.y > ALTURA_VIRTUAL + 4:
                novo = _sortear(self.rng, -4.0)
                c.x, c.y, c.vy, c.fase, c.freq, c.amp, c.cor = (
                    novo.x,
                    novo.y,
                    novo.vy,
                    novo.fase,
                    novo.freq,
                    novo.amp,
                    novo.cor,
                )

    def _titulo(self, surface: pg.Surface, t: float) -> None:
        hud = self.app.hud
        n = len(TITULO)
        w = n * ESP - (ESP - 8) + 2
        faixa = pg.Surface((w, 16), pg.SRCALPHA)
        brilho = int(t * 9) % (n + 8)
        x = 1
        for i, ch in enumerate(TITULO):
            y = 4 + round(math.sin(t * 4.0 + i * 0.55) * 2.0)
            put_text(faixa, hud.font, ch, x + 1, y + 1, color_idx=COR_SOMBRA)
            put_text(faixa, hud.font, ch, x, y, color_idx=BRANCO if i == brilho else AMARELO)
            x += ESP
        grande = pg.transform.scale(faixa, (w * 2, 32))
        surface.blit(grande, ((LARGURA_VIRTUAL - w * 2) // 2, 52))

    def draw(self, surface: pg.Surface) -> None:
        hud = self.app.hud
        t = self.t

        surface.blit(self.fundo, (0, 0))
        desloc = int(t * 20) % 32
        for y in range(-32 + desloc, ALTURA_VIRTUAL, 32):
            surface.fill((10, 22, 10), (0, y, LARGURA_VIRTUAL, 12), special_flags=pg.BLEND_RGB_ADD)

        for c in self.confetes:
            x = c.x + math.sin(t * c.freq + c.fase) * c.amp
            gira = math.sin(t * c.freq * 1.7 + c.fase) > 0
            w, h = (3, 2) if gira else (2, 3)
            surface.fill(c.cor, (int(x), int(c.y), w, h))

        self._titulo(surface, t)
        put_text_centered(surface, hud.font, f"{TOTAL_NIVEIS}/{TOTAL_NIVEIS}", 104, color_idx=BRANCO, sombra=True)

        for i, brilho in enumerate(self.brilhos):
            cx = LARGURA_VIRTUAL // 2 + (i - 1) * 36
            cy = 146 + round(math.sin(t * 3.0 + i * 1.3) * 4)
            surface.blit(pg.transform.scale(brilho, (28, 28)), (cx - 14, cy - 14), special_flags=pg.BLEND_RGB_ADD)

        if int(t * 2) % 2 == 0:
            put_text_centered(surface, hud.font, "ENTER", 196, color_idx=CINZA, sombra=True)

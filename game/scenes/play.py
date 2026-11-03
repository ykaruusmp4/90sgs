from __future__ import annotations

import math

import pygame as pg

from engine.camera.camera import screen_column
from engine.core import Scene
from engine.render import (
    Billboard,
    ZBuffer,
    draw_background,
    draw_billboards,
    draw_walls,
    horizon_y,
    line_height,
    radial_glow,
    sort_by_perp_desc,
)
from game.config.balance import TAM_ORB
from game.config.constants import CORES_ORB, LARGURA_VIRTUAL, TAMANHO_BLOCO, TOTAL_NIVEIS
from game.core.game_world import GameWorld
from game.hud.minimap import draw_minimap


class PlayScene(Scene):
    __slots__ = ("world", "zbuffer", "brilhos")

    def __init__(self, app):
        super().__init__(app)
        self.world = GameWorld(app)
        self.zbuffer = ZBuffer(LARGURA_VIRTUAL)
        self.brilhos = [radial_glow(c) for c in CORES_ORB]

    def enter(self) -> None:
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.mouse.get_rel()

        if self.app.audio:
            self.app.audio.tocar_ambiente("ambiente")

        if self.world.level is None:
            self.world.iniciar_novo_jogo()

    def exit(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        if self.app.audio:
            self.app.audio.parar_ambiente()

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
            self.app.scene_manager.change("MENU")

    def update(self, dt: float) -> None:
        acao = self.world.update(dt)
        if acao:
            self.app.scene_manager.change(acao)

    def draw(self, surface: pg.Surface) -> None:
        w = self.world
        if not w.level or not w.player:
            return

        j = w.player
        H = surface.get_height()
        W = surface.get_width()
        t = pg.time.get_ticks() / 1000.0

        draw_background(surface, w.level.background, bob_y=j.bobbing_y, tilt=j.tilt)
        draw_walls(
            surface,
            w.level.grid,
            j.camera,
            w.level.texture,
            self.zbuffer,
            bob_y=j.bobbing_y,
            tilt=j.tilt,
            multithread=self.app.settings.multithread,
        )

        items = []
        for orb in w.orbs:
            if orb.coletado:
                continue
            p = screen_column(j.camera, orb.bx, orb.by, W)
            if p is None:
                continue
            sx, perp = p
            if not (-50 <= sx <= W + 50):
                continue

            lh = line_height(H, perp)
            tam = int(lh * TAM_ORB * (1.0 + 0.10 * math.sin(t * 5.0 + orb.fase)))
            tam = max(3, min(tam, 256))

            spr = pg.transform.scale(self.brilhos[orb.cor_idx], (tam, tam))
            v = int(255 * (0.75 + 0.25 * math.sin(t * 5.0 + orb.fase)))
            spr.fill((v, v, v), special_flags=pg.BLEND_RGB_MULT)
            cy = horizon_y(H) + j.bobbing_y + lh * (0.15 + 0.04 * math.sin(t * 2.0 + orb.fase))
            items.append(Billboard(perp, sx, spr, cy, anchor="center", flags=pg.BLEND_RGB_ADD))

        for m in w.monstros:
            p = screen_column(j.camera, m.bx, m.by, W)
            if p is None:
                continue
            sx, perp = p
            if not (-100 <= sx <= W + 100):
                continue

            lh = line_height(H, perp)
            h = max(3, min(int(lh * 0.55 * (1.0 + 0.05 * math.sin(t * 9.0 + m.fase))), 300))
            w_spr = max(1, int(h * m.sprite.get_width() / m.sprite.get_height()))

            spr = pg.transform.scale(m.sprite, (w_spr, h))
            fog = max(0.25, 1.0 - perp * 0.03)
            s = int(255 * fog)
            spr.fill((s, s, s), special_flags=pg.BLEND_RGB_MULT)

            cy = horizon_y(H) + j.bobbing_y + lh * 0.5
            items.append(Billboard(perp, sx, spr, cy, anchor="bottom"))

        sort_by_perp_desc(items)
        draw_billboards(surface, items, self.zbuffer)

        draw_minimap(surface, w.level.grid, j.x, j.y, j.camera.angle, j.camera.fov, TAMANHO_BLOCO)

        ox, oy = W - w.level.grid.n * 2 - 4, 4
        for orb in w.orbs:
            if not orb.coletado:
                pg.draw.rect(surface, CORES_ORB[orb.cor_idx], (ox + orb.bx * 2 - 1, oy + orb.by * 2 - 1, 3, 3))
        for m in w.monstros:
            pg.draw.rect(surface, (255, 0, 0), (ox + m.bx * 2, oy + m.by * 2, 2, 2))

        self.app.hud.draw_gameplay(
            surface, j, w.orbs, w.tempo_restante, w.level.numero, TOTAL_NIVEIS, self.app.clock.fps
        )

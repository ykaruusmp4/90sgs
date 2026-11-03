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
from engine.world.flowfield import FlowField
from game.config.balance import ATRASO_MONSTROS, DURACAO_PARTIDA, INVULNERAVEL_DANO, RAIO_COLETA, RAIO_CONTATO, TAM_ORB
from game.config.constants import CORES_ORB, LARGURA_VIRTUAL, TAMANHO_BLOCO, TOTAL_NIVEIS
from game.entities import Player
from game.entities.monster import Monster
from game.entities.orb import Orb
from game.hud.minimap import draw_minimap
from game.levels import Level
from game.rules.spawning import spawn_monsters, spawn_orbs
from game.rules.win_lose import checar_derrota, checar_vitoria, proximo_nivel


class PlayScene(Scene):
    __slots__ = (
        "seed",
        "level",
        "player",
        "zbuffer",
        "orbs",
        "brilhos",
        "monstros",
        "flowfield",
        "tempo_nivel",
        "flash_dano",
        "tempo_restante",
        "_meio_ciclo",
    )

    def __init__(self, app, seed: str = "x9z2r7w1"):
        super().__init__(app)
        self.seed = seed
        self.level: Level | None = None
        self.player: Player | None = None
        self.zbuffer = ZBuffer(LARGURA_VIRTUAL)
        self.orbs: list[Orb] = []
        self.monstros: list[Monster] = []
        self.flowfield: FlowField | None = None
        self.brilhos = [radial_glow(c) for c in CORES_ORB]

        self.tempo_nivel = 0.0
        self.flash_dano = 0.0
        self.tempo_restante = DURACAO_PARTIDA
        self._meio_ciclo = 0

    def enter(self) -> None:
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.mouse.get_rel()  # Limpa o acumulado de antes de entrar

        if self.app.audio:
            self.app.audio.tocar_ambiente("ambiente")
            self.app.audio.tocar("nivel")

        self.load_level(1)

    def exit(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

        if self.app.audio:
            self.app.audio.parar_ambiente()

    def load_level(self, numero: int) -> None:
        self.level = Level(self.seed, numero)
        self.player = Player(self.level.start_x, self.level.start_y)

        seed_nivel = f"{self.seed}#{numero}"
        self.orbs = spawn_orbs(self.level.grid, self.level.start_x, self.level.start_y, seed_nivel)
        self.monstros = spawn_monsters(self.level.grid, self.level.start_x, self.level.start_y, seed_nivel)

        self.flowfield = FlowField(self.level.grid)
        self.tempo_nivel = 0.0
        self.tempo_restante = DURACAO_PARTIDA
        self.flash_dano = 0.0
        self._meio_ciclo = 0

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
            self.app.change_scene("MENU")

    def update(self, dt: float) -> None:
        assert self.player is not None and self.level is not None and self.flowfield is not None

        antes = self.tempo_nivel
        self.tempo_nivel += dt
        self.tempo_restante -= dt
        self.flash_dano = max(0.0, self.flash_dano - dt)

        # 1. Checar Derrota
        msg_derrota = checar_derrota(self.tempo_restante, self.player.hp)
        if msg_derrota:
            if self.app.audio:
                self.app.audio.tocar("gameover")
            self.app.scenes["FIM"].mensagem = msg_derrota
            self.app.change_scene("FIM")
            return

        # 2. Atualizar Player e Áudio de Passos
        keys = pg.key.get_pressed()
        mouse_dx, _ = pg.mouse.get_rel()
        self.player.update(keys, mouse_dx, dt, self.level.grid)
        self.app.aberracao = self.player.correndo_suave

        meio_ciclo = int(self.player.bobbing_ang // math.pi)
        if meio_ciclo != self._meio_ciclo:
            self._meio_ciclo = meio_ciclo
            if math.hypot(self.player.body.vx, self.player.body.vy) > 1.5 and self.app.audio:
                vol_passo = 0.6 + 0.4 * self.player.correndo_suave
                self.app.audio.tocar(f"passo{meio_ciclo % 2}", vol_passo)

        # 3. Coleta de Orbs
        for orb in self.orbs:
            if not orb.coletado and math.hypot(orb.x - self.player.x, orb.y - self.player.y) < RAIO_COLETA:
                orb.coletado = True
                if self.app.audio:
                    feitos = sum(1 for o in self.orbs if o.coletado)
                    self.app.audio.tocar(f"orb{(feitos - 1) % 3}")

        # 4. Checar Vitória
        if checar_vitoria(self.orbs):
            prox = proximo_nivel(self.level.numero)
            if prox:
                self.app.scenes["TRANSICAO"].iniciar(self.level.numero, prox)
                self.app.change_scene("TRANSICAO")
            else:
                if self.app.audio:
                    self.app.audio.tocar("vitoria")
                self.app.change_scene("VITORIA")
            return

        # 5. Despertar dos Monstros
        if antes < ATRASO_MONSTROS <= self.tempo_nivel:
            if self.app.audio:
                self.app.audio.tocar("despertar")

        # 6. Atualizar Monstros, Dano e Coração
        if self.tempo_nivel >= ATRASO_MONSTROS:
            p_cx = int(self.player.x // TAMANHO_BLOCO)
            p_cy = int(self.player.y // TAMANHO_BLOCO)
            self.flowfield.atualizar(p_cx, p_cy)

            for m in self.monstros:
                m.update(dt, self.player, self.flowfield, self.monstros, self.level.grid)
                dist = math.hypot(m.x - self.player.x, m.y - self.player.y)

                if dist < RAIO_CONTATO and self.player.invulneravel <= 0.0:
                    self.player.hp -= 1
                    self.player.invulneravel = INVULNERAVEL_DANO
                    self.flash_dano = 0.5
                    if self.app.audio:
                        self.app.audio.tocar("dano")

            # Cálculo do Coração (menor distância de caminho via BFS)
            melhor_passos = None
            for m in self.monstros:
                d = self.flowfield.dist[int(m.y // TAMANHO_BLOCO) * self.flowfield.n + int(m.x // TAMANHO_BLOCO)]
                if d >= 0 and (melhor_passos is None or d < melhor_passos):
                    melhor_passos = d
            if self.app.audio:
                self.app.audio.coracao(dt, melhor_passos)

        self.app.perigo = max(0.0, self.flash_dano / 0.5)

    def draw(self, surface: pg.Surface) -> None:
        assert self.player is not None and self.level is not None

        j = self.player
        H = surface.get_height()
        W = surface.get_width()
        t = pg.time.get_ticks() / 1000.0

        # 1. Mundo 3D
        draw_background(surface, self.level.background, bob_y=j.bobbing_y, tilt=j.tilt)
        draw_walls(
            surface,
            self.level.grid,
            j.camera,
            self.level.texture,
            self.zbuffer,
            bob_y=j.bobbing_y,
            tilt=j.tilt,
        )

        # 2. Entidades (Billboards)
        items = []

        # Orbs
        for orb in self.orbs:
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

        # Monstros
        for m in self.monstros:
            p = screen_column(j.camera, m.bx, m.by, W)
            if p is None:
                continue
            sx, perp = p
            if not (-100 <= sx <= W + 100):
                continue

            lh = line_height(H, perp)
            h = max(3, min(int(lh * 0.55 * (1.0 + 0.05 * math.sin(t * 9.0 + m.fase))), 300))
            w = max(1, int(h * m.sprite.get_width() / m.sprite.get_height()))

            spr = pg.transform.scale(m.sprite, (w, h))
            fog = max(0.25, 1.0 - perp * 0.03)
            s = int(255 * fog)
            spr.fill((s, s, s), special_flags=pg.BLEND_RGB_MULT)

            cy = horizon_y(H) + j.bobbing_y + lh * 0.5
            items.append(Billboard(perp, sx, spr, cy, anchor="bottom"))

        sort_by_perp_desc(items)
        draw_billboards(surface, items, self.zbuffer)

        # 3. HUD e Minimapa
        draw_minimap(surface, self.level.grid, j.x, j.y, j.camera.angle, j.camera.fov, TAMANHO_BLOCO)

        ox, oy = W - self.level.grid.n * 2 - 4, 4
        for orb in self.orbs:
            if orb.coletado:
                continue
            pg.draw.rect(surface, CORES_ORB[orb.cor_idx], (ox + orb.bx * 2 - 1, oy + orb.by * 2 - 1, 3, 3))
        for m in self.monstros:
            pg.draw.rect(surface, (255, 0, 0), (ox + m.bx * 2, oy + m.by * 2, 2, 2))

        self.app.hud.draw_gameplay(
            surface, j, self.orbs, self.tempo_restante, self.level.numero, TOTAL_NIVEIS, self.app.clock.fps
        )

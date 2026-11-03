from __future__ import annotations

import math
import random
import string

import pygame as pg

from engine.world.flowfield import FlowField
from game.config.balance import (
    DURACAO_PARTIDA,
    INVULNERAVEL_DANO,
    RAIO_COLETA,
    RAIO_CONTATO,
)
from game.config.constants import TAMANHO_BLOCO
from game.entities import Monster, Orb, Player
from game.levels import Level
from game.rules.spawning import spawn_monsters, spawn_orbs
from game.rules.win_lose import checar_derrota, checar_vitoria, proximo_nivel


class GameWorld:
    """Gerencia o estado, física e lógica de um nível."""

    def __init__(self, app, seed: str | None = None):
        self.app = app
        self.seed = seed or ""

        self.level: Level | None = None
        self.player: Player | None = None
        self.orbs: list[Orb] = []
        self.monstros: list[Monster] = []
        self.flowfield: FlowField | None = None

        self.tempo_nivel = 0.0
        self.tempo_restante = DURACAO_PARTIDA
        self.flash_dano = 0.0
        self._meio_ciclo = 0

    def iniciar_novo_jogo(self) -> None:
        self.seed = "".join(random.choices(string.ascii_lowercase + string.digits, k=16))

        self.load_level(1)
        if self.app.audio:
            self.app.audio.tocar("nivel")

    def load_level(self, numero: int) -> None:
        settings = self.app.settings

        self.level = Level(self.seed, numero, size=settings.map_size)
        self.player = Player(self.level.start_x, self.level.start_y)

        seed_nivel = f"{self.seed}#{numero}"
        self.orbs = spawn_orbs(self.level.grid, self.level.start_x, self.level.start_y, seed_nivel)
        self.monstros = spawn_monsters(self.level.grid, self.level.start_x, self.level.start_y, seed_nivel)

        self.flowfield = FlowField(self.level.grid)
        self.tempo_nivel = 0.0
        self.tempo_restante = DURACAO_PARTIDA * settings.time_mult
        self.flash_dano = 0.0
        self._meio_ciclo = 0

    def update(self, dt: float) -> str | None:
        """Atualiza a lógica. Retorna a próxima cena se algo acontecer (vitória/derrota)."""
        if not self.player or not self.level or not self.flowfield:
            return None

        antes = self.tempo_nivel
        self.tempo_nivel += dt
        self.tempo_restante -= dt
        self.flash_dano = max(0.0, self.flash_dano - dt)

        msg_derrota = checar_derrota(self.tempo_restante, self.player.hp)
        if msg_derrota:
            if self.app.audio:
                self.app.audio.tocar("gameover")
            self.app.scene_manager.scenes["FIM"].mensagem = msg_derrota
            return "FIM"

        keys = pg.key.get_pressed()
        mouse_dx, _ = pg.mouse.get_rel()
        self.player.update(keys, mouse_dx, dt, self.level.grid)
        self.app.aberracao = self.player.correndo_suave

        meio_ciclo = int(self.player.bobbing_ang // math.pi)
        if meio_ciclo != self._meio_ciclo:
            self._meio_ciclo = meio_ciclo
            if math.hypot(self.player.body.vx, self.player.body.vy) > 1.5 and self.app.audio:
                vol = 0.6 + 0.4 * self.player.correndo_suave
                self.app.audio.tocar(f"passo{meio_ciclo % 2}", vol)

        for orb in self.orbs:
            if not orb.coletado and math.hypot(orb.x - self.player.x, orb.y - self.player.y) < RAIO_COLETA:
                orb.coletado = True
                if self.app.audio:
                    feitos = sum(1 for o in self.orbs if o.coletado)
                    self.app.audio.tocar(f"orb{(feitos - 1) % 3}")

        if checar_vitoria(self.orbs):
            prox = proximo_nivel(self.level.numero)
            if prox:
                self.app.scene_manager.scenes["TRANSICAO"].iniciar(self.level.numero, prox)
                return "TRANSICAO"
            else:
                if self.app.audio:
                    self.app.audio.tocar("vitoria")
                return "VITORIA"

        atraso = self.app.settings.monster_delay
        if antes < atraso <= self.tempo_nivel:
            if self.app.audio:
                self.app.audio.tocar("despertar")

        if self.tempo_nivel >= atraso:
            p_cx = int(self.player.x // TAMANHO_BLOCO)
            p_cy = int(self.player.y // TAMANHO_BLOCO)
            self.flowfield.atualizar(p_cx, p_cy)

            for m in self.monstros:
                m.update(dt, self.player, self.flowfield, self.monstros, self.level.grid, self.app.settings.speed_mult)
                dist = math.hypot(m.x - self.player.x, m.y - self.player.y)

                if dist < RAIO_CONTATO and self.player.invulneravel <= 0.0:
                    self.player.hp -= 1
                    self.player.invulneravel = INVULNERAVEL_DANO
                    self.flash_dano = 0.5
                    self.app.glitch = 0.5
                    if self.app.audio:
                        self.app.audio.tocar("dano")

            melhor_passos = None
            for m in self.monstros:
                d = self.flowfield.dist[int(m.y // TAMANHO_BLOCO) * self.flowfield.n + int(m.x // TAMANHO_BLOCO)]
                if d >= 0 and (melhor_passos is None or d < melhor_passos):
                    melhor_passos = d
            if self.app.audio:
                self.app.audio.coracao(dt, melhor_passos)

        self.app.perigo = max(0.0, self.flash_dano / 0.5)
        self.app.glitch = max(0.0, self.flash_dano / 0.5)

        return None

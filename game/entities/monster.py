from __future__ import annotations

import math
import random

import pygame as pg

from engine.world.queries import has_line_of_sight
from game.config.balance import (
    FOV_VISAO,
    MONSTER_SEPARATION,
    MONSTER_WANDER_VEL_FRAC,
    PERDA_DELAY,
    RAIO_VISAO,
    VEL_MONSTRO,
    WANDER_PAUSA_MAX,
    WANDER_PAUSA_MIN,
    WANDER_RAIO_CELULAS,
)
from game.config.constants import TAMANHO_BLOCO
from game.entities.entity import Entity

MOLDES = [
    [
        "....####....",
        "..########..",
        ".##########.",
        ".##oo##oo##.",
        ".##oo##oo##.",
        ".##########.",
        ".##########.",
        ".###mmmm###.",
        ".##########.",
        "..########..",
        "..########..",
        "...######...",
        "..##.##.##..",
        "..##.##.##..",
    ],
    [
        ".##......##.",
        ".###....###.",
        ".##########.",
        ".##########.",
        ".#oo####oo#.",
        ".#oo####oo#.",
        ".##########.",
        ".##mmmmmm##.",
        ".##########.",
        ".##########.",
        "..########..",
        "..########..",
        "..##....##..",
        "..##....##..",
    ],
    [
        ".....##.....",
        ".....##.....",
        "....####....",
        "..########..",
        ".##########.",
        ".###oooo###.",
        ".##oooooo##.",
        ".##oooooo##.",
        ".###oooo###.",
        ".##########.",
        ".##########.",
        "..########..",
        "..#.####.#..",
        "..#..##..#..",
    ],
]
CORES_CREME = [(236, 224, 190), (240, 214, 178), (228, 226, 200)]


def _gerar_sprite(molde: list[str], base: tuple) -> pg.Surface:
    h, w = len(molde), len(molde[0])
    surf = pg.Surface((w, h), pg.SRCALPHA)
    escuro = tuple(int(c * 0.72) for c in base)
    claro = tuple(min(255, int(c * 1.06) + 6) for c in base)

    def corpo(x, y):
        return 0 <= x < w and 0 <= y < h and molde[y][x] != "."

    for y, linha in enumerate(molde):
        for x, ch in enumerate(linha):
            if ch == ".":
                continue
            if ch == "o":
                cor = (25, 15, 15)
            elif ch == "m":
                cor = (70, 40, 40)
            elif not corpo(x + 1, y) or not corpo(x, y + 1):
                cor = escuro
            elif not corpo(x - 1, y) or not corpo(x, y - 1):
                cor = claro
            else:
                cor = base
            surf.set_at((x, y), cor)
    return surf


SPRITES_MONSTROS = [_gerar_sprite(m, c) for m, c in zip(MOLDES, CORES_CREME)]

IDLE = "idle"
HUNTING = "hunting"


class Monster(Entity):
    __slots__ = (
        "variante",
        "fase",
        "sprite",
        "angle",
        "estado",
        "tempo_sem_ver",
        "wander_x",
        "wander_y",
        "wander_timer",
    )

    def __init__(self, x: float, y: float, variante: int, fase: float = 0.0):
        super().__init__(x, y, radius=12.0)
        self.variante = variante
        self.fase = fase
        self.sprite = SPRITES_MONSTROS[variante]
        self.angle = random.uniform(0, math.tau)
        self.estado = IDLE
        self.tempo_sem_ver = 0.0
        self.wander_x = x
        self.wander_y = y
        self.wander_timer = 0.0

    @property
    def bx(self) -> float:
        return self.x / TAMANHO_BLOCO

    @property
    def by(self) -> float:
        return self.y / TAMANHO_BLOCO

    def _pode_ver(self, player, grid) -> bool:
        dx = player.x - self.x
        dy = player.y - self.y
        d2 = dx * dx + dy * dy
        if d2 < 1e-3 or d2 > RAIO_VISAO * RAIO_VISAO:
            return False
        ang = math.atan2(dy, dx)
        diff = (ang - self.angle + math.pi) % math.tau - math.pi
        if abs(diff) > FOV_VISAO * 0.5:
            return False
        return has_line_of_sight(self.x, self.y, player.x, player.y, grid, TAMANHO_BLOCO)

    def _alvo_caca(self, player, flowfield):
        cx = int(self.x // TAMANHO_BLOCO)
        cy = int(self.y // TAMANHO_BLOCO)
        pcx = int(player.x // TAMANHO_BLOCO)
        pcy = int(player.y // TAMANHO_BLOCO)
        if (cx, cy) == (pcx, pcy):
            return player.x, player.y
        prox = flowfield.proximo(cx, cy)
        if prox is None:
            return self.x, self.y
        return prox[0] * TAMANHO_BLOCO + TAMANHO_BLOCO / 2, prox[1] * TAMANHO_BLOCO + TAMANHO_BLOCO / 2

    def _alvo_wander(self, dt, grid):
        self.wander_timer -= dt
        ddx = self.wander_x - self.x
        ddy = self.wander_y - self.y
        chegou = (ddx * ddx + ddy * ddy) < 64.0
        if self.wander_timer <= 0 or chegou:
            for _ in range(8):
                ang = random.uniform(0, math.tau)
                dist = random.uniform(1.5, WANDER_RAIO_CELULAS) * TAMANHO_BLOCO
                tx = self.x + math.cos(ang) * dist
                ty = self.y + math.sin(ang) * dist
                if not grid.is_solid(int(tx // TAMANHO_BLOCO), int(ty // TAMANHO_BLOCO)):
                    self.wander_x = tx
                    self.wander_y = ty
                    break
            self.wander_timer = random.uniform(WANDER_PAUSA_MIN, WANDER_PAUSA_MAX)
        return self.wander_x, self.wander_y

    def update(self, dt: float, player, flowfield, peers, grid) -> None:
        viu = self._pode_ver(player, grid)
        if viu:
            self.estado = HUNTING
            self.tempo_sem_ver = 0.0
        elif self.estado == HUNTING:
            self.tempo_sem_ver += dt
            if self.tempo_sem_ver > PERDA_DELAY:
                self.estado = IDLE
                self.wander_x = self.x
                self.wander_y = self.y
                self.wander_timer = 0.0

        if self.estado == HUNTING:
            alvo_x, alvo_y = self._alvo_caca(player, flowfield)
            vel = VEL_MONSTRO
        else:
            alvo_x, alvo_y = self._alvo_wander(dt, grid)
            vel = VEL_MONSTRO * MONSTER_WANDER_VEL_FRAC

        dx = alvo_x - self.x
        dy = alvo_y - self.y
        d = math.hypot(dx, dy)
        if d < 1e-4:
            return

        self.angle = math.atan2(dy, dx)
        passo = min(d, vel * dt)
        nx = self.x + (dx / d) * passo
        ny = self.y + (dy / d) * passo

        sep_r2 = MONSTER_SEPARATION * MONSTER_SEPARATION
        for other in peers:
            if other is self:
                continue
            ox = nx - other.x
            oy = ny - other.y
            od2 = ox * ox + oy * oy
            if 0.0 < od2 < sep_r2:
                od = math.sqrt(od2)
                f = (MONSTER_SEPARATION - od) / MONSTER_SEPARATION
                nx += (ox / od) * f * passo * 1.2
                ny += (oy / od) * f * passo * 1.2

        cx = int(nx // TAMANHO_BLOCO)
        cy = int(ny // TAMANHO_BLOCO)
        if not grid.is_solid(cx, cy):
            self.x = nx
            self.y = ny
        elif self.estado == IDLE:
            self.wander_timer = 0.0

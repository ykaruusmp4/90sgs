"""Jogador: corpo (física) + câmera (visão)."""

from __future__ import annotations

import math

import pygame as pg

from engine.camera import Camera
from engine.maths import damp
from engine.physics import move_body
from game.config.balance import (
    ARROW_GIRO,
    FOV_CORRENDO,
    FOV_NORMAL,
    RAIO_JOGADOR,
    SENSIBILIDADE_MOUSE,
    VEL_FRAME_ANDAR,
    VEL_FRAME_CORRIDA,
)
from game.config.constants import TAMANHO_BLOCO
from game.entities.entity import Entity

STAMINA_MAX = 100.0
STAMINA_GASTO = 45.0  # por segundo correndo
STAMINA_REGEN = 20.0  # por segundo parado/andando


class Player(Entity):
    __slots__ = (
        "camera",
        "hp",
        "stamina",
        "folego_esgotado",
        "correndo_suave",
        "bobbing_ang",
        "bobbing_y",
        "tilt",
        "invulneravel",
    )

    def __init__(self, x: float, y: float):
        super().__init__(x, y, RAIO_JOGADOR)
        self.camera = Camera(x, y, angle=0.0, fov=FOV_NORMAL)
        self.hp = 3
        self.stamina = STAMINA_MAX
        self.folego_esgotado = False
        self.correndo_suave = 0.0
        self.bobbing_ang = 0.0
        self.bobbing_y = 0.0
        self.tilt = 0.0
        self.invulneravel = 0.0

    def update(self, keys, mouse_dx: int, dt: float, grid) -> None:
        b = self.body
        cam = self.camera

        # --- Rotação: mouse + setas ---
        if mouse_dx:
            self._set_angle(self._angle() + mouse_dx * SENSIBILIDADE_MOUSE)
        if keys[pg.K_LEFT]:
            self._set_angle(self._angle() - ARROW_GIRO * dt)
        if keys[pg.K_RIGHT]:
            self._set_angle(self._angle() + ARROW_GIRO * dt)

        shift = keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]

        if self.stamina <= 1.0:
            self.folego_esgotado = True
        elif self.stamina >= 25.0 and not shift:
            self.folego_esgotado = False

        quer_mover = keys[pg.K_w] or keys[pg.K_s] or keys[pg.K_a] or keys[pg.K_d]
        correndo = shift and not self.folego_esgotado and quer_mover

        ang = self._angle()
        fx, fy = math.cos(ang), math.sin(ang)
        rx, ry = -fy, fx  # right = perp de forward (y pra baixo → roda 90°)

        dx = dy = 0.0
        alvo_tilt = 0.0
        andou = False
        if keys[pg.K_w]:
            dx += fx
            dy += fy
            andou = True
        if keys[pg.K_s]:
            dx -= fx
            dy -= fy
            andou = True
        if keys[pg.K_a]:
            dx -= rx
            dy -= ry
            alvo_tilt = 3.5 if correndo else 2.0
            andou = True
        if keys[pg.K_d]:
            dx += rx
            dy += ry
            alvo_tilt = -3.5 if correndo else -2.0
            andou = True

        mag = math.hypot(dx, dy)
        if mag > 1e-6:
            dx /= mag
            dy /= mag

        # --- Aceleração snappy (damp) ---
        target_speed = VEL_FRAME_CORRIDA if correndo else VEL_FRAME_ANDAR
        if andou:
            b.vx = damp(b.vx, dx * target_speed, 0.55, dt)
            b.vy = damp(b.vy, dy * target_speed, 0.55, dt)
        else:
            b.vx = damp(b.vx, 0.0, 0.5, dt)
            b.vy = damp(b.vy, 0.0, 0.5, dt)

        # --- Stamina ---
        if correndo and andou:
            self.stamina = max(0.0, self.stamina - STAMINA_GASTO * dt)
        else:
            self.stamina = min(STAMINA_MAX, self.stamina + STAMINA_REGEN * dt)

        move_body(b, grid, TAMANHO_BLOCO, dt)

        cam.move_to(b.x / TAMANHO_BLOCO, b.y / TAMANHO_BLOCO)
        cam.set_fov(damp(cam.fov, FOV_CORRENDO if correndo else FOV_NORMAL, 0.85, dt))
        self.correndo_suave = damp(self.correndo_suave, 1.0 if correndo else 0.0, 0.85, dt)
        self.tilt = damp(self.tilt, alvo_tilt, 0.85, dt)

        if andou and (abs(b.vx) > 0.2 or abs(b.vy) > 0.2):
            freq = 0.40 if correndo else 0.24
            amp = 4.0 if correndo else 2.0
            self.bobbing_ang += freq * (dt * 60.0)
            self.bobbing_y = math.sin(self.bobbing_ang) * amp
        else:
            self.bobbing_ang += 0.02 * (dt * 60.0)
            self.bobbing_y = math.sin(self.bobbing_ang) * 0.05

        self.invulneravel = max(0.0, self.invulneravel - dt)

    def _angle(self) -> float:
        return self.camera.angle

    def _set_angle(self, a: float) -> None:
        self.camera.set_angle(a)

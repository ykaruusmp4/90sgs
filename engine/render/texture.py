from __future__ import annotations

import random

import pygame as pg

from .palette import RGB, clamp255


def background(
    ceiling: RGB,
    floor: RGB,
    width: int,
    height: int,
    *,
    escuro_no_meio: float = 0.4,
    claro_nas_pontas: float = 1.4,
) -> pg.Surface:
    surf = pg.Surface((width, height))
    meio = height // 2
    for y in range(height):
        if y < meio:
            t = (meio - y) / meio
            base = ceiling
        else:
            t = (y - meio) / (height - meio) if height > meio else 0.0
            base = floor
        f = escuro_no_meio + (claro_nas_pontas - escuro_no_meio) * t
        cor = (clamp255(base[0] * f), clamp255(base[1] * f), clamp255(base[2] * f))
        pg.draw.line(surf, cor, (0, y), (width - 1, y))
    return surf


def wall_texture(
    base: RGB,
    seed: int,
    size: int = 64,
    *,
    alt_tijolo: int = 16,
    larg_tijolo: int = 32,
    argamassa_fator: float = 0.22,
    variacao_grao: int = 260,
) -> pg.Surface:
    rng = random.Random(seed)
    argamassa = tuple(clamp255(c * argamassa_fator) for c in base)
    tex = pg.Surface((size, size))
    tex.fill(argamassa)

    for fileira in range(size // alt_tijolo):
        desloc = larg_tijolo // 2 if fileira % 2 else 0
        for col in range(size // larg_tijolo):
            x0 = col * larg_tijolo + desloc
            brilho = rng.uniform(0.72, 1.08)
            cor = tuple(clamp255(c * brilho) for c in base)
            for xx in (x0, x0 - size):
                tex.fill(cor, pg.Rect(xx + 1, fileira * alt_tijolo + 1, larg_tijolo - 2, alt_tijolo - 2))

    for _ in range(variacao_grao):
        x, y = rng.randrange(size), rng.randrange(size)
        r, g, b = tex.get_at((x, y))[:3]
        v = rng.uniform(0.7, 1.15)
        tex.set_at((x, y), (clamp255(r * v), clamp255(g * v), clamp255(b * v)))
    return tex


def radial_glow(cor: RGB, size: int = 32) -> pg.Surface:
    surf = pg.Surface((size, size))
    surf.fill((0, 0, 0))
    c = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5 / c
            if d >= 1.0:
                continue
            halo = (1.0 - d) ** 2
            nucleo = max(0.0, 1.0 - d / 0.35) ** 1.5
            surf.set_at(
                (x, y),
                (
                    clamp255(cor[0] * halo + 255 * nucleo),
                    clamp255(cor[1] * halo + 255 * nucleo),
                    clamp255(cor[2] * halo + 255 * nucleo),
                ),
            )
    return surf

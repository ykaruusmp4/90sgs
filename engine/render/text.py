from __future__ import annotations

import math

import pygame as pg

from .bitmap_font import COR_SOMBRA, BitmapFont

ESPACO_PADRAO = 7
ESPECIAIS = "Ê"


def put_char(surf: pg.Surface, font: BitmapFont, ch: str, x: int, y: int, color_idx: int = 0) -> None:
    if ch == "Ê":
        base = font.glyph("E", color_idx)
        chapeu = font.chapeu(color_idx)
        if base:
            surf.blit(base, (x, y))
        if chapeu:
            surf.blit(chapeu, (x, y - 2))
        return
    g = font.glyph(ch, color_idx)
    if g:
        surf.blit(g, (x, y))


def put_text(
    surf: pg.Surface,
    font: BitmapFont,
    text: str,
    x: int,
    y: int,
    color_idx: int = 0,
    espacamento: int = ESPACO_PADRAO,
    sombra: bool = False,
) -> None:
    if sombra:
        put_text(surf, font, text, x + 1, y + 1, COR_SOMBRA, espacamento, False)
    xa = x
    for ch in text:
        put_char(surf, font, ch, xa, y, color_idx)
        xa += espacamento


def put_text_centered(
    surf: pg.Surface,
    font: BitmapFont,
    text: str,
    y: int,
    color_idx: int = 0,
    espacamento: int = ESPACO_PADRAO,
    sombra: bool = False,
) -> None:
    largura = (len(text) * espacamento) - (espacamento - font.largura)
    x = (surf.get_width() - largura) // 2
    put_text(surf, font, text, x, y, color_idx, espacamento, sombra)


def put_text_wave(
    surf: pg.Surface,
    font: BitmapFont,
    text: str,
    y: int,
    t: float,
    color_idx: int = 0,
    espacamento: int = ESPACO_PADRAO,
    amplitude: float = 2.0,
) -> None:
    largura = (len(text) * espacamento) - (espacamento - font.largura)
    x = (surf.get_width() - largura) // 2
    for i, ch in enumerate(text):
        dy = round(math.sin(t * 3.0 + i * 0.6) * amplitude)
        put_char(surf, font, ch, x + 1, y + dy + 1, COR_SOMBRA)
        put_char(surf, font, ch, x, y + dy, color_idx)
        x += espacamento

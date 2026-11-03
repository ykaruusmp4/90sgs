from __future__ import annotations

import math

import pygame as pg

from .bitmap_font import COR_SOMBRA, BitmapFont

ESPACO_PADRAO = 7
ESPECIAIS = "Ê"


def medir_texto(font: BitmapFont, text: str, escala: int = 1, espacamento: int | None = None) -> int:
    if not text:
        return 0
    esp = (ESPACO_PADRAO if espacamento is None else espacamento) * escala
    return len(text) * esp - (esp - font.largura * escala)


def put_char(surf: pg.Surface, font: BitmapFont, ch: str, x: int, y: int, color_idx: int = 0, escala: int = 1) -> None:
    if ch == "Ê":
        base = font.glyph("E", color_idx, escala)
        chapeu = font.chapeu(color_idx, escala)
        if base:
            surf.blit(base, (x, y))
        if chapeu:
            surf.blit(chapeu, (x, y - 2 * escala))
        return
    g = font.glyph(ch, color_idx, escala)
    if g:
        surf.blit(g, (x, y))


def put_text(
    surf: pg.Surface,
    font: BitmapFont,
    text: str,
    x: int,
    y: int,
    color_idx: int = 0,
    espacamento: int | None = None,
    sombra: bool = False,
    escala: int = 1,
) -> None:
    esp = (ESPACO_PADRAO if espacamento is None else espacamento) * escala
    if sombra:
        put_text(surf, font, text, x + escala, y + escala, COR_SOMBRA, espacamento, False, escala)
    xa = x
    for ch in text:
        put_char(surf, font, ch, xa, y, color_idx, escala)
        xa += esp


def put_text_centered(
    surf: pg.Surface,
    font: BitmapFont,
    text: str,
    y: int,
    color_idx: int = 0,
    espacamento: int | None = None,
    sombra: bool = False,
    escala: int = 1,
) -> None:
    x = (surf.get_width() - medir_texto(font, text, escala, espacamento)) // 2
    put_text(surf, font, text, x, y, color_idx, espacamento, sombra, escala)


def put_text_wave(
    surf: pg.Surface,
    font: BitmapFont,
    text: str,
    y: int,
    t: float,
    color_idx: int = 0,
    espacamento: int | None = None,
    amplitude: float = 2.0,
    escala: int = 1,
) -> None:
    esp = (ESPACO_PADRAO if espacamento is None else espacamento) * escala
    x = (surf.get_width() - medir_texto(font, text, escala, espacamento)) // 2
    for i, ch in enumerate(text):
        dy = round(math.sin(t * 3.0 + i * 0.6) * amplitude * escala)
        put_char(surf, font, ch, x + escala, y + dy + escala, COR_SOMBRA, escala)
        put_char(surf, font, ch, x, y + dy, color_idx, escala)
        x += esp

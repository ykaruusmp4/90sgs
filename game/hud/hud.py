import math

import pygame as pg

from engine.render import BitmapFont, put_text, put_text_centered, put_text_wave
from game.config.constants import CORES_HUD_FONTE, FONTE_HUD, VERSAO

BRANCO, VERMELHO, VERDE, CINZA, AZUL, AMARELO = 0, 1, 2, 3, 4, 5
COR_SOMBRA = -1


class HUD:
    def __init__(self):
        self.font = BitmapFont(str(FONTE_HUD), CORES_HUD_FONTE)

    def draw_gameplay(
        self, surf: pg.Surface, player, orbs: list, tempo: float, nivel: int, total_niveis: int, fps: int
    ):
        W = surf.get_width()
        H = surf.get_height()
        painel_y = H - 24

        pg.draw.rect(surf, (8, 8, 8), (0, painel_y, W, 24))
        pg.draw.line(surf, (30, 30, 30), (0, painel_y), (W, painel_y), 1)

        put_text(surf, self.font, f"{nivel}/{total_niveis}", 4, 4, color_idx=BRANCO, sombra=True)

        put_text(surf, self.font, "HP", 6, painel_y + 8, color_idx=VERMELHO)
        for i in range(3):
            cor = (220, 40, 40) if i < player.hp else (40, 15, 15)
            pg.draw.rect(surf, cor, (24 + (i * 14), painel_y + 8, 10, 8))

        pg.draw.rect(surf, (20, 20, 20), (72, painel_y + 8, 40, 8))
        largura_st = int(40 * max(0.0, min(1.0, player.stamina / 100.0)))
        if largura_st > 0:
            if player.folego_esgotado:
                cor_st = (220, 40, 40) if int(pg.time.get_ticks() / 125) % 2 == 0 else (90, 25, 25)
            else:
                cor_st = (0, 150, 255)
            pg.draw.rect(surf, cor_st, (72, painel_y + 8, largura_st, 8))

        segundos = int(math.ceil(max(0.0, tempo)))
        urgente = tempo <= 10 and int(pg.time.get_ticks() / 250) % 2 == 0
        cor_tempo = VERMELHO if urgente else BRANCO
        put_text(surf, self.font, str(segundos), 125, painel_y + 8, color_idx=cor_tempo)
        put_text(surf, self.font, "sgs", 125 + len(str(segundos)) * 7 + 3, painel_y + 8, color_idx=CINZA)

        for i, orb in enumerate(orbs):
            x = 168 + i * 11
            y = painel_y + 8
            cor_orb = [(255, 220, 60), (60, 230, 255), (255, 80, 220)][orb.cor_idx]
            if orb.coletado:
                pg.draw.rect(surf, cor_orb, (x, y, 8, 8))
            else:
                pg.draw.rect(surf, tuple(c // 6 for c in cor_orb), (x, y, 8, 8))
                pg.draw.rect(surf, tuple(c // 3 for c in cor_orb), (x, y, 8, 8), 1)

        put_text(surf, self.font, f"FPS {fps}", W - 54, painel_y + 8, color_idx=VERDE)

    def draw_menu(self, surf: pg.Surface, titulo: str, opcoes: list[str], selecionada: int, t: float, seed: str = ""):
        surf.fill((10, 10, 12))
        put_text_wave(surf, self.font, titulo, 40, t, color_idx=VERMELHO)
        y = 100
        for i, texto in enumerate(opcoes):
            ativo = i == selecionada
            prefixo = "> " if ativo else "  "
            put_text_centered(surf, self.font, prefixo + texto, y, color_idx=BRANCO if ativo else CINZA)
            y += 20

        W = surf.get_width()
        H = surf.get_height()

        # Seed no canto inferior esquerdo
        if seed:
            put_text(surf, self.font, f"SEED {seed}", 4, H - 14, color_idx=CINZA)

        # Versão no canto inferior direito
        x_versao = W - len(VERSAO) * 7 - 4
        put_text(surf, self.font, VERSAO, x_versao, H - 14, color_idx=CINZA)

    def draw_fim(self, surf: pg.Surface, mensagem: str, t: float):
        surf.fill((10, 10, 12))
        put_text_wave(surf, self.font, mensagem, 90, t, color_idx=VERMELHO)
        if int(t * 2) % 2 == 0:
            put_text_centered(surf, self.font, "ENTER", 130, color_idx=CINZA)

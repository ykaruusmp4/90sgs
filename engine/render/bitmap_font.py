"""Fonte bitmap parseada de arquivo + cache de glifos por cor.

Formato do arquivo (P16font.txt): cada linha = `codigo_hex,row0,row1,...,rowN`.
Cada `row` é uma máscara de 8 bits (bit 7 = coluna 0).

`COR_SOMBRA = -1` é o índice especial reservado pra sombra.
"""

from __future__ import annotations

import pygame as pg

COR_SOMBRA = -1
GLIFO_FALLBACK = "?"


class BitmapFont:
    __slots__ = ("data", "cache", "altura", "largura", "_paleta")

    def __init__(
        self,
        caminho_txt: str,
        paleta: list[tuple[int, int, int]],
        largura: int = 8,
        altura: int = 8,
    ):
        self.largura = largura
        self.altura = altura
        self.data: dict[int, list[int]] = {}
        self.cache: dict[int, dict[int | str, pg.Surface]] = {}
        self._paleta = paleta
        self._carregar(caminho_txt)
        self._construir_cache()

    def _carregar(self, caminho: str) -> None:
        try:
            with open(caminho, encoding="utf-8") as arq:
                for linha in arq:
                    linha = linha.strip()
                    if not linha:
                        continue
                    partes = [x.strip() for x in linha.split(",") if x.strip()]
                    if not partes:
                        continue
                    valores = [int(x, 16) for x in partes]
                    self.data[valores[0]] = valores[1:]
        except FileNotFoundError:
            print(f"[FONT] fonte não encontrada: {caminho}")

    def _construir_cache(self) -> None:
        cores: dict[int, tuple[int, int, int]] = {i: rgb for i, rgb in enumerate(self._paleta)}
        cores[COR_SOMBRA] = (0, 0, 0)

        for color_idx, rgb in cores.items():
            bucket: dict[int | str, pg.Surface] = {}
            for code, rows in self.data.items():
                bucket[code] = self._raster(rows, rgb)

            # O chapeu usa os mesmos bits só que menor (2 linhas)
            bucket["chapeu"] = self._raster([0x0C, 0x1E], rgb)
            self.cache[color_idx] = bucket

    def _raster(self, rows: list[int], rgb: tuple[int, int, int]) -> pg.Surface:
        """Desenha uma lista de bytes (máscaras de 8 bits) numa Surface."""
        w = self.largura
        h = len(rows)
        surf = pg.Surface((w, max(h, self.altura)), pg.SRCALPHA)

        for r, row in enumerate(rows):
            for c in range(w):
                if (row >> (7 - c)) & 1:
                    surf.set_at((c, r), rgb)
        return surf

    def glyph(self, ch: str, color_idx: int) -> pg.Surface | None:
        bucket = self.cache.get(color_idx) or self.cache.get(0)
        if bucket is None:
            return None
        return bucket.get(ord(ch)) or bucket.get(ord(GLIFO_FALLBACK))

    def chapeu(self, color_idx: int) -> pg.Surface | None:
        bucket = self.cache.get(color_idx) or self.cache.get(0)
        if bucket is None:
            return None
        return bucket.get("chapeu")

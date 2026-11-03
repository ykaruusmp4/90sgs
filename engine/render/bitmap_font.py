from __future__ import annotations

import pygame as pg

COR_SOMBRA = -1
GLIFO_FALLBACK = "?"


class BitmapFont:
    __slots__ = ("data", "cache", "altura", "largura", "_paleta", "_esc")

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
        self._esc: dict[tuple, pg.Surface] = {}
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

            bucket["chapeu"] = self._raster([0x0C, 0x1E], rgb)
            self.cache[color_idx] = bucket

    def _raster(self, rows: list[int], rgb: tuple[int, int, int]) -> pg.Surface:
        w = self.largura
        h = len(rows)
        surf = pg.Surface((w, max(h, self.altura)), pg.SRCALPHA)

        for r, row in enumerate(rows):
            for c in range(w):
                if (row >> (7 - c)) & 1:
                    surf.set_at((c, r), rgb)
        return surf

    def _escalar(self, base: pg.Surface | None, chave: tuple, escala: int) -> pg.Surface | None:
        if base is None or escala == 1:
            return base
        s = self._esc.get(chave)
        if s is None:
            s = pg.transform.scale(base, (base.get_width() * escala, base.get_height() * escala))
            self._esc[chave] = s
        return s

    def glyph(self, ch: str, color_idx: int, escala: int = 1) -> pg.Surface | None:
        bucket = self.cache.get(color_idx) or self.cache.get(0)
        if bucket is None:
            return None
        base = bucket.get(ord(ch)) or bucket.get(ord(GLIFO_FALLBACK))
        return self._escalar(base, (escala, color_idx, ch), escala)

    def chapeu(self, color_idx: int, escala: int = 1) -> pg.Surface | None:
        bucket = self.cache.get(color_idx) or self.cache.get(0)
        if bucket is None:
            return None
        return self._escalar(bucket.get("chapeu"), (escala, color_idx, "chapeu"), escala)

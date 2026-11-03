from __future__ import annotations

import re
import time
from array import array
from pathlib import Path

import moderngl as mgl
import pygame as pg

_INCLUDE = re.compile(r'^\s*#include\s+"([^"]+)"\s*$')


def load_shader_source(caminho: str | Path) -> str:
    return _expand(Path(caminho), set())


def _expand(caminho: Path, seen: set[Path]) -> str:
    caminho = caminho.resolve()
    if caminho in seen:
        return f"// (ja incluido: {caminho.name})\n"
    seen.add(caminho)
    linhas = []
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        m = _INCLUDE.match(linha)
        if m:
            linhas.append(f"// >>> {m.group(1)}")
            linhas.append(_expand(caminho.parent / m.group(1), seen))
            linhas.append(f"// <<< {m.group(1)}")
        else:
            linhas.append(linha)
    return "\n".join(linhas) + "\n"


class ShaderPipeline:
    __slots__ = ("largura", "altura", "ctx", "programa", "vao", "textura_tela", "_t0")

    def __init__(self, largura: int, altura: int, caminho_vertex: str, caminho_fragment: str):
        self.largura = largura
        self.altura = altura
        self._t0 = time.perf_counter()

        self.ctx = mgl.create_context()
        self.programa = self.ctx.program(
            vertex_shader=load_shader_source(caminho_vertex),
            fragment_shader=load_shader_source(caminho_fragment),
        )

        quad = array(
            "f",
            [
                -1.0,
                1.0,
                0.0,
                1.0,
                -1.0,
                -1.0,
                0.0,
                0.0,
                1.0,
                1.0,
                1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
                0.0,
            ],
        )
        vbo = self.ctx.buffer(quad)
        self.vao = self.ctx.vertex_array(self.programa, [(vbo, "2f 2f", "in_vert", "in_texcoord")])

        self.textura_tela = self.ctx.texture((largura, altura), 4)
        self.textura_tela.repeat_x = False
        self.textura_tela.repeat_y = False
        self.textura_tela.filter = (mgl.NEAREST, mgl.NEAREST)

        self._uniform("tex", 0)
        self._uniform("u_res", (float(largura), float(altura)))
        self._uniform("u_crt", 1.0)
        self._uniform("u_aberracao", 0.0)
        self._uniform("u_perigo", 0.0)
        self._uniform("u_dither", 1.0)

    def _uniform(self, nome: str, valor) -> None:
        if nome in self.programa:
            self.programa[nome].value = valor

    def _ajustar_viewport(self) -> None:
        w, h = pg.display.get_window_size()
        escala = min(w / self.largura, h / self.altura)
        vw = max(1, int(self.largura * escala))
        vh = max(1, int(self.altura * escala))
        self.ctx.viewport = (0, 0, w, h)
        self.ctx.clear(0, 0, 0)
        self.ctx.viewport = ((w - vw) // 2, (h - vh) // 2, vw, vh)

    def render(self, superficie_jogo: pg.Surface, **uniformes) -> None:
        self._uniform("u_time", time.perf_counter() - self._t0)
        for nome, valor in uniformes.items():
            self._uniform(nome, valor)

        self.textura_tela.write(pg.image.tobytes(superficie_jogo, "RGBA", True))
        self._ajustar_viewport()
        self.textura_tela.use(location=0)
        self.vao.render(mgl.TRIANGLE_STRIP)

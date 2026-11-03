import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    _RAIZ = Path(sys._MEIPASS)
else:
    _RAIZ = Path(__file__).resolve().parent.parent.parent

ASSETS = _RAIZ / "assets"
FONTES = ASSETS / "fonts"
SHADERS = ASSETS / "shaders"

FONTE_HUD = FONTES / "P16font.txt"
SHADER_VS = SHADERS / "post.vs"
SHADER_POST = SHADERS / "post_process.fs"

LARGURA_VIRTUAL = 256
ALTURA_VIRTUAL = 224
ESCALE = 4
LARGURA_JANELA = LARGURA_VIRTUAL * ESCALE
ALTURA_JANELA = ALTURA_VIRTUAL * ESCALE

TAMANHO_BLOCO = 64
TAM_TEXTURA = 64
MARGEM_FUNDO = 24

CORES_HUD_FONTE = [
    (255, 255, 255),
    (220, 40, 40),
    (50, 200, 50),
    (140, 140, 140),
    (0, 160, 255),
    (255, 220, 60),
]

TOTAL_NIVEIS = 10
ORBS_POR_NIVEL = 3
CORES_ORB = [
    (255, 220, 60),
    (60, 230, 255),
    (255, 80, 220),
]

VERSAO = "v0.1.0-indev"

__all__ = [
    "ASSETS",
    "FONTES",
    "SHADERS",
    "FONTE_HUD",
    "SHADER_VS",
    "SHADER_POST",
    "LARGURA_VIRTUAL",
    "ALTURA_VIRTUAL",
    "ESCALE",
    "LARGURA_JANELA",
    "ALTURA_JANELA",
    "TAMANHO_BLOCO",
    "TAM_TEXTURA",
    "MARGEM_FUNDO",
    "CORES_HUD_FONTE",
    "TOTAL_NIVEIS",
    "ORBS_POR_NIVEL",
    "CORES_ORB",
    "VERSAO",
]

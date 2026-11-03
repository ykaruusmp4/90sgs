"""Constantes de infraestrutura — não devem mudar por gameplay.

Caminhos resolvidos a partir da raiz do projeto (`90sgs/`).
"""

from pathlib import Path

# --- Caminhos --------------------------------------------------------------
_RAIZ = Path(__file__).resolve().parent.parent.parent
ASSETS = _RAIZ / "assets"
FONTES = ASSETS / "fonts"
SHADERS = ASSETS / "shaders"

FONTE_HUD = FONTES / "P16font.txt"
SHADER_VS = SHADERS / "post.vs"
SHADER_POST = SHADERS / "post_process.fs"

# --- Resolução virtual -----------------------------------------------------
LARGURA_VIRTUAL = 256
ALTURA_VIRTUAL = 224
ESCALE = 4
LARGURA_JANELA = LARGURA_VIRTUAL * ESCALE
ALTURA_JANELA = ALTURA_VIRTUAL * ESCALE

# --- Unidades de render ----------------------------------------------------
TAMANHO_BLOCO = 64  # pixels por célula do grid
TAM_TEXTURA = 64  # px do tile de parede
MARGEM_FUNDO = 24  # margem vertical do fundo (parallax de bob/tilt)

# --- HUD -------------------------------------------------------------------
CORES_HUD_FONTE = [
    (255, 255, 255),
    (220, 40, 40),
    (50, 200, 50),
    (140, 140, 140),
    (0, 160, 255),
    (255, 220, 60),
]

# --- Progressão ------------------------------------------------------------
TOTAL_NIVEIS = 10
VERSAO = "v0.1.0-indev"
ORBS_POR_NIVEL = 3
CORES_ORB = [(255, 220, 60), (60, 230, 255), (255, 80, 220)]

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
]

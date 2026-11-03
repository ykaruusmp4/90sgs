"""Tuning de gameplay — mexa aqui pra balancear, não em `constants.py`."""

import math

# --- Movimento do jogador --------------------------------------------------
ATRITO = 0.82
ACELERACAO = 1.2
RAIO_JOGADOR = 14
VEL_ANDAR = 1.1
VEL_CORRIDA = 2.0
VEL_GIRO = 2.7

FOV_NORMAL = math.pi / 3
FOV_CORRENDO = math.pi / 2.6

# --- Mouse -----------------------------------------------------------------
SENSIBILIDADE_MOUSE = 0.0025  # radianos por pixel de mouse
ARROW_GIRO = VEL_GIRO  # setas esq/dir pra girar como fallback

# --- Player: velocidades per-frame (pra usar com damp) ---------------------
VEL_FRAME_ANDAR = VEL_ANDAR * ACELERACAO * ATRITO / (1.0 - ATRITO)
VEL_FRAME_CORRIDA = VEL_CORRIDA * ACELERACAO * ATRITO / (1.0 - ATRITO)

# --- Sessão ----------------------------------------------------------------
DURACAO_PARTIDA = 90.0
TAMANHO_MAPA = 48

# --- Paletas por nível -----------------------------------------------------
PALETAS = {
    0: {"teto": (15, 18, 22), "chao": (8, 8, 10), "base_parede": (180, 0, 0)},
    1: {"teto": (12, 22, 12), "chao": (6, 10, 6), "base_parede": (0, 140, 50)},
    2: {"teto": (15, 15, 26), "chao": (8, 8, 14), "base_parede": (0, 80, 180)},
}

# --- Orbs ------------------------------------------------------------------
RAIO_COLETA = 45.0
TAM_ORB = 0.28

# --- Monstros --------------------------------------------------------------
MONSTROS_POR_NIVEL = 3
MULT_VEL_MONSTRO = 0.88
VEL_MONSTRO = VEL_FRAME_ANDAR * 60.0 * MULT_VEL_MONSTRO  # Aproximação px/s
RAIO_CONTATO = 22.0
ATRASO_MONSTROS = 4.5
INVULNERAVEL_DANO = 1.5

# --- IA do monstro --------------------------------------------------------
RAIO_VISAO = 12.0 * 64  # 12 células
FOV_VISAO = math.pi * 0.66  # ~120 graus de cone
PERDA_DELAY = 3.0  # segundos sem ver antes de voltar a vagar
WANDER_PAUSA_MIN = 0.8
WANDER_PAUSA_MAX = 2.5
WANDER_RAIO_CELULAS = 3.0  # raio de vagar, em células
MONSTER_SEPARATION = 22.0  # px de repulsão entre monstros
MONSTER_WANDER_VEL_FRAC = 0.4  # velocidade enquanto vaga (fração da normal)

# --- Áudio -----------------------------------------------------------------
VOL_MESTRE = 0.5


def vel_terminal(vel_input: float) -> float:
    """px/s que o jogador atinge segurando a tecla (aceleração + atrito)."""
    return vel_input * ACELERACAO * ATRITO / (1.0 - ATRITO) * 60.0


VEL_JOGADOR_ANDANDO = vel_terminal(VEL_ANDAR)
VEL_JOGADOR_CORRENDO = vel_terminal(VEL_CORRIDA)

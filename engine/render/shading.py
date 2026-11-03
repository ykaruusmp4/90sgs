"""Fatores de escurecimento por distância (fog)."""

FOG = 0.03  # mesmo valor da original
SIDE_DARKEN = 0.60  # face horizontal mais escura (simula iluminação)
MIN_BRIGHT_SPRITE = 0.25


def wall_fog(perp: float, side: int) -> float:
    """Fator 0..1 para multiplicar a cor da parede.

    Faces horizontais (side=1) levam escurecimento extra pra dar leitura de
    volume — mesma regra da `renderizar_cenario` original.
    """
    f = 1.0 - perp * FOG
    if f < 0.0:
        f = 0.0
    elif f > 1.0:
        f = 1.0
    if side == 1:
        f *= SIDE_DARKEN
    return f


def sprite_fog(perp: float, min_bright: float = MIN_BRIGHT_SPRITE) -> float:
    """Fator 0..1 para sprites. Nunca cai abaixo de `min_bright`."""
    f = 1.0 - perp * FOG
    if f < min_bright:
        return min_bright
    if f > 1.0:
        return 1.0
    return f

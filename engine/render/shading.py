FOG = 0.03
SIDE_DARKEN = 0.60
MIN_BRIGHT_SPRITE = 0.25


def wall_fog(perp: float, side: int) -> float:
    f = 1.0 - perp * FOG
    if f < 0.0:
        f = 0.0
    elif f > 1.0:
        f = 1.0
    if side == 1:
        f *= SIDE_DARKEN
    return f


def sprite_fog(perp: float, min_bright: float = MIN_BRIGHT_SPRITE) -> float:
    f = 1.0 - perp * FOG
    if f < min_bright:
        return min_bright
    if f > 1.0:
        return 1.0
    return f

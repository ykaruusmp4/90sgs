import math

from .envelope import apply_envelope
from .oscillators import noise, saw, square, triangle

TAXA = 22050


def tom(
    f0: float,
    f1: float,
    dur: float,
    onda: str = "square",
    duty: float = 0.5,
    vol: float = 0.5,
    ataque: float = 0.004,
    soltar: float = 0.02,
    decai: float = 0.0,
    curva: float = 1.0,
    vib: float = 0.0,
    vib_hz: float = 6.0,
) -> list[float]:
    n = max(1, int(dur * TAXA))
    inv = 1.0 / TAXA
    fase = 0.0
    base = [0.0] * n

    for i in range(n):
        u = i / n
        f = f0 + (f1 - f0) * (u**curva)
        if vib:
            f *= 1.0 + vib * math.sin(6.283185 * vib_hz * i * inv)

        fase += f * inv
        if fase >= 1.0:
            fase -= int(fase)

        if onda == "square":
            s = square(f, duty, fase)
        elif onda == "triangle":
            s = triangle(fase)
        elif onda == "saw":
            s = saw(fase)
        else:
            s = noise()

        base[i] = s * vol

    return apply_envelope(base, TAXA, ataque, soltar, decai)


def misturar(*camadas) -> list[float]:
    itens = []
    for c in camadas:
        if isinstance(c, tuple):
            itens.append((c[0], int(c[1] * TAXA)))
        else:
            itens.append((c, 0))
    n = max(o + len(a) for a, o in itens)
    out = [0.0] * n
    for a, o in itens:
        for i, v in enumerate(a):
            out[o + i] += v
    return out


def sequencia(*partes) -> list[float]:
    out = []
    for p in partes:
        out.extend(p)
    return out

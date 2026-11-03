import colorsys
import random


def gerar_paleta(seed: str) -> dict:
    """Gera uma paleta harmônica procedural baseada na seed."""
    rng = random.Random(seed)

    h = rng.random()
    s = rng.uniform(0.5, 1.0)
    v = rng.uniform(0.4, 0.9)

    parede = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))

    h_teto = (h + 0.5) % 1.0  # Inverte a cor
    teto = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h_teto, s * 0.5, v * 0.2))

    chao = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s * 0.6, v * 0.1))

    return {"teto": teto, "chao": chao, "base_parede": parede}

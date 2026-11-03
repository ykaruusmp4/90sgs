def apply_envelope(samples: list[float], taxa: int, ataque: float, soltar: float, decai: float) -> list[float]:
    n = len(samples)
    na = max(1, int(ataque * taxa))
    ns = max(1, int(soltar * taxa))
    out = [0.0] * n

    for i in range(n):
        u = i / n
        amp = 1.0 - decai * u
        if i < na:
            amp *= i / na
        resto = n - i
        if resto < ns:
            amp *= resto / ns
        out[i] = samples[i] * amp
    return out

import random


def generate_noise(dur: float, taxa: int) -> list[float]:
    n = max(1, int(dur * taxa))
    return [random.uniform(-1.0, 1.0) for _ in range(n)]

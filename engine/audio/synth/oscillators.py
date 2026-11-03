import math
import random


def square(freq: float, duty: float, fase: float) -> float:
    return 1.0 if fase < duty else -1.0


def triangle(fase: float) -> float:
    return 4.0 * abs(fase - 0.5) - 1.0


def saw(fase: float) -> float:
    return 2.0 * fase - 1.0


def noise() -> float:
    return random.uniform(-1.0, 1.0)

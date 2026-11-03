from .constants import EPS


def clamp(v: float, lo: float, hi: float) -> float:
    return lo if v < lo else hi if v > hi else v


def clamp01(v: float) -> float:
    return 0.0 if v < 0.0 else 1.0 if v > 1.0 else v


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def inv_lerp(a: float, b: float, v: float) -> float:
    if a == b:
        return 0.0
    return (v - a) / (b - a)


def remap(v: float, a0: float, a1: float, b0: float, b1: float) -> float:
    return b0 + (b1 - b0) * inv_lerp(a0, a1, v)


def sign(v: float) -> int:
    return (v > 0) - (v < 0)


def damp(current: float, target: float, decay: float, dt: float, ref_fps: float = 60.0) -> float:
    return target + (current - target) * (decay ** (dt * ref_fps))


def approach(current: float, target: float, max_delta: float) -> float:
    if current < target:
        return min(current + max_delta, target)
    return max(current - max_delta, target)


def approx_zero(v: float, eps: float = EPS) -> bool:
    return -eps < v < eps

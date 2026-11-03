from .constants import PI, TAU


def normalize(a: float) -> float:
    return (a + PI) % TAU - PI


def delta(a: float, b: float) -> float:
    return normalize(a - b)


def lerp_angle(a: float, b: float, t: float) -> float:
    return normalize(a + delta(b, a) * t)


def damp_angle(current: float, target: float, decay: float, dt: float, ref_fps: float = 60.0) -> float:
    d = delta(target, current)
    return normalize(current + d * (1.0 - decay ** (dt * ref_fps)))

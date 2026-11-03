from __future__ import annotations

RGB = tuple[int, int, int]


def clamp255(v: float) -> int:
    return 0 if v < 0 else 255 if v > 255 else int(v)


def scale(rgb: RGB, f: float) -> RGB:
    return (clamp255(rgb[0] * f), clamp255(rgb[1] * f), clamp255(rgb[2] * f))


def scale_int(rgb: RGB, k: int) -> RGB:
    return (rgb[0] // k, rgb[1] // k, rgb[2] // k)


def darken(rgb: RGB, f: float = 0.72) -> RGB:
    return scale(rgb, f)


def lighten(rgb: RGB, f: float = 1.06, bump: int = 6) -> RGB:
    return (clamp255(rgb[0] * f + bump), clamp255(rgb[1] * f + bump), clamp255(rgb[2] * f + bump))


def lerp(a: RGB, b: RGB, t: float) -> RGB:
    return (
        clamp255(a[0] + (b[0] - a[0]) * t),
        clamp255(a[1] + (b[1] - a[1]) * t),
        clamp255(a[2] + (b[2] - a[2]) * t),
    )


def grayscale(v: int) -> RGB:
    v = 0 if v < 0 else 255 if v > 255 else int(v)
    return (v, v, v)

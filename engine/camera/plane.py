"""Camera plane: vetor perpendicular à direção, escalado por tan(fov/2).

O comprimento do plane codifica o FOV: quanto maior, mais aberto.
`Camera.ray_dir` combina `direction + plane * t` (t ∈ [-1, +1]) pra gerar
os raios por coluna, e `Camera.project` usa `cross(plane, direction)` pra
transformar coordenadas de mundo em coordenadas de câmera.
"""

import math

from ..maths.vec2 import Vec2


def make_plane(direction: Vec2, fov: float) -> Vec2:
    half_width = math.tan(fov * 0.5)
    perp = direction.perpendicular()
    return Vec2(perp.x * half_width, perp.y * half_width)


def projection_inverse(plane: Vec2, direction: Vec2) -> float:
    """Denominador usado por `Camera.project` para transformar sprites."""
    det = plane.x * direction.y - direction.x * plane.y
    return 1.0 / det if det != 0.0 else 0.0

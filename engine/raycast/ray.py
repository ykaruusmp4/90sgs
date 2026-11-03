"""Raio em espaço de mundo."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Ray:
    ox: float  # origem x
    oy: float  # origem y
    dx: float  # direção x (não precisa ser unit)
    dy: float  # direção y

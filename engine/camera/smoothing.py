from __future__ import annotations

from ..maths.angles import damp_angle
from ..maths.scalars import approach, damp

__all__ = ["damp", "damp_angle", "approach", "Smoothed"]


class Smoothed:
    __slots__ = ("value", "decay", "ref_fps")

    def __init__(self, value: float = 0.0, decay: float = 0.85, ref_fps: float = 60.0):
        self.value = value
        self.decay = decay
        self.ref_fps = ref_fps

    def to(self, target: float, dt: float) -> float:
        self.value = damp(self.value, target, self.decay, dt, self.ref_fps)
        return self.value

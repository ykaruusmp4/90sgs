"""Resultado de um cast contra o grid."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Hit:
    cell_x: int  # célula da parede atingida
    cell_y: int
    side: int  # 0 = face vertical (step em x), 1 = face horizontal (step em y)
    perp: float  # distância perpendicular ao plano da câmera
    wall_x: float  # 0..1, já flipado — usa direto pra amostrar a textura

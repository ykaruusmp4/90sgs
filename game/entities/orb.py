from engine.physics import Body
from game.config.constants import TAMANHO_BLOCO
from game.entities.entity import Entity


class Orb(Entity):
    __slots__ = ("cor_idx", "coletado", "fase")

    def __init__(self, x: float, y: float, cor_idx: int, fase: float = 0.0):
        # Raio 0.0 porque a coleta é por distância, não por colisão física
        super().__init__(x, y, radius=0.0)
        self.cor_idx = cor_idx
        self.coletado = False
        self.fase = fase

    @property
    def bx(self) -> float:
        return self.x / TAMANHO_BLOCO

    @property
    def by(self) -> float:
        return self.y / TAMANHO_BLOCO

from engine.render import background, wall_texture
from engine.world import find_start_cell, generate, seed_to_int
from game.config.constants import ALTURA_VIRTUAL, LARGURA_VIRTUAL, MARGEM_FUNDO, TAM_TEXTURA, TAMANHO_BLOCO
from game.rules.palette_generator import gerar_paleta


class Level:
    __slots__ = ("numero", "grid", "texture", "background", "start_x", "start_y")

    def __init__(self, world_seed: str, numero: int, size: int = 48):
        self.numero = numero
        hash_nivel = f"{world_seed}#{numero}"
        semente = seed_to_int(hash_nivel)

        paleta = gerar_paleta(hash_nivel)

        self.grid = generate(hash_nivel, size=size)
        self.texture = wall_texture(paleta["base_parede"], semente, size=TAM_TEXTURA)
        self.background = background(
            paleta["teto"],
            paleta["chao"],
            LARGURA_VIRTUAL,
            ALTURA_VIRTUAL + 2 * MARGEM_FUNDO,
        )

        cx, cy = find_start_cell(self.grid)
        self.start_x = cx * TAMANHO_BLOCO + TAMANHO_BLOCO / 2
        self.start_y = cy * TAMANHO_BLOCO + TAMANHO_BLOCO / 2

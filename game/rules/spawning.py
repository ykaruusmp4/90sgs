import math
import random

from engine.world import Grid, bfs_distances
from game.config.constants import TAMANHO_BLOCO
from game.entities.monster import Monster
from game.entities.orb import Orb


def spawn_orbs(grid: Grid, start_x: float, start_y: float, seed: str, quantidade: int = 3) -> list[Orb]:
    rng = random.Random(seed + "|orbs")

    cx, cy = int(start_x // TAMANHO_BLOCO), int(start_y // TAMANHO_BLOCO)
    distancias = bfs_distances(grid, (cx, cy))

    # Filtra pra ficar entre 6 e 18 blocos de distância (nem de graça, nem no fim do mundo)
    candidatos = [c for c, d in distancias.items() if 6 <= d <= 18]

    if len(candidatos) < quantidade:
        candidatos = [c for c, d in distancias.items() if d >= 6]

    rng.shuffle(candidatos)

    orbs = []
    meio = TAMANHO_BLOCO / 2
    for i, (ox, oy) in enumerate(candidatos[:quantidade]):
        orbs.append(Orb(ox * TAMANHO_BLOCO + meio, oy * TAMANHO_BLOCO + meio, i, rng.uniform(0, math.tau)))
    return orbs


def spawn_monsters(grid: Grid, start_x: float, start_y: float, seed: str, quantidade: int = 3) -> list[Monster]:
    rng = random.Random(seed + "|monstros")
    cx, cy = int(start_x // TAMANHO_BLOCO), int(start_y // TAMANHO_BLOCO)
    distancias = bfs_distances(grid, (cx, cy))

    candidatos = [c for c, d in distancias.items() if d >= 18]
    rng.shuffle(candidatos)

    monstros = []
    meio = TAMANHO_BLOCO / 2
    for i, (mx, my) in enumerate(candidatos[:quantidade]):
        monstros.append(Monster(mx * TAMANHO_BLOCO + meio, my * TAMANHO_BLOCO + meio, i % 3, rng.uniform(0, math.tau)))
    return monstros

from game.config.constants import TOTAL_NIVEIS


def checar_vitoria(orbs: list) -> bool:
    return all(o.coletado for o in orbs)


def checar_derrota(tempo_restante: float, hp: int) -> str | None:
    if tempo_restante <= 0.0:
        return "TEMPO ESGOTADO"
    if hp <= 0:
        return "GAME OVER"
    return None


def proximo_nivel(nivel_atual: int) -> int | None:
    if nivel_atual >= TOTAL_NIVEIS:
        return None
    return nivel_atual + 1

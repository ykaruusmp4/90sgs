from game.config.constants import TOTAL_NIVEIS


def checar_vitoria(orbs: list) -> bool:
    """True se todos os orbs do nível foram coletados."""
    return all(o.coletado for o in orbs)


def checar_derrota(tempo_restante: float, hp: int) -> str | None:
    """Retorna a mensagem de game over, ou None se o jogo continua."""
    if tempo_restante <= 0.0:
        return "TEMPO ESGOTADO"
    if hp <= 0:
        return "GAME OVER"
    return None


def proximo_nivel(nivel_atual: int) -> int | None:
    """Retorna o próximo nível, ou None se o jogador zerou o jogo."""
    if nivel_atual >= TOTAL_NIVEIS:
        return None
    return nivel_atual + 1

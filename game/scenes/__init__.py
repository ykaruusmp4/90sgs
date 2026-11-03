from engine.core import Scene

from .game_over import GameOverScene
from .howto import HowToScene
from .menu import MenuScene
from .play import PlayScene
from .transition import TransitionScene
from .victory import VictoryScene


def build_scenes(app) -> dict[str, Scene]:
    return {
        "MENU": MenuScene(app),
        "HOWTO": HowToScene(app),
        "JOGO": PlayScene(app),
        "TRANSICAO": TransitionScene(app),
        "FIM": GameOverScene(app),
        "VITORIA": VictoryScene(app),
    }

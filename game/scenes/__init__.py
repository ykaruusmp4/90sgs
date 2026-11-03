from engine.core import Scene

from .font_test import FontTestScene
from .game_over import GameOverScene
from .howto import HowToScene
from .menu import MenuScene
from .options import OptionsScene
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
        "OPTIONS": OptionsScene(app),
        "VITORIA": VictoryScene(app),
        "FONT_TEST": FontTestScene(app),
    }

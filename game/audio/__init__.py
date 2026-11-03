from engine.audio import Mixer, criar_som

from .sfx_patches import gerar_sons


def init_audio() -> Mixer:
    mixer = Mixer()
    patches = gerar_sons()
    for nome, amostras in patches.items():
        mixer.registrar(nome, criar_som(amostras))
    return mixer


__all__ = ["init_audio"]

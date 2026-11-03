from array import array

import pygame as pg

from .synth import TAXA


def para_pcm(amostras: list[float], canais: int = 1) -> bytes:
    pico = 32767
    arr = array("h")
    if canais == 1:
        arr.extend(max(-pico, min(pico, int(v * pico))) for v in amostras)
    else:
        for v in amostras:
            x = max(-pico, min(pico, int(v * pico)))
            for _ in range(canais):
                arr.append(x)
    return arr.tobytes()


def criar_som(amostras: list[float], canais: int = 1) -> pg.mixer.Sound:
    return pg.mixer.Sound(buffer=para_pcm(amostras, canais))

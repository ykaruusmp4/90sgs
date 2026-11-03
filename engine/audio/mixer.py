import pygame as pg

from game.config.balance import VOL_MESTRE


class Mixer:
    def __init__(self):
        self.sons: dict[str, pg.mixer.Sound] = {}
        self.mudo = False
        self.canal_amb = None
        self._coracao_t = 0.0

        if not pg.mixer.get_init():
            print("[AUDIO] Mixer indisponível! Sem áudio.")
            return

        pg.mixer.set_num_channels(12)
        pg.mixer.set_reserved(1)
        self.canal_amb = pg.mixer.Channel(0)

    def registrar(self, nome: str, som: pg.mixer.Sound):
        self.sons[nome] = som
        self._aplicar_volume_som(som)

    def _aplicar_volume_som(self, som: pg.mixer.Sound):
        som.set_volume(0.0 if self.mudo else VOL_MESTRE)

    def tocar(self, nome: str, volume: float = 1.0):
        if self.mudo or nome not in self.sons:
            return
        canal = self.sons[nome].play()
        if canal and volume != 1.0:
            canal.set_volume(VOL_MESTRE * volume)

    def tocar_ambiente(self, nome: str):
        if self.canal_amb and nome in self.sons:
            if not self.canal_amb.get_busy():
                self.canal_amb.play(self.sons[nome], loops=-1)

    def parar_ambiente(self):
        if self.canal_amb:
            self.canal_amb.stop()

    def alternar_mudo(self):
        self.mudo = not self.mudo
        for som in self.sons.values():
            self._aplicar_volume_som(som)

    def coracao(self, dt: float, passos: int | None):
        if passos is None or passos >= 16:
            self._coracao_t = 0.0
            return

        k = (16 - max(passos, 3)) / (16 - 3)
        self._coracao_t += dt

        if self._coracao_t >= 1.15 - 0.80 * k:
            self._coracao_t = 0.0
            self.tocar("coracao", 0.35 + 0.65 * k)

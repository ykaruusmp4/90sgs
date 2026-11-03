import pygame as pg

from engine.core import Scene
from engine.render import put_text, put_text_centered, put_text_wave
from game.hud.hud import AMARELO, BRANCO, CINZA, VERDE, VERMELHO


class OptionsScene(Scene):
    __slots__ = ("opcao", "opcoes")

    def __init__(self, app):
        super().__init__(app)
        self.opcao = 0
        self.opcoes = ["DIFFICULTY", "MAP SIZE", "CRT", "MULTI-THREAD (EXP)", "VSYNC", "FPS LIMIT", "BACK"]

    def enter(self) -> None:
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            s = self.app.settings

            if event.key in (pg.K_w, pg.K_UP):
                self.opcao = (self.opcao - 1) % len(self.opcoes)
                if self.app.audio:
                    self.app.audio.tocar("blip")
            elif event.key in (pg.K_s, pg.K_DOWN):
                self.opcao = (self.opcao + 1) % len(self.opcoes)
                if self.app.audio:
                    self.app.audio.tocar("blip")

            elif event.key in (pg.K_a, pg.K_LEFT):
                self._mudar_valor(s, -1)
            elif event.key in (pg.K_d, pg.K_RIGHT):
                self._mudar_valor(s, 1)

            elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                if self.app.audio:
                    self.app.audio.tocar("select")

                if self.opcao == 2:
                    s.crt_on = not s.crt_on
                elif self.opcao == 3:
                    s.multithread = not s.multithread
                elif self.opcao == 4:
                    s.vsync = not s.vsync
                    self.app.apply_video_settings()
                elif self.opcao == 6:
                    self.app.scene_manager.change("MENU")

            elif event.key == pg.K_ESCAPE:
                self.app.scene_manager.change("MENU")

    def _mudar_valor(self, s, direcao):
        if self.app.audio:
            self.app.audio.tocar("blip")

        if self.opcao == 0:
            s.difficulty = max(0, min(2, s.difficulty + direcao))
        elif self.opcao == 1:
            sizes = [32, 48, 64]
            idx = sizes.index(s.map_size)
            s.map_size = sizes[max(0, min(2, idx + direcao))]
        elif self.opcao == 5:
            s.fps_limit_idx = max(0, min(4, s.fps_limit_idx + direcao))
            self.app.apply_video_settings()

    def draw(self, surface: pg.Surface) -> None:
        t = pg.time.get_ticks() / 1000.0
        surface.fill((10, 10, 12))
        hud = self.app.hud
        s = self.app.settings

        put_text_wave(surface, hud.font, "OPTIONS", 15, t, color_idx=VERMELHO, escala=2)

        crt_txt = "[ Ô ]" if s.crt_on else "[   ]"
        mt_txt = "[ Ô ]" if s.multithread else "[   ]"
        vsync_txt = "[ Ô ]" if s.vsync else "[   ]"

        vals = [s.difficulty_name, s.map_size_name, crt_txt, mt_txt, vsync_txt, s.fps_limit_name, ""]

        y = 50
        for i, (nome, val) in enumerate(zip(self.opcoes, vals)):
            ativo = i == self.opcao
            cor = BRANCO if ativo else CINZA

            x_nome = 20
            if ativo:
                put_text(surface, hud.font, ">", x_nome - 10, y, color_idx=AMARELO)
            put_text(surface, hud.font, nome, x_nome, y, color_idx=cor)

            if val:
                x_val = surface.get_width() - len(val) * 7 - 20

                if i in (0, 1, 5) and ativo:
                    pode_esq = False
                    pode_dir = False

                    if i == 0:
                        pode_esq = s.difficulty > 0
                        pode_dir = s.difficulty < 2
                    elif i == 1:
                        sizes = [32, 48, 64]
                        idx_size = sizes.index(s.map_size)
                        pode_esq = idx_size > 0
                        pode_dir = idx_size < 2
                    elif i == 5:
                        pode_esq = s.fps_limit_idx > 0
                        pode_dir = s.fps_limit_idx < 4

                    if pode_esq:
                        put_text(surface, hud.font, "<", x_val - 12, y, color_idx=AMARELO)
                    if pode_dir:
                        put_text(surface, hud.font, ">", x_val + len(val) * 7 + 4, y, color_idx=AMARELO)

                put_text(surface, hud.font, val, x_val, y, color_idx=VERDE if ativo else CINZA)

            y += 14

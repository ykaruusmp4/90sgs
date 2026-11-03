from engine.core import App
from game.audio import init_audio
from game.config import constants as C
from game.hud.hud import HUD
from game.scenes import build_scenes


def main():
    app = App(
        title="90 SECONDS",
        virtual_width=C.LARGURA_VIRTUAL,
        virtual_height=C.ALTURA_VIRTUAL,
        window_scale=C.ESCALE,
        shader_vertex=str(C.SHADER_VS),
        shader_fragment=str(C.SHADER_POST),
        target_fps=0,
    )

    app.hud = HUD()
    app.audio = init_audio()

    for name, scene in build_scenes(app).items():
        app.scene_manager.register(name, scene)

    app.scene_manager.change("MENU")
    app.run()


if __name__ == "__main__":
    main()

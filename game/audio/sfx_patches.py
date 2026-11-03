from engine.audio.synth import misturar, sequencia, tom


def gerar_sons() -> dict:
    sons = {}

    sons["blip"] = tom(660, 660, 0.05, "square", vol=0.3, soltar=0.02)
    sons["select"] = sequencia(tom(659.25, 659.25, 0.06, "square", vol=0.3), tom(880.0, 880.0, 0.14, "square", vol=0.3))

    sons["orb0"] = sequencia(
        tom(523.25, 523.25, 0.07, "square", duty=0.25, vol=0.28),
        tom(659.25, 659.25, 0.07, "square", duty=0.25, vol=0.28),
        tom(783.99, 783.99, 0.22, "square", duty=0.25, vol=0.28),
    )
    sons["orb1"] = sequencia(
        tom(659.25, 659.25, 0.07, "square", duty=0.25, vol=0.28),
        tom(783.99, 783.99, 0.07, "square", duty=0.25, vol=0.28),
        tom(987.77, 987.77, 0.22, "square", duty=0.25, vol=0.28),
    )
    sons["orb2"] = sequencia(
        tom(783.99, 783.99, 0.07, "square", duty=0.25, vol=0.28),
        tom(987.77, 987.77, 0.07, "square", duty=0.25, vol=0.28),
        tom(1174.66, 1174.66, 0.22, "square", duty=0.25, vol=0.28),
    )

    sons["dano"] = misturar(
        tom(900, 80, 0.28, "noise", vol=0.55, decai=0.5, curva=0.6), tom(260, 50, 0.32, "square", vol=0.45, curva=0.5)
    )

    sons["gameover"] = misturar(
        tom(440, 55, 1.1, "square", vol=0.38, curva=0.7, vib=0.02, soltar=0.3),
        tom(300, 40, 1.1, "noise", vol=0.22, decai=0.8),
    )

    melodia = [("C5", 0.10), ("E5", 0.10), ("G5", 0.10), ("C6", 0.18), ("G5", 0.10), ("C6", 0.14), ("E6", 0.50)]
    freq = {"C5": 523.25, "E5": 659.25, "G5": 783.99, "C6": 1046.50, "E6": 1318.51}
    camadas = []
    t = 0.0
    for nota, d in melodia:
        camadas.append((tom(freq[nota], freq[nota], d, "square", duty=0.25, vol=0.3, soltar=d * 0.4, decai=0.3), t))
        t += d
    sons["vitoria"] = misturar(*camadas)

    sons["passo0"] = tom(500, 200, 0.05, "noise", vol=0.35, decai=0.9, soltar=0.02)
    sons["passo1"] = tom(430, 170, 0.05, "noise", vol=0.35, decai=0.9, soltar=0.02)

    sons["coracao"] = misturar(
        tom(75, 40, 0.11, "triangle", vol=0.9, soltar=0.05, curva=0.5),
        tom(400, 100, 0.04, "noise", vol=0.25, decai=0.9),
        (tom(65, 35, 0.13, "triangle", vol=0.7, soltar=0.06, curva=0.5), 0.17),
        (tom(350, 90, 0.04, "noise", vol=0.18, decai=0.9), 0.17),
    )

    sons["despertar"] = misturar(
        tom(110, 40, 0.7, "saw", vol=0.45, curva=0.6, vib=0.03, vib_hz=9.0, soltar=0.2),
        tom(120, 30, 0.7, "noise", vol=0.22, soltar=0.2),
    )

    sons["ambiente"] = misturar(
        tom(55.0, 55.0, 1.0, "triangle", vol=0.22, ataque=0.0, soltar=0.0),
        tom(56.0, 56.0, 1.0, "triangle", vol=0.22, ataque=0.0, soltar=0.0),
        tom(110.0, 110.0, 1.0, "square", duty=0.2, vol=0.04, ataque=0.0, soltar=0.0),
    )

    return sons

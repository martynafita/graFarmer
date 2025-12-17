# gra superFarmer - projekt
# autor: Martyna Fita
# przedmiot: Programowanie w językach funkcyjnych

import random
import pygame


class Game:
    wymiany = [[6, "krolik", 1, "owca"], [2, "owca", 1, "swinia"], [3, "swinia", 1, "krowa"], [2, "krowa", 1, "kon"],
               [1, "owca", 1, "maly_pies"], [1, "krowa", 1, "duzy_pies"]]
    zwierzeta_hodowlane = ["krolik", "owca", "swinia", "krowa", "kon"]
    liczba_graczy = 4
    kolejka = [i for i in range(liczba_graczy)]
    # kontynuuj = 1
    wybor = 1
    wygrana = 0
    gracz = kolejka[0]


class GUI:
    okno = pygame.display.set_mode((950, 600))
    Start = pygame.Rect(400, 480, 150, 70)


def rzut_koscmi(dice1: list, dice2: list) -> tuple:
    return random.choice(dice1), random.choice(dice2)


def rzut_gracza(id: int, stan_gry: dict) -> dict:
    niebieska = ["krolik"] * 6 + ["owca"] * 3 + ["swinia"] + ["krowa", "wilk"]
    pomaranczowa = ["krolik"] * 6 + ["owca"] * 2 + ["swinia"] * 2 + ["kon", "lis"]

    wynik = rzut_koscmi(pomaranczowa, niebieska)
    gracz = stan_gry["gracze"][id]

    print(id, wynik)

    gracz = {
        zwierze:
            gracz[zwierze]
            + ((gracz[zwierze] + wynik.count(zwierze)) // 2)
            if zwierze in Game.zwierzeta_hodowlane and wynik.count(zwierze) > 0
            else gracz[zwierze]
        for zwierze in gracz
    }

    gracz = {
        zwierze:
        0 if zwierze == "krolik" and "lis" in wynik and gracz["maly_pies"] == 0
        else 0 if zwierze in ["owca", "swinia", "krowa"] and "wilk" in wynik and gracz["duzy_pies"] == 0
        else gracz[zwierze]
        for zwierze in gracz
    }

    nowy_stan_gry = stan_gry.copy()
    nowy_stan_gry["gracze"][id] = gracz

    return nowy_stan_gry


def wykonaj_ture(stan_gry: dict, kolejka: list) -> tuple:
    gracz_id = kolejka[0]
    nowy_stan = rzut_gracza(gracz_id, stan_gry)
    nowa_kolejka = kolejka[1:] + [gracz_id]
    return nowy_stan, nowa_kolejka


def wymiana(stan_gry: dict, kolejka: list, wybor: int) -> tuple:
    gracz_id = kolejka[0]
    nowy_stan_gry = stan_gry.copy()
    nowa_kolejka = kolejka[1:] + [gracz_id]

    if nowy_stan_gry["gracze"][gracz_id][Game.wymiany[wybor-1][1]] >= Game.wymiany[wybor-1][0]:
        nowy_stan_gry["gracze"][gracz_id][Game.wymiany[wybor-1][3]] += Game.wymiany[wybor-1][2]
        nowy_stan_gry["gracze"][gracz_id][Game.wymiany[wybor-1][1]] -= Game.wymiany[wybor-1][0]
    else:
        print('Nie można dokonać wymiany. Pomijasz kolejkę!')

    return nowy_stan_gry, nowa_kolejka


def stworz_gracza(id: int) -> dict:
    return {
    "id": id,
    "krolik": 1,
    "owca": 0,
    "swinia": 0,
    "krowa": 0,
    "kon": 0,
    "maly_pies": 0,
    "duzy_pies": 0
    }


def obsluga_tury(stan_gry: dict, kolejka: list) -> tuple:
    gracz = kolejka[0]
    print(gracz, "Gracz - Twój stan: ", stan_gry['gracze'][gracz])
    wybor = int(input("1 - rzut kostką, 2- wymiana"))
    if wybor == 1:
        nowy_stan_gry, nowa_kolejka = wykonaj_ture(stan_gry, kolejka)

    elif wybor == 2:
        wymianaWybor = int(input("Ktora wymiana?"))
        nowy_stan_gry, nowa_kolejka = wymiana(stan_gry, kolejka, wymianaWybor)
    else:
        print("Niepoprawny wybór")
        return stan_gry, kolejka

    print("Stan po zagraniu: ", nowy_stan_gry['gracze'][gracz], "\n\n")
    return nowy_stan_gry, nowa_kolejka


def czy_wygral(gracz) -> bool:
    return all(gracz[zwierze] >= 1 for zwierze in Game.zwierzeta_hodowlane)

# while kontynuuj == 1 and wygrana == 0:
#     stan_gry, kolejka = obsluga_tury(stan_gry, kolejka)
#     id_gracza = kolejka[-1]
#     wygrana = czy_wygral(stan_gry["gracze"][id_gracza])
#     if wygrana == 1:
#         print(f"Gracz {id_gracza} wygrał!!!")
#         kontunuuj = 0


def narysuj_text(text: str, kolor: tuple, x: int, y: int) -> None:
    font = pygame.font.SysFont(None, 32)
    surface_tekstu = font.render(text, True, kolor)
    GUI.okno.blit(surface_tekstu, (x, y))


def narysuj_obraz(plik: str, x: int, y: int) -> None:
    obraz = pygame.image.load(plik)
    GUI.okno.blit(obraz, (x, y))


def inicjalizacja_GUI_0() -> None:
    czarny = (0,0,0)
    GUI.okno.fill((45, 156, 80))

    # górne menu
    for i in range(100, 800, 200):
        pygame.draw.rect(GUI.okno, (255, 255, 255), [i, 20, 150, 70])
    narysuj_text("Ustawienia", czarny, 115, 45)
    narysuj_text("Gracze", czarny, 330, 45)
    narysuj_text("Jak grać", czarny, 530, 45)
    narysuj_text("Informacje", czarny, 720, 45)

    # logo na śrdoku
    logo = "logo.jpg"
    narysuj_obraz(logo, 362, 187)

    # start
    pygame.draw.rect(GUI.okno, (255, 255, 255), GUI.Start)
    narysuj_text("Start", czarny, 445, 505)

    pygame.display.update()


def stworzGraczy(liczba_graczy: int) -> list:
    gracze = [stworz_gracza(i) for i in range(liczba_graczy)]
    return gracze


def GameState(liczba_graczy: int) -> dict:
    stan_gry = {
        "gracze": stworzGraczy(liczba_graczy),
        "tura": 0
    }
    return stan_gry


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Gra Farmer")
    gra = True
    stan_GUI = 0

    while gra:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gra = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pozycja = event.pos
                if GUI.Start.collidepoint(pozycja):
                    stan_GUI = 1

        if stan_GUI == 0:
            inicjalizacja_GUI_0()
        if stan_GUI == 1:
            GUI.okno.fill((255, 255, 255))
            pygame.display.update()


if __name__ == "__main__":
    main()

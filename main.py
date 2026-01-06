# superFarmer game - project
# author: Martyna Fita
# subject: Programming in functional languages

import random
import pygame
from pygame import SurfaceType


class Game:
    exchanges = [[6, "rabbit", 1, "sheep"], [2, "sheep", 1, "pig"], [3, "pig", 1, "cow"], [2, "cow", 1, "horse"],
               [1, "sheep", 1, "small_dog"], [1, "cow", 1, "big_dog"]]
    files = {
        "rabbit": "rabbit.jpg",
        "sheep": "sheep.jpg",
        "pig": "pig.jpg",
        "cow": "cow.jpg",
        "horse": "horse.jpg",
        "fox": "fox.png",
        "wolf": "wolf.png",
        "small_dog": "small_dog.png",
        "big_dog": "big_dog.png"
    }
    limits = {
        "rabbit": 60,
        "sheep": 24,
        "pig": 20,
        "cow": 12,
        "horse": 6,
        "small_dog": 1,
        "big_dog": 2
    }
    farm_animals = ["rabbit", "sheep", "pig", "cow", "horse"]
    initial_values = {
        "rabbit": 1,
        "sheep": 0,
        "pig": 0,
        "cow": 0,
        "horse": 0
    }
    number_of_players = 2
    queue = []
    choice = 1
    victory = 0
    result = ()
    move_made = 0
    Names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    roll_made = False
    exchange_made = False
    Exchange = 0


class GUI:
    window = pygame.display.set_mode((950, 600))
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (45, 156, 80)
    # start screen
    Start = pygame.Rect(400, 480, 150, 70)
    Settings = pygame.Rect(100, 20, 150, 70)
    Players = pygame.Rect(300, 20, 150, 70)
    How_To_Play = pygame.Rect(500, 20, 150, 70)
    Information = pygame.Rect(700, 20, 150, 70)
    # main screen
    Name = pygame.Rect(400, 20, 150, 50)
    Roll_Dice = pygame.Rect(200, 500, 150, 50)
    Exchange = pygame.Rect(400, 500, 150, 50)
    End = pygame.Rect(600, 500, 150, 50)
    # exchanges
    exchange_buttons = []
    exchange_rectangles = [
        pygame.Rect(100, 300, 200, 70),
        pygame.Rect(100, 400, 200, 70),
        pygame.Rect(375, 300, 200, 70),
        pygame.Rect(375, 400, 200, 70),
        pygame.Rect(650, 300, 200, 70),
        pygame.Rect(650, 400, 200, 70),
    ]
    # settings window
    Number_Of_Players = pygame.Rect(50, 20, 200, 70)
    Starting_Values = pygame.Rect(50, 110, 250, 70)
    buttons = []
    Back = pygame.Rect(780, 510, 150, 70)
    # names
    name_fields = []
    field_text = ["Player 1", "Player 2", "Player 3", "Player 4"]
    active_field = None
    # end screen
    BackToMenu = pygame.Rect(300, 400, 150, 70)
    Exit = pygame.Rect(500, 400, 150, 70)

class Button:
    def __init__(self, rectangle, action, label):
        self.rectangle = rectangle
        self.action = action
        self.label = label
        self.clicked = False

    def draw(self, window):
        pygame.draw.rect(window, GUI.white, self.rectangle)
        pygame.draw.rect(window, GUI.white, self.rectangle)
        draw_text(
            self.label,
            GUI.black,
            self.rectangle.x + 13,
            self.rectangle.y + 8
        )

    def handle_click(self, position):
        if self.rectangle.collidepoint(position) and not self.clicked:
            self.clicked = True
            self.action()

    def reset_click(self):
        self.clicked = False


def create_player(id: int) -> dict:
    return {
    "id": id,
    "rabbit": Game.initial_values["rabbit"],
    "sheep": Game.initial_values["sheep"],
    "pig": Game.initial_values["pig"],
    "cow": Game.initial_values["cow"],
    "horse": Game.initial_values["horse"],
    "small_dog": 0,
    "big_dog": 0
    }


def roll_dice(dice1: list, dice2: list) -> tuple:
    return random.choice(dice1), random.choice(dice2)


def apply_limits(player: dict) -> None:
    for animal, limit in Game.limits.items():
        if player[animal] > limit:
            player[animal] = limit


def player_roll(id: int, game_state: dict) -> dict:
    blue = ["rabbit"] * 6 + ["sheep"] * 3 + ["pig"] + ["cow", "wolf"]
    orange = ["rabbit"] * 6 + ["sheep"] * 2 + ["pig"] * 2 + ["horse", "fox"]

    result = roll_dice(orange, blue)
    Game.result = result
    player = game_state["players"][id]

    player = {
        animal:
            player[animal]
            + ((player[animal] + result.count(animal)) // 2)
            if animal in Game.farm_animals and result.count(animal) > 0
            else player[animal]
        for animal in player
    }

    if "fox" in result:
        if player["small_dog"] >= 1:
            player["small_dog"] = 0
        else:
            player["rabbit"] = 1

    if "wolf" in result:
        if player["big_dog"] >= 1:
            player["big_dog"] = 0
        else:
            player["sheep"] = 0
            player["pig"] = 0
            player["cow"] = 0

    apply_limits(player)

    new_game_state = game_state.copy()
    new_game_state["players"][id] = player

    return new_game_state


def create_players(number_of_players: int) -> list:
    players = [create_player(i) for i in range(number_of_players)]
    return players


def GameState(number_of_players: int) -> dict:
    game_state = {
        "players": create_players(number_of_players),
    }
    return game_state


def execute_turn(game_state: dict) -> dict:
    player_id = Game.queue[0]
    new_state = player_roll(player_id, game_state)
    Game.move_made = 1
    return new_state


def decrease(file: str) -> None:
    if Game.initial_values[file] > 0:
        Game.initial_values[file] -= 1


def increase(file: str) -> None:
    if Game.initial_values[file] < 15:
        Game.initial_values[file] += 1


def decrease_number_of_players() -> None:
    if Game.number_of_players > 2:
        Game.number_of_players -= 1


def increase_number_of_players() -> None:
    if Game.number_of_players < 4:
        Game.number_of_players += 1


def exchange(game_state: dict, choice: int) -> dict:
    player_id = Game.queue[0]
    new_game_state = game_state.copy()

    if new_game_state["players"][player_id][Game.exchanges[choice-1][1]] >= Game.exchanges[choice-1][0]:
        new_game_state["players"][player_id][Game.exchanges[choice-1][3]] += Game.exchanges[choice-1][2]
        new_game_state["players"][player_id][Game.exchanges[choice-1][1]] -= Game.exchanges[choice-1][0]
    apply_limits(new_game_state["players"][player_id])
    return new_game_state


def execute_exchange(game_state: dict, nr: int) -> None:
    new_state = exchange(game_state, nr)
    game_state.update(new_state)
    Game.Exchange = 0
    Game.exchange_made = True


def initialize_exchange_buttons(game_state: dict) -> None:
    GUI.exchange_buttons.clear()

    for i, rectangle in enumerate(GUI.exchange_rectangles):
        GUI.exchange_buttons.append(
            Button(
                rectangle,
                lambda n=i+1: execute_exchange(game_state, n),
                ""
            )
        )


def end_turn(game_state: dict) -> bool:
    Game.result = ()
    Game.Exchange = 0
    queue = Game.queue
    victory = check_victory(game_state['players'][queue[0]])
    new_queue = queue[1:] + [queue[0]]
    Game.queue = new_queue
    Game.move_made = 0
    Game.roll_made = False
    Game.exchange_made = False
    return victory


def check_victory(player) -> bool:
    return all(player[animal] >= 1 for animal in Game.farm_animals)


def draw_text(text: str, color: tuple, x: int, y: int) -> SurfaceType:
    font = pygame.font.SysFont(None, 32)
    text_surface = font.render(text, True, color)
    GUI.window.blit(text_surface, (x, y))
    return text_surface


def draw_image(file: str, x: int, y: int) -> None:
    image = pygame.image.load(file)
    GUI.window.blit(image, (x, y))


def draw_small_image(file: str, x: int, y: int, width: int, height: int) -> None:
    image = pygame.image.load(file)
    image = pygame.transform.scale(image, (width, height))
    GUI.window.blit(image, (x, y))


def draw_multiline_text(text: str, color: tuple, x: int, y: int, max_width: int,
                                 font = None, line_spacing = 5) -> None:
    if font is None:
        font = pygame.font.SysFont(None, 28)
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    words = text.split(' ')
    line = ""
    y_offset = 0

    for word in words:
        test_line = line + word + " "
        width, height = font.size(test_line)
        if width > max_width:
            # draw current line
            text_surface = font.render(line, True, color)
            GUI.window.blit(text_surface, (x, y + y_offset))
            y_offset += height + line_spacing
            line = word + " "
        else:
            line = test_line

    # draw last line
    if line:
        text_surface = font.render(line, True, color)
        GUI.window.blit(text_surface, (x, y + y_offset))


def draw_button(rectangle: pygame.rect.Rect, text: str, active: bool) -> None:
    border_color = (39, 242, 80) if active else (80,80,80)
    pygame.draw.rect(GUI.window, GUI.white, rectangle)
    pygame.draw.rect(GUI.window, border_color, rectangle, 5)
    draw_text(text, GUI.black, rectangle.x + 10, rectangle.y + 10)


def draw_exchange(exchange: int, rectangle: pygame.rect.Rect):
    amount1, what1, amount2, what2 = Game.exchanges[exchange]

    x = rectangle.x
    y = rectangle.y

    draw_text(str(amount1), GUI.black, x + 10, y + 25)
    draw_small_image(Game.files[what1], x + 30, y + 10, 50, 50)
    draw_text("=> " + str(amount2), GUI.black, x + 85, y + 25)
    draw_small_image(Game.files[what2], x + 135, y + 10, 50, 50)


def initialize_GUI_0() -> None:
    GUI.window.fill(GUI.green)

    # top menu
    pygame.draw.rect(GUI.window, GUI.white, GUI.Settings)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Players)
    pygame.draw.rect(GUI.window, GUI.white, GUI.How_To_Play)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Information)

    draw_text("Ustawienia", GUI.black, 115, 45)
    draw_text("Gracze", GUI.black, 330, 45)
    draw_text("Jak grać", GUI.black, 530, 45)
    draw_text("Informacje", GUI.black, 720, 45)

    # logo in the middle
    logo = "logo.jpg"
    draw_image(logo, 362, 187)

    # start
    pygame.draw.rect(GUI.window, GUI.white, GUI.Start)
    draw_text("Start", GUI.black, 445, 505)

    pygame.display.update()


def initialize_GUI_1() -> None:
    GUI.window.fill(GUI.green)
    GUI.buttons.clear()
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Number_Of_Players)
    draw_text("Liczba graczy: " + str(Game.number_of_players), GUI.black, 60, 45)
    GUI.buttons.append(Button(
        pygame.Rect(270, 35, 40, 40),
        lambda: decrease_number_of_players(),
        "-"
    ))
    GUI.buttons.append(Button(
        pygame.Rect(330, 35, 40, 40),
        lambda: increase_number_of_players(),
        "+"
    ))
    pygame.draw.rect(GUI.window, GUI.white, GUI.Starting_Values)
    draw_text("Wartości początkowe", GUI.black, 60, 135)
    y = 200
    for file in Game.files:
        if y <= 520:
            pygame.draw.rect(GUI.window, GUI.white, pygame.Rect(120, y, 50, 50))
            draw_small_image(Game.files[file], 50, y, 50, 50)
            draw_text(str(Game.initial_values[file]), GUI.black, 140, y+15)

            GUI.buttons.append(
                Button(
                    pygame.Rect(200, y+5, 40, 40),
                    lambda p=file: decrease(p),
                    "-"
                )
            )

            GUI.buttons.append(
                Button(
                    pygame.Rect(260, y+5, 40, 40),
                    lambda p=file: increase(p),
                    "+"
                )
            )
            y += 70
        else:
            break

    for p in GUI.buttons:
        p.draw(GUI.window)

    pygame.display.update()


def initialize_GUI_2() -> None:
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    y = 50
    for i in range(Game.number_of_players):
        Rect = pygame.Rect(40, y, 50, 50)
        pygame.draw.rect(GUI.window, GUI.white, Rect)
        draw_text(str(i+1), GUI.black, Rect.x + 20, Rect.y + 15)
        y += 70

    if not GUI.name_fields or len(GUI.name_fields) != Game.number_of_players:
        GUI.name_fields = [pygame.Rect(100, 50 + i * 70, 200, 50) for i in range(Game.number_of_players)]
        GUI.field_text = [""] * Game.number_of_players

    for i, field in enumerate(GUI.name_fields):
        pygame.draw.rect(GUI.window, GUI.white, field)
        text_surface = draw_text(GUI.field_text[i], GUI.black, field.x + 5, field.y + 10)
        field.w = max(150, text_surface.get_width() + 10)
        if GUI.active_field == i:
            pygame.draw.rect(GUI.window, GUI.black, field, 2)
    pygame.display.update()


def initialize_GUI_3() -> None:
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    text = """Jesteś hodowcą zwierząt i chcesz zostać superfarmerem. Twoje zwierzęta rozmnażają się, 
a to przynosi ci zysk. Możesz zamieniać wyhodowane zwierzęta na inne, jeśli uznasz, 
że to się opłaca. Aby zwyciężyć, musisz jako pierwszy uzyskać stado złożone co najmniej 
z konia, krowy, świni, owcy i królika. Jednak wszystkie Twoje plany mogą pozostać tylko 
w sferze marzeń, jeśli nie zachowasz należytej ostrożności! W okolicy grasują bowiem 
wilk i lis, których łatwym łupem mogą stać się Twoje zwierzęta. 
W grze może brać udział od 2 do 4 osób. Każdy gracz na początek otrzymuje jednego królika. 
Gracze rzucają kolejno, zawsze dwiema kostkami. Jeśli gracz rzuci kostkami tak, że na 
obu wypadnie takie samo zwierzę, to dostaje to zwierzę ze stada głównego. Gdy gracz ma 
już jakieś zwierzęta, to po rzucie otrzymuje ze stada tyle zwierząt wyrzuconego 
gatunku, ile ma pełnych par tego gatunku ( łącznie z wyrzuconymi na kostkach).Przed każdym rzutem kostkami gracz, 
jeśli zechce może dokonać jednej wymiany. 
Wymiany odbywają się zgodnie z przelicznikami przedstawionymi w tabeli wymian."""

    draw_multiline_text(text, GUI.black, 50, 50, 850)
    pygame.display.update()


def initialize_GUI_4() -> None:
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    text = """Superfarmer to gra, która powstała w Warszawie w 1943 roku. Nosiła wtedy tytuł 
„Hodowla zwierzątek". Grę wymyślił wybitny polski matematyk, profesor Uniwersytetu Warszawskiego, 
Karol Borsuk. Po zajęciu Warszawy hitlerowcy zamknęli Uniwersytet, w wyniku tego profesor stracił pracę. 
Sprzedaż gry była pomysłem profesora na ratowanie rodzinnego budżetu. Zestawy do gry wykonywane 
były metodami domowymi przez żonę profesora, panią Zofię Borsukową. 
Umieszczone w grze rysunki zwierzątek namalowała Janina Śliwicka. W krótkim czasie 
gra zyskała nadspodziewanie wielką popularność nie tylko wśród przyjaciół, lecz także 
w szerokich kręgach dalszych znajomych i nieznajomych osób. W domu państwa 
Borsuków rozdzwonił się telefon, a głos w słuchawce coraz częściej zadawał pytanie: 
Czy to hodowla zwierzątek? Po potwierdzeniu zwykle następowało zamówienie. 
Gra bawiła nie tylko dzieci, wciągała także i dorosłych pomagając im przetrwać 
ponure okupacyjne wieczory. Gry spłonęły wraz z miastem w czasie powstania warszawskiego, w sierpniu 1944r. 
Szczęśliwie jeden z egzemplarzy zachował się poza Warszawą i wiele lat po wojnie wrócił 
do rodziny Borsuków. - GRANNA, Warszawa, marzec 2013"""

    draw_multiline_text(text, GUI.black, 50, 50, 850)
    pygame.display.update()


def initialize_GUI_5(game_state, queue) -> None:
    name = GUI.field_text[queue[0]]
    y = 110
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Name)
    text_surface = draw_text(str(game_state['players'][queue[0]]['id'] + 1) + " " + name, GUI.black, 420, 35)
    GUI.Name.w = max(150, text_surface.get_width() + 30)
    draw_image("rabbit.jpg", 50, y)
    draw_image("sheep.jpg", 230, y)
    draw_image("pig.jpg", 410, y)
    draw_image("cow.jpg", 590, y)
    draw_image("horse.jpg", 770, y)
    draw_text(str(game_state['players'][queue[0]]["rabbit"]), GUI.black, 100, 250)
    draw_text(str(game_state['players'][queue[0]]["sheep"]), GUI.black, 270, 250)
    draw_text(str(game_state['players'][queue[0]]["pig"]), GUI.black, 460, 250)
    draw_text(str(game_state['players'][queue[0]]["cow"]), GUI.black, 640, 250)
    draw_text(str(game_state['players'][queue[0]]["horse"]), GUI.black, 820, 250)

    draw_button(
        GUI.Roll_Dice,
        "Rzuć kostką",
        not Game.roll_made
    )
    draw_button(
        GUI.Exchange,
        "Wymiany",
        not Game.exchange_made
    )
    draw_button(
        GUI.End,
        "Zakończ turę",
        Game.roll_made
    )

    if len(Game.result) > 0:
        draw_image(Game.files[Game.result[0]], 300, 300)
        draw_image(Game.files[Game.result[-1]], 500, 300)
    if Game.Exchange == 1:
        initialize_exchange_buttons(game_state)

        for i, p in enumerate(GUI.exchange_buttons):
            pygame.draw.rect(GUI.window, GUI.white, p.rectangle)
            draw_exchange(i, p.rectangle)

    if game_state["players"][queue[0]]["small_dog"] >= 1:
        draw_small_image(Game.files["small_dog"], 50, 20, 50, 50)
    if game_state["players"][queue[0]]["big_dog"] >= 1:
        draw_small_image(Game.files["big_dog"], 130, 20, 50, 50)
    pygame.display.update()


def initialize_GUI_6() -> None:
    GUI.window.fill(GUI.green)
    draw_text("Zwycięzcą jest " + Game.Names[Game.queue[-1]], GUI.white, 350, 200)
    pygame.draw.rect(GUI.window, GUI.white, GUI.BackToMenu)
    draw_text("Menu główne", GUI.black, GUI.BackToMenu.x+5, GUI.BackToMenu.y+25)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Exit)
    draw_text("Wyjdź z gry", GUI.black, GUI.Exit.x + 13, GUI.Exit.y + 25)
    pygame.display.update()


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Gra SuperFarmer")
    game = True
    GUI_state = 0
    game_state = None
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if GUI_state == 0 and GUI.Start.collidepoint(position):
                    game_state = GameState(Game.number_of_players)
                    Game.queue = [i for i in range(Game.number_of_players)]
                    GUI_state = 5
                elif GUI_state == 0 and GUI.Settings.collidepoint(position):
                    GUI_state = 1
                elif GUI_state == 0 and GUI.Players.collidepoint(position):
                    GUI_state = 2
                elif GUI_state == 0 and GUI.How_To_Play.collidepoint(position):
                    GUI_state = 3
                elif GUI_state == 0 and GUI.Information.collidepoint(position):
                    GUI_state = 4
                elif GUI_state != 6 and GUI.Back.collidepoint(position):
                    GUI_state = 0
                elif GUI_state == 1:
                    for p in GUI.buttons:
                        p.handle_click(position)
                elif GUI_state == 5 and GUI.Roll_Dice.collidepoint(position) and not Game.roll_made:
                    Game.Exchange = 0
                    Game.exchange_made = True
                    game_state = execute_turn(game_state)
                    Game.roll_made = True
                elif GUI_state == 5 and GUI.Exchange.collidepoint(position) and not Game.exchange_made and Game.move_made == 0:
                    Game.Exchange = 1
                    Game.exchange_made = True
                elif GUI_state == 5 and Game.Exchange == 1:
                    for p in GUI.exchange_buttons:
                        p.handle_click(position)
                elif GUI_state == 5 and GUI.End.collidepoint(position):
                    victory = end_turn(game_state)
                    if victory:
                        GUI_state = 6
                elif GUI_state == 6 and GUI.Exit.collidepoint(position):
                    game = False
                elif GUI_state == 6 and GUI.BackToMenu.collidepoint(position):
                    GUI_state = 0

            if GUI_state == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    GUI.active_field = None
                    for i, field in enumerate(GUI.name_fields):
                        if field.collidepoint(event.pos):
                            GUI.active_field = i
                            break
                elif event.type == pygame.KEYDOWN and GUI.active_field is not None:
                    if event.key == pygame.K_BACKSPACE:
                        GUI.field_text[GUI.active_field] = GUI.field_text[GUI.active_field][:-1]
                    elif event.key == pygame.K_RETURN:
                        Game.Names[GUI.active_field] = GUI.field_text[
                                                            GUI.active_field] or f"Gracz {GUI.active_field + 1}"
                        GUI.active_field = None
                    else:
                        GUI.field_text[GUI.active_field] += event.unicode

        if GUI_state == 0:
            initialize_GUI_0()
        if GUI_state == 1:
            initialize_GUI_1()
        if GUI_state == 2:
            initialize_GUI_2()
        if GUI_state == 3:
            initialize_GUI_3()
        if GUI_state == 4:
            initialize_GUI_4()
        if GUI_state == 5:
            initialize_GUI_5(game_state, Game.queue)
        if GUI_state == 6:
            initialize_GUI_6()


if __name__ == "__main__":
    main()
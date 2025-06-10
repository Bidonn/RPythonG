import pygame
from project.theGame.Classes.Button import Button
import project.theGame.settings as s
from project.theGame.Classes.Class import Class, Warrior, Wizzard
import time

start_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 3 * 2, 200, 50, "Start Game", (255,255,255), (50,255,50))


MENU_BG = pygame.transform.scale(pygame.image.load('imgs/village-bg.png'), (1000, 800))
TITLE_LOGO = pygame.transform.scale(pygame.image.load('imgs/titlelogo.png'), (500, 500))

def ui_menu(WIN: pygame.surface):
    """
        Menu główne z opcjami: New Game, Load Game, Quit
        Zwraca: 'new_game', 'load_game', 'quit' lub None
        """
    from project.theGame.Classes.Button import Button

    # Przyciski menu
    new_game_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 2 +20, 200, 50, "New Game", (255, 255, 255),
                             (200, 200, 200))
    load_game_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 2 + 90, 200, 50, "Load Game", (255, 255, 255),
                              (200, 200, 200))
    quit_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 2 + 160, 200, 50, "Quit", (255, 255, 255), (200, 200, 200))

    WIN.blit(MENU_BG, (0,0))

    # Tytuł

    WIN.blit(TITLE_LOGO, (s.WIDTH // 2 - TITLE_LOGO.get_width()/2, s.HEIGHT // 3.5 - TITLE_LOGO.get_height()/2))
    while True:
        pygame.time.Clock().tick(60)
        # Rysowanie przycisków
        new_game_button.draw(WIN)
        load_game_button.draw(WIN)
        quit_button.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if new_game_button.handle_event(event):
                return "new_game"

            if load_game_button.handle_event(event):
                return "load_game"

            if quit_button.handle_event(event):
                return "quit"
        pygame.display.update()
    return None



def ui_character_select(WIN: pygame.surface):
    warrior_img = pygame.transform.scale(pygame.image.load('imgs/warrior.png'), (120, 240))
    wizzard_img = pygame.transform.scale(pygame.image.load('imgs/wizzard.png'), (120, 240))

    # Utworzenie przycisków
    warrior_button = Button(s.WIDTH // 4 - 100, s.HEIGHT // 2 + 100, 200, 50, "Warrior", (255, 255, 255),
                            (200, 200, 200))
    wizzard_button = Button(s.WIDTH * 3 // 4 - 100, s.HEIGHT // 2 + 100, 200, 50, "Wizzard", (255, 255, 255),
                            (200, 200, 200))

    # Pole tekstowe na nazwę gracza
    input_text = ""
    input_rect = pygame.Rect(s.WIDTH // 2 - 150, s.HEIGHT // 2 + 230, 300, 50)
    input_active = True

    # Zmienna do obsługi komunikatu błędu
    show_error = False
    error_timer = 0

    while True:
        # Wypełnienie tła
        WIN.fill((50, 50, 50))

        # Wyświetlenie tytułu
        title = s.FONT.render("Choose your character", True, (255, 255, 255))
        title_rect = title.get_rect(center=(s.WIDTH // 2, 50))
        WIN.blit(title, title_rect)

        # Wyświetlenie obrazków postaci
        WIN.blit(warrior_img, (s.WIDTH // 4 - 60, s.HEIGHT // 2 - 200))
        WIN.blit(wizzard_img, (s.WIDTH * 3 // 4 - 60, s.HEIGHT // 2 - 200))

        # Rysowanie przycisków
        warrior_button.draw(WIN)
        wizzard_button.draw(WIN)

        # Rysowanie pola tekstowego i etykiety
        name_label = s.FONT.render("Enter player name:", True, (255, 255, 255))
        WIN.blit(name_label, (input_rect.x, input_rect.y - 50))

        # Rysowanie pola tekstowego
        pygame.draw.rect(WIN, (255, 255, 255), input_rect, 2)
        text_surface = s.FONT.render(input_text, True, (255, 255, 255))

        # Ograniczenie długości tekstu
        if text_surface.get_width() > input_rect.width - 20:
            input_text = input_text[:-1]
            text_surface = s.FONT.render(input_text, True, (255, 255, 255))

        WIN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # Rysowanie kursora tekstowego
        if input_active and time.time() % 1 > 0.5:  # migający kursor
            cursor_x = input_rect.x + 5 + text_surface.get_width()
            pygame.draw.line(WIN,
                             (255, 255, 255),
                             (cursor_x, input_rect.y + 5),
                             (cursor_x, input_rect.y + 45),
                             2)

        # Wyświetlanie komunikatu błędu jeśli jest aktywny
        if show_error:
            current_time = time.time()
            if current_time - error_timer < 2.0:  # Wyświetl przez 2 sekundy
                error_text = s.FONT.render("Player name can't be empty!", True, (255, 0, 0))
                WIN.blit(error_text, (s.WIDTH // 2 - error_text.get_width() // 2, input_rect.bottom + 10))
            else:
                show_error = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 20:  # Ograniczenie do 20 znaków
                    if event.unicode.isprintable():  # Tylko drukowalne znaki
                        input_text += event.unicode

            # Obsługa przycisków - tylko jeśli nazwa została wprowadzona
            if input_text.strip():  # Sprawdzamy czy nazwa nie jest pusta
                if warrior_button.handle_event(event):
                    return Warrior(input_text.strip(), 1, 0)

                if wizzard_button.handle_event(event):
                    return Wizzard(input_text.strip(), 1, 0)
            else:
                # Jeśli nazwa jest pusta, pokaż komunikat błędu na 2 sekundy
                if warrior_button.handle_event(event) or wizzard_button.handle_event(event):
                    show_error = True
                    error_timer = time.time()

        pygame.display.update()


def ui_load_game(WIN: pygame.surface):
    """
    Wyświetla interfejs do ładowania zapisanych gier z opcją usuwania.
    Zwraca wybraną postać z zapisaną grą lub None jeśli anulowano.
    """
    from project.theGame.database import Entry, delete_entry
    from project.theGame.Classes.Class import Warrior, Wizzard
    from project.theGame.Classes.Button import Button

    # Pobierz wszystkie zapisy z bazy danych
    def refresh_saves():
        try:
            return list(Entry.select().order_by(Entry.date.desc()))
        except:
            return []

    saves = refresh_saves()

    if not saves:
        # Jeśli brak zapisów, wyświetl komunikat
        return ui_no_saves_screen(WIN)

    # Przygotowanie interfejsu
    scroll_offset = 0
    max_visible_saves = 7
    selected_save = None
    delete_mode = False

    # Przyciski
    load_button = Button(s.WIDTH // 2 - 200, s.HEIGHT - 100, 200, 50, "Load Game", (255, 255, 255), (0, 200, 0))
    delete_button = Button(s.WIDTH // 2 + 5, s.HEIGHT - 100, 200, 50, "Delete Mode", (255, 255, 255), (200, 100, 0))
    back_button = Button(50, s.HEIGHT - 100, 100, 50, "Back", (255, 255, 255), (200, 0, 0))
    confirm_delete_button = Button(s.WIDTH // 2 - 200, s.HEIGHT - 100, 200, 50, "Confirm", (255, 255, 255), (0, 200, 0))
    # Komunikaty
    message = ""
    message_timer = 0
    message_color = (255, 255, 255)

    while True:
        WIN.blit(MENU_BG, (0, 0))

        # Tytuł
        title_text = "Delete Mode: Select save to DELETE" if delete_mode else "Load Game"
        title_color = (255, 100, 100) if delete_mode else (255, 255, 255)
        title = s.FONT.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(s.WIDTH // 2, 50))
        WIN.blit(title, title_rect)

        # Nagłówki tabeli
        headers = ["Player", "Character", "Level", "Score", "Date"]
        header_y = 100
        col_positions = [80, 220, 380, 470, 700]

        for i, header in enumerate(headers):
            header_text = s.FONT.render(header, True, (200, 200, 200))
            WIN.blit(header_text, (col_positions[i], header_y-10))

        # Linia pod nagłówkami
        pygame.draw.line(WIN, (255, 255, 255), (60, header_y + 30), (s.WIDTH - 60, header_y + 30), 2)

        # Wyświetlanie zapisów
        save_rects = []
        start_y = header_y + 50

        visible_saves = saves[scroll_offset:scroll_offset + max_visible_saves]

        for i, save in enumerate(visible_saves):
            y_pos = start_y + i * 40
            save_rect = pygame.Rect(60, y_pos +5, s.WIDTH - 120, 35)
            save_rects.append((save_rect, save))

            # Kolory w zależności od trybu
            if delete_mode:
                hover_color = (150, 50, 50)
                select_color = (200, 100, 100)
            else:
                hover_color = (80, 80, 80)
                select_color = (100, 100, 150)

            # Podświetlenie wybranego zapisu
            if selected_save and selected_save.id == save.id:
                pygame.draw.rect(WIN, select_color, save_rect)
            elif save_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(WIN, hover_color, save_rect)

            # Dane zapisu
            level_text = str(getattr(save, 'level', 1))
            data = [
                save.player_name,
                save.character_class,
                level_text,
                str(save.score),
                save.date.strftime("%Y-%m-%d %H:%M")
            ]

            text_color = (255, 200, 200) if delete_mode else (255, 255, 255)
            for j, text in enumerate(data):
                text_surface = s.FONT.render(text, True, text_color)
                WIN.blit(text_surface, (col_positions[j], y_pos))

        # Scrollbar jeśli potrzebny
        if len(saves) > max_visible_saves:
            scrollbar_height = 280
            scrollbar_y = start_y
            scrollbar_rect = pygame.Rect(s.WIDTH - 20, scrollbar_y, 15, scrollbar_height)
            pygame.draw.rect(WIN, (100, 100, 100), scrollbar_rect)

            # Thumb scrollbara
            if len(saves) > max_visible_saves:
                thumb_height = max(20, scrollbar_height * max_visible_saves // len(saves))
                thumb_y = scrollbar_y + (scrollbar_height - thumb_height) * scroll_offset // max(1,
                                                                                                 len(saves) - max_visible_saves)
                thumb_rect = pygame.Rect(s.WIDTH - 20, thumb_y, 15, thumb_height)
                pygame.draw.rect(WIN, (200, 200, 200), thumb_rect)

        # Przyciski
        if not delete_mode:
            load_button.draw(WIN)
        else:
            confirm_delete_button.draw(WIN)
        delete_button.draw(WIN)
        back_button.draw(WIN)

        # Zmiana tekstu przycisku delete w zależności od trybu
        delete_button.text = "Cancel Delete" if delete_mode else "Delete Mode"
        delete_button.color = (100, 100, 100) if delete_mode else (255, 255, 255)


        # Instrukcje
        if delete_mode and selected_save:
            instruction = s.FONT.render("Click Confirm to confirm deletion", True, (255, 100, 100))
        elif delete_mode:
            instruction = s.FONT.render("Select a save to delete", True, (255, 150, 150))
        elif not selected_save:
            instruction = s.FONT.render("Select a save to load or delete", True, (150, 150, 150))
        else:
            instruction = s.FONT.render("Click Load Game or Delete Save", True, (150, 150, 150))

        instruction_rect = instruction.get_rect(center=(s.WIDTH // 2, s.HEIGHT - 170))
        WIN.blit(instruction, instruction_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    # Sprawdź kliknięcie na zapis
                    for save_rect, save in save_rects:
                        if save_rect.collidepoint(event.pos):
                            selected_save = save
                            break

                    # Sprawdź przyciski
                    if back_button.handle_event(event):
                        return None

                    if delete_button.handle_event(event):
                        if not delete_mode:
                            # Włącz tryb usuwania
                            delete_mode = True
                            selected_save = None
                        else:
                            # Anuluj tryb usuwania
                            delete_mode = False
                            selected_save = None

                    if delete_mode and confirm_delete_button.handle_event(event) and selected_save:
                        # Potwierdź usunięcie
                        if delete_entry(selected_save.id):
                            saves = refresh_saves()
                            delete_mode = False
                            selected_save = None
                            if not saves:
                                return ui_no_saves_screen(WIN)



                    if not delete_mode and load_button.handle_event(event) and selected_save:
                        # Utwórz postać na podstawie zapisu
                        level = getattr(selected_save, 'level', 1)

                        if selected_save.character_class == "Warrior":
                            hero = Warrior(selected_save.player_name, level, selected_save.score)
                        elif selected_save.character_class == "Wizzard":
                            hero = Wizzard(selected_save.player_name, level, selected_save.score)
                        else:
                            continue

                        return hero

                elif event.button == 4:  # Scroll up
                    scroll_offset = max(0, scroll_offset - 1)
                elif event.button == 5:  # Scroll down
                    scroll_offset = min(max(0, len(saves) - max_visible_saves), scroll_offset + 1)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if delete_mode:
                        delete_mode = False
                        selected_save = None
                        message = "Delete mode cancelled"
                        message_color = (150, 150, 150)
                        message_timer = time.time()
                    else:
                        return None
                elif event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - 1)
                elif event.key == pygame.K_DOWN:
                    scroll_offset = min(max(0, len(saves) - max_visible_saves), scroll_offset + 1)
                elif event.key == pygame.K_DELETE and selected_save and not delete_mode:
                    # Skrót Delete na klawiaturze
                    delete_mode = True

        pygame.display.update()


def ui_no_saves_screen(WIN: pygame.surface):
    """
    Wyświetla ekran gdy brak zapisanych gier.
    """
    back_button = Button(s.WIDTH // 2 - 250, s.HEIGHT // 2 + 50, 500, 50, "Create character", (255, 255, 255), (200, 0, 0))

    while True:
        WIN.blit(MENU_BG, (0,0))

        # Komunikat
        title = s.FONT.render("No Saved Games", True, (255, 255, 255))
        title_rect = title.get_rect(center=(s.WIDTH // 2, s.HEIGHT // 2 - 50))
        WIN.blit(title, title_rect)

        message = s.FONT.render("You don't have any saved games yet.", True, (200, 200, 200))
        message_rect = message.get_rect(center=(s.WIDTH // 2, s.HEIGHT // 2))
        WIN.blit(message, message_rect)

        back_button.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if back_button.handle_event(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return ui_character_select(WIN)

        pygame.display.update()


def ui_pause_menu(WIN: pygame.surface, hero, elapsed_time):
    """
    Ekran pauzy z opcjami: Resume, Save Game, Exit to Menu
    Zwraca: 'resume', 'save', 'exit' lub None
    """
    from project.theGame.Classes.Button import Button
    from project.theGame.database import add_entry

    # Przyciski
    resume_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 2 - 80, 200, 50, "Resume", (255, 255, 255), (200, 255, 200))
    save_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 2 - 20, 200, 50, "Save Game", (255, 255, 255), (200, 200, 255))
    exit_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 2 + 40, 200, 50, "Exit", (255, 255, 255),
                         (255, 200, 200))

    # Półprzezroczyste tło
    overlay = pygame.Surface((s.WIDTH, s.HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))

    # Zmienna do komunikatu o zapisie
    save_message = ""
    save_message_timer = 0

    while True:
        # Rysuj overlay
        WIN.blit(overlay, (0, 0))

        # Tytuł
        title = s.FONT.render("GAME PAUSED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(s.WIDTH // 2, s.HEIGHT // 2 - 150))
        WIN.blit(title, title_rect)

        # Statystyki gracza
        player_info = [
            f"Player: {hero.player}",
            f"Character: {hero.name}",
            f"Score: {hero.score}",
            f"Level: {hero.level}",
            f"Time: {round(elapsed_time)}s"
        ]

        for i, info in enumerate(player_info):
            info_text = s.FONT.render(info, True, (200, 200, 200))
            info_rect = info_text.get_rect(center=(s.WIDTH // 2, (s.HEIGHT // 3)*2  + i * 30))
            WIN.blit(info_text, info_rect)

        # Przyciski
        resume_button.draw(WIN)
        save_button.draw(WIN)
        exit_button.draw(WIN)

        # Komunikat o zapisie
        if save_message and time.time() - save_message_timer < 2.0:
            message_color = (0, 255, 0) if "successfully" in save_message else (255, 0, 0)
            message_text = s.FONT.render(save_message, True, message_color)
            message_rect = message_text.get_rect(center=(s.WIDTH // 2, (s.HEIGHT // 4)*3 + 100))
            WIN.blit(message_text, message_rect)

        # Instrukcje
        instruction = s.FONT.render("Press ESC to resume", True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(s.WIDTH // 2, s.HEIGHT - 50))
        WIN.blit(instruction, instruction_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

            if resume_button.handle_event(event):
                return "resume"

            if save_button.handle_event(event):
                try:
                    # Zapisz grę do bazy danych
                    add_entry(hero.player, hero.name, hero.score, hero.level)
                    save_message = "Game saved successfully!"
                    save_message_timer = time.time()
                except Exception as e:
                    print(e)
                    save_message = "Save failed!"
                    save_message_timer = time.time()

            if exit_button.handle_event(event):
                return "exit"

        pygame.display.update()


def ui_game_over(WIN: pygame.surface, hero): #game over screen
    pass

def ui_gameplay_overlay(WIN: pygame.surface, hero): #spelle, zycie, staty
    pass
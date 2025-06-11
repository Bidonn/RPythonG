from operator import truediv

import pygame
import project.theGame.settings as s


class ShopKeeper:
    just_bought = False
    def __init__(self):
        """
        Inicjalizacja sklepikarza
        :param x: pozycja x sklepikarza
        :param y: pozycja y sklepikarza
        """
        self.is_active = False
        self.x = 1000
        self.y = 600
        self.width = 125
        self.height = 125
        self.image = pygame.image.load("imgs/ognisko.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.menu = ShopMenu()

    def draw(self, win, scroll):
        """
        Rysuje sklepikarza na ekranie z uwzględnieniem przewijania
        :param win: okno, na którym rysujemy
        """
        # Pozycja na ekranie uwzględniająca przewijanie
        screen_x = self.x - scroll
        screen_y = self.y
        win.blit(self.image, (screen_x, screen_y))

        self.update(scroll)

        if self.menu.is_visible:
            # Pozycja menu nad ogniskiem
            menu_x = screen_x + (self.width - self.menu.menu_width) // 2
            menu_y = screen_y - self.menu.menu_height - 10  # 10 pikseli odstępu od ogniska
            self.menu.draw(win, menu_x, menu_y)


    def update(self, scroll):
        """
        Aktualizuje pozycję prostokąta kolizji z uwzględnieniem przewijania
        """
        # Aktualizujemy rect do aktualnej pozycji na ekranie
        self.rect.x = self.x - scroll
        self.rect.y = self.y
        self.is_active = True

    def check_collision(self, player_rect):
        """
        Sprawdza kolizję z graczem i zwraca True, jeśli występuje kolizja
        :param player_rect: prostokąt kolizji gracza
        :return: True jeśli jest kolizja, False w przeciwnym przypadku
        """
        if self.is_active:
            collision = self.rect.colliderect(player_rect)
            # Aktualizuj stan menu na podstawie kolizji
            if collision and not self.menu.is_visible:
                self.menu.show()
            elif not collision and self.menu.is_visible:
                self.menu.hide()
            return collision
        return False

    def handle_click(self, mouse_pos, scroll, hero):
        """
        Obsługuje kliknięcie w przyciski menu
        :param mouse_pos: pozycja kliknięcia myszy
        :param scroll: aktualna wartość przewijania
        :return: indeks klikniętego przycisku lub None jeśli nie kliknięto przycisku
        """
        if not self.menu.is_visible:
            return None

        # Pozycja menu na ekranie
        menu_x = self.x - scroll + (self.width - self.menu.menu_width) // 2
        menu_y = self.y - self.menu.menu_height - 10

        return self.menu.handle_click(mouse_pos, menu_x, menu_y, hero)



class Item:
    def __init__(self, name, price, image_path, description=""):
        """
        Inicjalizacja przedmiotu
        :param name: nazwa przedmiotu
        :param price: cena przedmiotu
        :param image_path: ścieżka do obrazka przedmiotu
        :param description: opis przedmiotu (opcjonalny)
        """
        self.name = name
        self.price = price
        self.description = description
        self.image = pygame.image.load(image_path)
        self.width = 50  # domyślny rozmiar
        self.height = 50
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, win, x, y):
        """
        Rysuje przedmiot na ekranie
        :param win: okno, na którym rysujemy
        :param x: pozycja x przedmiotu
        :param y: pozycja y przedmiotu
        """
        win.blit(self.image, (x, y))



class ShopMenu:
    def __init__(self):
        """
        Inicjalizacja menu sklepu z przyciskami
        """
        # Ustawienia menu
        self.button_size = 60  # Rozmiar kwadratowego przycisku
        self.button_margin = 20  # Odstęp między przyciskami
        self.menu_width = 3 * self.button_size + 4 * self.button_margin  # Szerokość menu
        self.menu_height = self.button_size + 2 * self.button_margin  # Wysokość menu

        # Stan menu
        self.is_visible = False
        self.menu_surface = None
        self.buttons = []

        # Inicjalizacja powierzchni menu i przycisków
        self._init_menu()

    def _init_menu(self):
        """
        Inicjalizuje powierzchnię menu i przyciski
        """
        # Przygotowanie przezroczystej powierzchni dla menu
        self.menu_surface = pygame.Surface((self.menu_width, self.menu_height), pygame.SRCALPHA)

        # Dodanie półprzezroczystego tła
        pygame.draw.rect(self.menu_surface, (0, 0, 0, 128), (0, 0, self.menu_width, self.menu_height), border_radius=10)

        # Tworzenie przycisków (prostokąty i pozycje)
        for i in range(3):
            x = self.button_margin + i * (self.button_size + self.button_margin)
            y = self.button_margin
            button_rect = pygame.Rect(x, y, self.button_size, self.button_size)
            # Kolor przycisku - różne kolory dla różnych przycisków
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Czerwony, zielony, niebieski
            self.buttons.append((button_rect, colors[i]))

    def show(self):
        """
        Pokazuje menu
        """
        self.is_visible = True

    def hide(self):
        """
        Ukrywa menu
        """
        self.is_visible = False

    def draw(self, win, x, y):
        """
        Rysuje menu na ekranie
        :param win: okno, na którym rysujemy
        :param x: pozycja x menu
        :param y: pozycja y menu
        """
        if not self.is_visible:
            return

        # Rysowanie tła menu
        win.blit(self.menu_surface, (x, y))

        # Rysowanie przycisków
        for button, color in self.buttons:
            button_x = x + button.x
            button_y = y + button.y
            pygame.draw.rect(win, color, (button_x, button_y, button.width, button.height), border_radius=5)

            # Dodanie obramowania do przycisków
            pygame.draw.rect(win, (255, 255, 255), (button_x, button_y, button.width, button.height), 2,
                             border_radius=5)

    def handle_click(self, mouse_pos, menu_x, menu_y, hero):
        """
        Obsługuje kliknięcie w przyciski menu
        :param mouse_pos: pozycja kliknięcia myszy
        :param menu_x: pozycja x menu na ekranie
        :param menu_y: pozycja y menu na ekranie
        :param hero: nie popłacz sie
        :return: indeks klikniętego przycisku lub None jeśli nie kliknięto przycisku
        """
        if not self.is_visible:
            return None
        # Sprawdzenie, czy kliknięcie było w obszarze menu
        for i, (button, _) in enumerate(self.buttons):
            button_x = menu_x + button.x
            button_y = menu_y + button.y
            button_rect = pygame.Rect(button_x, button_y, button.width, button.height)

            if button_rect.collidepoint(mouse_pos):
                print(f"Kliknięto przycisk {i + 1}")
                outer_i = i+1
                hero.level+=1
                if i == 0:
                    hero.max_hp += 10
                if i == 1:
                    hero.DMG += 2.5
                if i == 2:
                    hero.ms += 1
                ShopKeeper.just_bought = True
                return i

        return None



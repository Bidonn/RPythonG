from operator import truediv

import pygame
import project.theGame.settings as s


class ShopKeeper:
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
            return self.rect.colliderect(player_rect)
        return False



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

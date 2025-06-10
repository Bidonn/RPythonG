import pygame
from project.theGame.Classes.Button import Button
import project.theGame.settings as s
from project.theGame.Classes.Class import Class, Warrior, Wizzard

start_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 3 * 2, 200, 50, "Start Game", (255,255,255), (50,255,50))


MENU_BG = pygame.transform.scale(pygame.image.load('imgs/village-bg.png'), (1000, 800))
TITLE_LOGO = pygame.transform.scale(pygame.image.load('imgs/titlelogo.png'), (500, 500))

def ui_menu(WIN: pygame.surface):
    WIN.blit(MENU_BG, (0, 0))
    start_button.draw(WIN)
    WIN.blit(TITLE_LOGO, (s.WIDTH // 2 - TITLE_LOGO.get_width() / 2, s.HEIGHT // 3 - TITLE_LOGO.get_height() / 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False

        if start_button.handle_event(event):
            return True

    return None

def ui_character_select(WIN: pygame.surface):
    warrior_img = pygame.transform.scale(pygame.image.load('imgs/warrior.png'), (120, 240))
    wizzard_img = pygame.transform.scale(pygame.image.load('imgs/wizzard.png'), (120, 240))

    # Utworzenie przycisków
    warrior_button = Button(s.WIDTH // 4 - 100, s.HEIGHT // 2 + 100, 200, 50, "Warrior", (255, 255, 255), (200, 200, 200))
    wizzard_button = Button(s.WIDTH * 3 // 4 - 100, s.HEIGHT // 2 + 100, 200, 50, "Wizzard", (255, 255, 255),
                            (200, 200, 200))

    while True:
        # Wypełnienie tła
        WIN.fill((50, 50, 50))

        # Wyświetlenie tytułu
        title = s.FONT.render("Wybierz swoją postać", True, (255, 255, 255))
        title_rect = title.get_rect(center=(s.WIDTH // 2, 50))
        WIN.blit(title, title_rect)

        # Wyświetlenie obrazków postaci
        WIN.blit(warrior_img, (s.WIDTH // 4 - 60, s.HEIGHT // 2 - 200))
        WIN.blit(wizzard_img, (s.WIDTH * 3 // 4 - 60, s.HEIGHT // 2 - 200))

        # Rysowanie przycisków
        warrior_button.draw(WIN)
        wizzard_button.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            # Obsługa przycisków
            if warrior_button.handle_event(event):
                return Warrior("Gracz")

            if wizzard_button.handle_event(event):
                return Wizzard("Gracz")

        pygame.display.update()

def ui_game_over(WIN: pygame.surface, hero): #game over screen
    pass

def ui_gameplay_overlay(WIN: pygame.surface, hero): #spelle, zycie, staty
    pass
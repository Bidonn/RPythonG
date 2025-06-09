import math
import pygame
import random
import time
import settings as s
from project.theGame.Classes.Class import Warrior, Wizzard
from project.theGame.Classes.Enemy import Enemy
from project.theGame.Classes.Button import Button

pygame.init()

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption('village killer')

# Inicjalizacja bohatera
hero = Warrior("Imie gracza")

# Wczytanie grafik
MENU_BG = pygame.transform.scale(pygame.image.load('imgs/village-bg.png'), (1000, 800))
TITLE_LOGO = pygame.transform.scale(pygame.image.load('imgs/titlelogo.png'), (500, 500))
BG = pygame.transform.scale(pygame.image.load('imgs/tlo2.png'), (2000, 800))
HERO_IMG = pygame.transform.scale(pygame.image.load(hero.image), (60, 120))

# Przeciwnicy
enemy = Enemy("ziutek", s.WIDTH, s.HEIGHT, pygame.transform.scale(pygame.image.load('imgs/villager.png'), (60,120)), s.Scroll)
enemy2 = Enemy("ziutek 2", s.WIDTH, s.HEIGHT - s.HEIGHT/2, pygame.transform.scale(pygame.image.load('imgs/villager.png'), (60,120)), s.Scroll)
enemies = [enemy, enemy2]

# Scroll i gracz
s.Scroll = 0
player = pygame.Rect(hero.X, hero.Y, 60, 120)



def draw(hero, elapsed_time, scroll):
    WIN.blit(BG, (-scroll, 0))

    time_text = s.FONT.render(f"Time: {round(elapsed_time)}s", True, "black")
    WIN.blit(time_text, (10, 10))

    WIN.blit(HERO_IMG, player)

    for enemy in enemies:
        enemy.draw(WIN)

    hero.draw_attack(WIN)

    pygame.display.update()




def clamp_player_position(player):
    if player.y < s.HEIGHT - 550:
        player.y = s.HEIGHT - 550
    if player.y > s.HEIGHT - player.height:
        player.y = s.HEIGHT - player.height
    if player.x < 0:
        player.x = 0
    if player.x > s.WIDTH - player.width:
        player.x = s.WIDTH - player.width


def main():
    start_button = Button(s.WIDTH // 2 - 100, s.HEIGHT // 3 * 2, 200, 50, "Start Game", (255,255,255), (50,255,50))

    run = False
    menu = True
    clock = pygame.time.Clock()
    elapsed_time = 0

    while menu:
        clock.tick(60)
        WIN.blit(MENU_BG,(0,0))
        start_button.draw(WIN)
        WIN.blit(TITLE_LOGO,(s.WIDTH//2 - TITLE_LOGO.get_width()/2,s.HEIGHT//3 - TITLE_LOGO.get_height()/2))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if start_button.handle_event(event):
                menu = False
                run = True

        pygame.display.update()


    start_time = time.time()
    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        hero.update_attack(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                hero.start_attack(pygame.mouse.get_pos(), player)



        keys = pygame.key.get_pressed()

        # Ruch w lewo
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.x > s.WIDTH // 2 or s.Scroll <= 0:
                player.x -= hero.ms
                if player.x < 0:
                    player.x = 0
            else:
                s.Scroll -= hero.ms
                if s.Scroll < 0:
                    s.Scroll = 0

        # Ruch w prawo
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.x < s.WIDTH // 2 or s.Scroll >= BG.get_width() - s.WIDTH:
                player.x += hero.ms
                if player.x > s.WIDTH - player.width:
                    player.x = s.WIDTH - player.width
            else:
                s.Scroll += hero.ms
                max_scroll = BG.get_width() - s.WIDTH
                if s.Scroll > max_scroll:
                    s.Scroll = max_scroll

        # Góra / dół
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= hero.ms
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += hero.ms

        for enemy in enemies:
            enemy.move(player,enemies, s.Scroll)

        clamp_player_position(player)
        draw(hero, elapsed_time, s.Scroll)

    pygame.quit()


if __name__ == '__main__':
    main()

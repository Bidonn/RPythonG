import math
import pygame
import random
import time
import settings as s
from project.theGame.Classes.Enemy import Enemy
import project.theGame.Classes.UI as UI

pygame.init()

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption('village killer')

# Wczytanie grafik
BG = pygame.transform.scale(pygame.image.load('imgs/tlo2.png'), (2000, 800))

# Przeciwnicy
enemy = Enemy("ziutek", s.WIDTH, s.HEIGHT, pygame.transform.scale(pygame.image.load('imgs/villager.png'), (60,120)), s.Scroll, 100)
enemy2 = Enemy("ziutek 2", s.WIDTH, s.HEIGHT - s.HEIGHT/2, pygame.transform.scale(pygame.image.load('imgs/villager.png'), (60,120)), s.Scroll, 100)
enemies = [enemy, enemy2]


def draw(hero, elapsed_time, scroll, player):
    WIN.blit(BG, (-scroll, 0))

    time_text = s.FONT.render(f"Time: {round(elapsed_time)}s", True, "black")
    WIN.blit(time_text, (10, 10))

    WIN.blit(hero.image, player)

    for enemy in enemies:
        enemy.draw(WIN, elapsed_time)

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


    clock = pygame.time.Clock()
    elapsed_time = 0
    while True:
        clock.tick(60)
        if UI.ui_menu(WIN):
            break
        pygame.display.update()

    hero = UI.ui_character_select(WIN)
    if hero is None:  # Jeśli użytkownik zamknął okno
        return

    s.Scroll = 0
    player = pygame.Rect(hero.X, hero.Y, 60, 120)

    start_time = time.time()
    while True:
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
            if not hero.check_attack(enemy, elapsed_time):
                enemies.remove(enemy)
                continue

        clamp_player_position(player)
        draw(hero, elapsed_time, s.Scroll, player)

    pygame.quit()


if __name__ == '__main__':
    main()

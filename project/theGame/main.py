import pygame
import random
import time
import settings as s
from project.theGame.Classes.Class import Class, Warrior, Wizzard

pygame.font.init()

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))

hero = Warrior("Imie gracza")

BG = pygame.transform.scale(pygame.image.load('imgs/tlo2.png'), (2000, 800))
HERO_IMG = pygame.transform.scale(pygame.image.load(hero.image), (60, 120))

pygame.display.set_caption('village killer')


FONT = pygame.font.SysFont('comicsans', 30)
s.Scroll = 0
player = pygame.Rect(hero.X, hero.Y, 60, 120)

def draw(hero, elapsed_time, scroll):
    WIN.blit(BG, (-scroll, 0))  # przesunięcie tła

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", True, "black")
    WIN.blit(time_text, (10, 10))

    WIN.blit(HERO_IMG, player)

    pygame.display.update()


def clamp_player_position(player):
    # Ograniczenie w pionie: max y to połowa wysokości okna, min y to dół okna minus wysokość postaci
    if player.y < s.HEIGHT - 550:
        player.y = s.HEIGHT - 550
    if player.y > s.HEIGHT - player.height:
        player.y = s.HEIGHT - player.height

    # Ograniczenie w poziomie: lewa krawędź to 0, prawa to szerokość okna minus szerokość postaci
    if player.x < 0:
        player.x = 0
    if player.x > s.WIDTH - player.width:
        player.x = s.WIDTH - player.width


def main():

    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0




    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break




        keys = pygame.key.get_pressed()
        # LEWO
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.x > s.WIDTH // 2 or s.Scroll <= 0:  # ZMIANA – tylko jeśli nie można scrollować
                player.x -= hero.ms
                if player.x < 0:  # NOWE – ograniczenie lewej krawędzi
                    player.x = 0
            else:
                s.Scroll -= hero.ms  # NOWE – przesuwanie świata
                if s.Scroll < 0:  # NOWE – ograniczenie lewej granicy świata
                    s.Scroll = 0

        # PRAWO
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.x < s.WIDTH // 2 or s.Scroll >= BG.get_width() - s.WIDTH:  # ZMIANA
                player.x += hero.ms
                if player.x > s.WIDTH - player.width:  # NOWE – ograniczenie prawej krawędzi ekranu
                    player.x = s.WIDTH - player.width
            else:
                s.Scroll += hero.ms  # NOWE – przesuwanie świata
                max_scroll = BG.get_width() - s.WIDTH  # NOWE – maksymalne przesunięcie
                if s.Scroll > max_scroll:  # NOWE – ograniczenie końca świata
                    scroll_offset = max_scroll

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= hero.ms
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += hero.ms

        clamp_player_position(player)

        draw(player, elapsed_time, s.Scroll)


        clamp_player_position(player)  # <- tutaj ograniczamy ruch gracza

        draw(player, elapsed_time, s.Scroll)

    pygame.quit()

if __name__ == '__main__':
    main()
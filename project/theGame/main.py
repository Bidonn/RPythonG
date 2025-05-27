import pygame
import random
import time
import settings as s
from theGame.settings import HEIGHT

pygame.font.init()

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))

BG = pygame.transform.scale(pygame.image.load('imgs/testBG.jpg'), (s.WIDTH, s.HEIGHT))

pygame.display.set_caption('Learnign experience')


FONT = pygame.font.SysFont('comicsans', 30)

def draw(hero, elapsed_time):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", True, "white")

    WIN.blit(time_text, (10,10))

    pygame.draw.rect(WIN, "blue", hero)

    pygame.display.update()



def main():
    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    player = pygame.Rect(s.WIDTH/2, HEIGHT/2, 50, 50)


    while run:
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_DOWN]:
            player.y += 5

        draw(player, elapsed_time)

    pygame.quit()

if __name__ == '__main__':
    main()
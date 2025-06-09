import math
import pygame
import project.theGame.settings as s

class Enemy:
    FONT = pygame.font.SysFont('comicsans', 30)
    def __init__(self, name: str, x ,y, image: pygame.Surface, scroll):
        self.health = 100
        self.x = x
        self.y = y
        self.name = name
        self.attack_cd = 0.0
        self.dmg_cd = 0.0
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.last_scroll = scroll
        print(f"Created Enemy {self.name}")

    def move(self, player, scroll):
        if scroll != self.last_scroll: # zeby sie kleil do tla
            self.x -= (scroll - self.last_scroll)
            self.last_scroll = scroll

        diffx = self.x - player.x
        diffy = self.y - player.y
        #traktujemy ujemne jako dodatnie do pierwiastka i dodajemy na koncu znak
        newx = math.sqrt(abs(diffx) * (1/60))
        self.x -= newx * (1 if diffx > 0 else -1)
        newy = math.sqrt(abs(diffy) * (1/60))
        self.y -= newy * (1 if diffy > 0 else -1)

    def draw(self, WIN: pygame.display):
        WIN.blit(self.image, (self.x, self.y))
        if s.DEBUG:
            debug_text = s.FONT.render(f"{int(self.x)}, {int(self.y)}", True, "black")
            WIN.blit(debug_text, (self.x, self.y -60))
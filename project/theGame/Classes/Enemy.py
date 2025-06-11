from __future__ import annotations # type hinting klasy w klasie

import math
import pygame
import project.theGame.settings as s
from typing import List


class Enemy:
    FONT = pygame.font.SysFont('comicsans', 30)
    def __init__(self, name: str, x ,y, image: pygame.Surface, scroll, max_health):
        self.health = max_health
        self.max_health = max_health
        self.x = x
        self.y = y
        self.name = name
        self.attack_cd = 0.0
        self.dmg_cd = 0.0
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.last_scroll = scroll
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        print(f"Created Enemy {self.name}")

    def clamp_position(self):
        if self.y < s.HEIGHT - 550:
            self.y = s.HEIGHT - 550
        if self.y > s.HEIGHT - self.height:
            self.y = s.HEIGHT - self.height
        if self.x < 0:
            self.x = 0
        if self.x > s.WIDTH - self.width:
            self.x = s.WIDTH - self.width
        # Aktualizujemy rect
        self.rect.x = self.x
        self.rect.y = self.y


    def take_damage(self, hero, gametime): # true jesli enemis zyje false jesli wlasnie umarl od ataku
        if self.dmg_cd > gametime:
            return True
        else:
            self.dmg_cd = gametime + 0.5

        self.health -= hero.level * 1000
        if self.health < 0:
            hero.score += self.max_health * hero.level
            return False
        else:
            return True


    def move(self, player, enemies: List[Enemy], scroll):
        if scroll != self.last_scroll: # zeby sie kleil do tla
            self.x -= (scroll - self.last_scroll)
            self.last_scroll = scroll

        diffx = self.x - player.x
        diffy = self.y - player.y
        #traktujemy ujemne jako dodatnie do pierwiastka i dodajemy na koncu znak
        newx = math.sqrt(abs(diffx) * (1/60))
        newy = math.sqrt(abs(diffy) * (1/60))

        # Tymczasowo zapisujemy nową pozycję
        move_x =  newx * (1 if diffx > 0 else -1)
        move_y =  newy * (1 if diffy > 0 else -1)

        # Próbujemy ruch w poziomie i pionie
        self.x -= move_x
        self.y -= move_y
        self.rect.x = self.x
        self.rect.y = self.y

        # Sprawdzamy kolizje i odpychamy jeśli są
        for other in enemies:
            if other != self and self.rect.colliderect(other.rect):
                # Obliczamy wektor między środkami przeciwników
                dx = self.rect.centerx - other.rect.centerx
                dy = self.rect.centery - other.rect.centery

                # Normalizujemy wektor (zamieniamy na jednostkowy)
                distance = math.sqrt(dx * dx + dy * dy)
                if distance == 0:  # jeśli są dokładnie w tym samym miejscu
                    dx, dy = 1, 0  # przesuwamy w prawo
                else:
                    dx = dx / distance
                    dy = dy / distance

                # Odpychamy się od siebie
                push_strength = 2  # siła odpychania
                self.x += dx * push_strength
                self.y += dy * push_strength
                self.rect.x = self.x
                self.rect.y = self.y

        self.clamp_position() # clamp i aktualizacja recta


    def draw(self, WIN: pygame.display, gametime):
        WIN.blit(self.image, (self.x, self.y))
        color = (255,0,0)
        if self.dmg_cd > gametime:
            color = (50,50,50)
        pygame.draw.rect(WIN, color, (self.x - 10, self.y - 20, max(80 * (self.health/self.max_health), 5),15))
        if s.DEBUG:
            debug_text = s.FONT.render(f"{int(self.x)}, {int(self.y)}", True, "black")
            WIN.blit(debug_text, (self.x, self.y -60))
            pygame.draw.rect(WIN, (255, 0, 0), self.rect, 2)

import math
from abc import ABC, abstractmethod
import project.theGame.settings as s
import pygame


class Class(ABC):
    def __init__(self, name: str, hp: int, ms: int, image: str, score, dmg = 10,level=1):
        self.level = level
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.ms = ms
        self.image = pygame.transform.scale(pygame.image.load(image), (60, 120))
        self.X = 20
        self.Y = s.HEIGHT / 2
        self.score = score
        self.dmg_cd = 0
        self.player = pygame.Rect(self.X, self.Y, self.image.get_width(),self.image.get_height())
        self.DMG = dmg
        self.character_class = None

    def check_damage(self, enemy, elapsed_time):
        if elapsed_time > self.dmg_cd:


            if self.player.colliderect(enemy.rect):
                self.dmg_cd = elapsed_time + 0.5
                self.hp -= 10

        if self.hp <= 0:
            return False
        else:
            return True

    @abstractmethod
    def spell1(self):
        pass

    @abstractmethod
    def spell2(self):
        pass

    @abstractmethod
    def spell3(self):
        pass

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def start_attack(self, mouse_pos, player_rect):
        pass

    @abstractmethod
    def update_attack(self, player_rect):
        pass


    @abstractmethod
    def draw_attack(self, surface):
        pass

    @abstractmethod
    def check_attack(self, enemy, gametime): # pls zaimplementuj w wizardzie
        pass


class Warrior(Class):
    sword_timelimit = 1.5
    def __init__(self, name, score, level=1, ms=10, dmg=10, hp=100):
        self.sword_angle = 0
        self.sword_img = pygame.transform.scale(pygame.image.load("imgs/sword.png"), (100, 33))
        self.sword_active = False
        self.sword_timer = 0
        self.sword_base_angle = 0  # Kąt bazowy (do kursora)
        self.sword_attack_duration = 0.3  # sekundy
        self.sword_pos = (0, 0)
        super().__init__(name, hp, ms, "imgs/warrior.png", score, dmg, level)
        self.character_class = "Warrior"
        print("Created Warrior")

    def spell1(self):
        pass

    def spell2(self):
        pass

    def spell3(self):
        pass

    def attack(self):
        pass

    def start_attack(self, mouse_pos, player_rect):
        """Rozpoczyna animację ataku w kierunku kursora."""
        if not self.sword_active:
            self.sword_active = True
            self.sword_timer = pygame.time.get_ticks() / 1000  # w sekundach

            dx = mouse_pos[0] - player_rect.centerx
            dy = mouse_pos[1] - player_rect.centery
            self.sword_base_angle = math.degrees(math.atan2(-dy, dx))

    def update_attack(self, player_rect):
        """Aktualizuje pozycję i kąt miecza co klatkę."""
        if not self.sword_active:
            return

        t = pygame.time.get_ticks() / 1000 - self.sword_timer
        if t > self.sword_attack_duration:
            self.sword_active = False
            self.sword_angle = 0
            self.sword_pos = (-1000, -1000)  # poza ekranem
            return

        # Animacja kąta: od -45° do +45° względem kąta bazowego
        progress = t / self.sword_attack_duration
        swing_offset = -45 + 90 * progress
        self.sword_angle = self.sword_base_angle + swing_offset

        # Pozycja miecza względem gracza
        angle_rad = math.radians(self.sword_angle)
        offset_x = math.cos(angle_rad) * 60
        offset_y = -math.sin(angle_rad) * 60
        self.sword_pos = (player_rect.centerx + offset_x, player_rect.centery + offset_y)


    def draw_attack(self, surface):
        """Rysuje miecz jeśli aktywny."""
        if not self.sword_active:
            return

        rotated_sword = pygame.transform.rotate(self.sword_img, self.sword_angle)
        rect = rotated_sword.get_rect(center=self.sword_pos)
        surface.blit(rotated_sword, rect.topleft)

    def check_attack(self, enemy, gametime): # true jesli enemis zyje false jesli wlasnie umarl od ataku
        if not self.sword_active:  # jeśli miecz nie jest aktywny, nie sprawdzamy ataku
            return True

            # Obliczamy środek miecza na podstawie sword_pos
        sword_center_x = self.sword_pos[0]
        sword_center_y = self.sword_pos[1]

        # Obliczamy środek przeciwnika
        enemy_center_x = enemy.x + enemy.width / 2
        enemy_center_y = enemy.y + enemy.height / 2

        # Obliczamy odległość między mieczem a przeciwnikiem używając wzoru na odległość między punktami
        distance = math.sqrt(
            (sword_center_x - enemy_center_x) ** 2 +
            (sword_center_y - enemy_center_y) ** 2
        )

        # Jeśli przeciwnik jest w zasięgu 50 pikseli od miecza
        if distance <= 80:
            # Wywołujemy metodę take_damage na przeciwniku
            return enemy.take_damage(self, gametime)

        return True


class Wizzard(Class):
    def __init__(self, name, score, level=1, ms=4, dmg=10, hp=50):
        self.magic_cd = 1
        self.magic_timer = 0
        self.magic_missiles = []
        self.magic_cd = 5  # cooldown w milisekundach
        self.magic_timer = 0
        self.magic_damage = 20
        self.missile_speed = 5
        self.missile_radius = 5  # promień kółka pocisku
        self.missile_color = (0, 0, 255)  # niebieski kolor

        # Obrazek pocisku
        self.missile_img = pygame.Surface((40, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(self.missile_img, (0, 150, 255), (0, 0, 40, 16))
        super().__init__(name, hp, ms, "imgs/wizzard.png", score, dmg, level)
        self.character_class = "Wizzard"
        print("Created Wizzard")

    def spell1(self):
        pass

    def spell2(self):
        pass

    def spell3(self):
        pass

    def attack(self):
        pass

    def start_attack(self, mouse_pos, player_rect):
        # Sprawdzenie cooldownu
        current_time = pygame.time.get_ticks()
        if current_time - self.magic_timer < self.magic_cd:
            return False

        # Resetowanie timera
        self.magic_timer = current_time

        # Obliczenie kierunku pocisku (np. w stronę kursora myszy)
        dx = mouse_pos[0] - player_rect.centerx
        dy = mouse_pos[1] - player_rect.centery
        direction = math.atan2(dy, dx)

        # Tworzenie nowego pocisku
        new_missile = Missile(
            x=player_rect.centerx,
            y=player_rect.centery,
            direction=direction,
            speed=self.missile_speed,
            damage=self.magic_damage,
            owner=self,
            radius=self.missile_radius,
            color=self.missile_color

        )

        # Dodanie pocisku do tablicy
        self.magic_missiles.append(new_missile)
        return True

    def update_attack(self, player_rect):
        # Aktualizacja wszystkich aktywnych pocisków
        for missile in self.magic_missiles[:]:  # Kopia listy, żeby bezpiecznie usuwać elementy
            missile.update()

            # Usuwanie nieaktywnych pocisków z listy
            if not missile.active:
                self.magic_missiles.remove(missile)

    def draw_attack(self, surface):
        # Rysowanie wszystkich aktywnych pocisków
        for missile in self.magic_missiles:
            missile.draw(surface)

    def check_attack(self, enemy, gametime):
        """
        Sprawdza kolizję wszystkich pocisków z danym przeciwnikiem.
        Zwraca True jeśli przeciwnik żyje, False jeśli został pokonany.
        """
        enemy_alive = True

        # Sprawdzanie kolizji dla wszystkich pocisków
        for missile in self.magic_missiles[:]:  # Kopia listy
            # Sprawdź kolizję z przeciwnikiem
            if not missile.check_collision(enemy, gametime):
                enemy_alive = False
                # Wróć wcześniej, ponieważ przeciwnik już został pokonany
                break

        # Usuń nieaktywne pociski
        self.magic_missiles = [m for m in self.magic_missiles if m.active]

        return enemy_alive  # True jeśli przeciwnik żyje, False jeśli został pokonany


class Missile:
    def __init__(self, x, y, direction, speed, damage, owner, radius=5, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.direction = direction  # kąt w radianach
        self.speed = speed
        self.damage = damage
        self.owner = owner  # odniesienie do postaci, która wystrzeliła pocisk
        self.radius = radius  # promień kółka
        self.color = color  # kolor RGB (0,0,255) to niebieski
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 5000  # czas życia pocisku w milisekundach (3 sekundy)

        # Obliczenie wektora kierunku na podstawie kąta
        self.dx = math.cos(self.direction) * self.speed
        self.dy = math.sin(self.direction) * self.speed

        # Tworzymy prostokąt do kolizji
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)

    def update(self):
        # Sprawdzenie czy pocisk nie przekroczył czasu życia
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.lifetime:
            self.active = False
            return

        # Aktualizacja pozycji
        self.x += self.dx
        self.y += self.dy

        # Aktualizacja prostokąta
        self.rect.center = (self.x, self.y)

        # Sprawdzenie czy pocisk nie wyleciał poza ekran
        if (self.x < 0 or self.x > s.WIDTH or
                self.y < 0 or self.y > s.HEIGHT):
            self.active = False

    def draw(self, screen):

        if self.active:
            # Rysowanie kółka zamiast obrazka
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

            # Opcjonalnie: dodaj efekt blasku (większe, półprzezroczyste kółko)
            # Aby to zrobić, potrzebujesz powierzchni z przezroczystością
            glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.color, 100), (self.radius * 2, self.radius * 2), self.radius * 2)
            screen.blit(glow_surface, (int(self.x) - self.radius * 2, int(self.y) - self.radius * 2))

    def check_collision(self, enemy, gametime):
        """Sprawdza kolizję z przeciwnikiem i wywołuje jego metodę take_damage"""
        if not self.active:
            return True  # pocisk nieaktywny, przeciwnik żyje

        # Prostokąt dla pocisku
        missile_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                   self.radius * 2, self.radius * 2)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

        if missile_rect.colliderect(enemy_rect):
            self.active = False  # pocisk znika po trafieniu
            return enemy.take_damage(self.owner, gametime)

        return True  # przeciwnik żyje, nie został trafiony


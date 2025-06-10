import math
from abc import ABC, abstractmethod
import project.theGame.settings as s
import pygame


class Class(ABC):
    def __init__(self, name: str, player: str, hp: int, ms: int, image: str, level, score):
        self.level = level
        self.player = player
        self.name = name
        self.hp = hp
        self.ms = ms
        self.image = pygame.transform.scale(pygame.image.load(image), (60, 120))
        self.X = 20
        self.Y = s.HEIGHT / 2
        self.score = score



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
    def __init__(self, player: str, level, score):
        self.sword_angle = 0
        self.sword_img = pygame.transform.scale(pygame.image.load("imgs/sword.png"), (100, 33))
        self.sword_active = False
        self.sword_timer = 0
        self.sword_base_angle = 0  # Kąt bazowy (do kursora)
        self.sword_attack_duration = 0.25  # sekundy
        self.sword_pos = (0, 0)
        super().__init__("Warrior", player, 100, 10, "imgs/warrior.png", level, score)
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
        if distance <= 50:
            # Wywołujemy metodę take_damage na przeciwniku
            return enemy.take_damage(self, gametime)

        return True


class Wizzard(Class):
    def __init__(self, player: str, level, score):
        super().__init__("Wizzard", player, 50, 4, "imgs/wizzard.png", level, score)
        print("Created Wizzard")

    def spell1(self):
        pass

    def spell2(self):
        pass

    def spell3(self):
        pass

    def attack(self):
        pass

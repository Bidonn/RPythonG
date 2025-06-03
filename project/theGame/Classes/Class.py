from abc import ABC, abstractmethod
import project.theGame.settings as s
import pygame


class Class(ABC):
    def __init__(self, name: str, player: str, hp:int, ms: int, image: str):
        self.level = 1
        self.player = player
        self.name = name
        self.hp = hp
        self.ms = ms
        self.image = image
        self.X = s.WIDTH/2
        self.Y = s.HEIGHT/2

    @abstractmethod
    def spell1(self):
        pass  # This is an abstract method, no implementation here.

    @abstractmethod
    def spell2(self):
        pass

    @abstractmethod
    def spell3(self):
        pass

    @abstractmethod
    def attack(self):
        pass

class Warrior(Class):

    def __init__(self, player: str):
        super().__init__("Warrior", player, 100, 3, "imgs/warrior.png")
        print("Created Warrior")

    def spell1(self):
        pass

    def spell2(self):
        pass

    def spell3(self):
        pass

    def attack(self):
        pass

class Wizzard(Class):
    def __init__(self, player: str):
        super().__init__("Wizzard", player, 50, 4, "imgs/wizzard.png")
        print("Created Wizzard")

    def spell1(self):
        pass

    def spell2(self):
        pass

    def spell3(self):
        pass

    def attack(self):
        pass
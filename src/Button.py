import pygame
import project.theGame.settings as s
class Button:
    """
    pomocnicza klasa do przyciskow w ui
    """
    def __init__(self, x, y, width, height, text, color, hover_color):
        """
        tworzernie obiektu przycisku
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = s.FONT

    def draw(self, surface):
        """
        rysowanie przycisku
        """
        pygame.draw.rect(surface, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        obsługa kliknięcia przycisku
        """
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

import pygame
import sys
import time
from SuivreCarte import main_SuivreCarte
from Sac import main_Sac

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0, 128)  # 128 pour de la transparence
WHITE = (255, 255, 255)
RED = (0, 0, 0, 128)

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

background_image = pygame.image.load("fonds\\plage.jpeg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Police de texte
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

def open_new_window_choix1():
    main_SuivreCarte()
    print("Ouverture d'une nouvelle fenêtre")

def open_new_window_choix2():
    main_Sac()
    print("Ouverture d'une nouvelle fenêtre")

class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, 28)
        self.rendered_text = None
        self.displayed_text = ""
        self.background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.background_color = (0, 0, 0, 128)

    def set_text(self, text):
        self.text = text
        self.rendered_text = self.font.render(self.text, True, WHITE)

    def display_text(self, delay=0.05):
        self.displayed_text = ""
        for i in range(len(self.text)):
            self.displayed_text += self.text[i]
            self.rendered_text = self.font.render(self.displayed_text, True, WHITE)
            self.background_surface.fill((0, 0, 0, 200))  # Fill with transparent background
            pygame.draw.rect(self.background_surface, self.background_color, self.rect)
            self.background_surface.blit(self.rendered_text, self.rect.topleft)
            screen.blit(background_image, (0, 0))
            screen.blit(self.background_surface, self.rect.topleft)
            pygame.display.flip()
            time.sleep(delay)

    def draw(self):
        screen.blit(self.background_surface, self.rect.topleft)
        if self.rendered_text:
            screen.blit(self.rendered_text, self.rect.topleft)

def draw_Nauffrage(choix1, choix2, text_box, display_buttons):
    screen.blit(background_image, (0, 0))

    # Dessiner la boîte de texte
    text_box.draw()

    if display_buttons:
        # Dessiner les boutons
        choix1.draw()
        choix2.draw()

    pygame.display.flip()

def main_Nauffrage():
    pygame.display.set_caption("Nauffrage")
    choix1 = Button(screen_width // 4, 220, screen_width // 2, 50, "Suivre le chien", open_new_window_choix1)
    choix2 = Button(screen_width // 4, 300, screen_width // 2, 50, "Fouiller le sac", open_new_window_choix2)
    text_box = TextBox(0, 400, screen_width, 200)
    display_buttons = False

    screen.blit(background_image, (0, 0))

    # Délai avant écriture de 0,6 secondes
    pygame.time.delay(600)

    # Affichage du texte
    text_box.set_text("Le texte défile au fur et à mesure.")
    text_box.display_text()
    display_buttons = True

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if choix1.rect.collidepoint(event.pos):
                    # Action pour le bouton "choix1"
                    if choix1.action:
                        choix1.action()
                elif choix2.rect.collidepoint(event.pos):
                    # Action pour le bouton "choix2"
                    if choix2.action:
                        choix2.action()
                    running = False

        draw_Nauffrage(choix1, choix2, text_box, display_buttons)

if __name__ == "__main__":
    main_Nauffrage()

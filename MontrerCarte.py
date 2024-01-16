import pygame
import sys
import time

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0, 128) # 128 pour de la transparence

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

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

def open_new_window():
    print("Ouverture d'une nouvelle fenêtre")

class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.font = pygame.font.Font(None, 28)
        self.rendered_text = None
        self.displayed_text = ""

    def set_text(self, text):
        self.text = text
        self.rendered_text = self.font.render(self.text, True, WHITE)

    def display_text(self, delay=0.05):
        self.displayed_text = ""
        for i in range(len(self.text)):
            self.displayed_text += self.text[i]
            self.rendered_text = self.font.render(self.displayed_text, True, WHITE)
            screen.fill(BLACK)  # Remplissage avec la couleur noire transparente
            pygame.draw.rect(screen, RED, self.rect)
            screen.blit(self.rendered_text, self.rect.topleft)
            pygame.display.flip()
            time.sleep(delay)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
        if self.rendered_text:
            screen.blit(self.rendered_text, self.rect.topleft)

def draw_MontrerCarte(choix1, choix2, text_box, display_buttons):
    screen.fill(BLACK)

    # Dessiner la boîte de texte
    text_box.draw()

    if display_buttons:
        # Dessiner les boutons
        choix1.draw()
        choix2.draw()

    pygame.display.flip()

def main_MontrerCarte():
    pygame.display.set_caption("Merci")
    choix1 = Button(screen_width // 4, 220, screen_width // 2, 50, "Choix1 - Suite", open_new_window)
    choix2 = Button(screen_width // 4, 300, screen_width // 2, 50, "Choix2 - Quit", sys.exit)
    text_box = TextBox(0, 400, screen_width, 200)
    display_buttons = False

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
                        display_buttons = True
                    running = False

        draw_MontrerCarte(choix1, choix2, text_box, display_buttons)

if __name__ == "__main__":
    main_MontrerCarte()
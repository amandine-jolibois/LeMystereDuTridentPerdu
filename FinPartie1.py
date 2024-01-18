import pygame
import sys
from pygame import image, transform
from Partir import main_Partir
from Entrer import main_Entrer

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des couleurs
BLACK = (0, 0, 0, 128)  # 128 pour de la transparence
WHITE = (255, 255, 255)
SABLE = (224, 205, 169)

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#icon = pygame.image.load("fonds\\Tete-Trident.ico").convert_alpha()

background_image = pygame.image.load("fonds\\devanttemple.jpeg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

i = 0

# Police de texte
font = pygame.font.Font(None, 30)


class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, SABLE, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_lines = []
        self.font = pygame.font.Font(None, 30)
        self.rendered_lines = []

    def set_text(self, text):
        self.text_lines = text.split('\n')
        self.rendered_lines = [self.font.render(line, True, (255, 255, 255)) for line in self.text_lines]

    def draw(self):
        transparent_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (0, 0, 0, 170), transparent_surface.get_rect())

        y_offset = 0
        for rendered_line in self.rendered_lines:
            transparent_surface.blit(rendered_line, (0, y_offset))
            y_offset += self.font.get_height()

        screen.blit(transparent_surface, self.rect.topleft)

    def clear_text(self):
        self.text_lines = []
        self.rendered_lines = []

    def set_new_text(self, new_text):
        self.text_lines = new_text.split('\n')
        self.rendered_lines = [self.font.render(line, True, (255, 255, 255)) for line in self.text_lines]

def open_new_window_choix1():
    main_Partir()
    print("Ouverture d'une nouvelle fenêtre")


def open_new_window_choix2():
    main_Entrer()
    print("Ouverture d'une nouvelle fenêtre")

def draw_Nauffrage(choix1, choix2):
    global i
    screen.blit(background_image, (0, 0))


    # Dessiner les boutons
    choix1.draw()
    choix2.draw()

    pygame.display.flip()


def main_FinPartie1():
    global i
    pygame.mixer.music.load("Son\\Environnement\\voit le temple.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    pygame.display.set_caption("Le temple !")
    # pygame.display.set_icon(icon)

    running = True

    choix1 = Button(screen_width // 3, 220, screen_width // 3, 50, "Trop dangereux - Partir", open_new_window_choix1)
    choix2 = Button(screen_width // 3, 300, screen_width // 3, 50, "Entrer dans le Temple", open_new_window_choix2)

    # Dessiner les boutons et le bouton "Suite >>"
    draw_Nauffrage(choix1, choix2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
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


            pygame.display.flip()

if __name__ == "__main__":
    main_FinPartie1()

pygame.mixer.music.stop()

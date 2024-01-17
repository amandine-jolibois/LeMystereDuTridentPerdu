import pygame
import sys
from Nauffrage import main_Nauffrage

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
background_image = pygame.image.load("fonds\\Titre.jpeg")
background_image = pygame.transform.scale(background_image, (800, 600))

# Police de texte
font = pygame.font.Font(None, 36)


class Button:
    def __init__(self, image_path, position, size, action):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=position)
        self.action = action

    def draw(self):
        screen.blit(self.image, self.rect)


def draw_menu(start_button, quit_button):
    screen.blit(background_image, (0, 0))

    # Dessiner les boutons
    start_button.draw()
    quit_button.draw()

    pygame.display.flip()


def open_new_window():
    main_Nauffrage()
    print("Ouverture d'une nouvelle fenêtre (Start)")


def main_menu():
    pygame.mixer.music.load("Son\\Environnement\\Embiance.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    pygame.display.set_caption("Menu Principal")
    # pygame.display.set_icon("fonds\\Tete-Trident.ico")
    start_button = Button("Buttons\\PlayUp.png", (275, 250), (250, 120), action=open_new_window)
    quit_button = Button("Buttons\\QuitUp.png", (275, 370), (250, 120), action=sys.exit)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if start_button.rect.collidepoint(event.pos):
                    start_button = Button("Buttons\\PlayDown.png", (275, 250), (250, 120), action = open_new_window)
                elif quit_button.rect.collidepoint(event.pos):
                    quit_button = Button("Buttons\\QuitDown.png", (275, 370), (250, 120), action=sys.exit)
                else:
                    start_button = Button("Buttons\\PlayUp.png", (275, 250), (250, 120), action=open_new_window)
                    quit_button = Button("Buttons\\QuitUp.png", (275, 370), (250, 120), action=sys.exit)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(event.pos):
                    # Action pour le bouton "Start"
                    if start_button.action:
                        start_button.action()
                elif quit_button.rect.collidepoint(event.pos):
                    # Action pour le bouton "Quit"
                    if quit_button.action:
                        quit_button.action()
                        pygame.mixer.music.stop()
                    running = False

        draw_menu(start_button, quit_button)


# Exécution du menu principal
main_menu()
pygame.mixer.music.stop()

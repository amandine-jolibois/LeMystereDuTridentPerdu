import pygame
import sys
from pygame import image, transform


# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des couleurs
BLACK = (0, 0, 0, 128)  # 128 pour de la transparence
WHITE = (255, 255, 255)
MER = (2 , 125 , 173)

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#icon = pygame.image.load("fonds\\Tete-Trident.ico").convert_alpha()

background_image = pygame.image.load("fonds\\Game-over.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


son_GameOver = pygame.mixer.Sound("Son\\Song Part2\\game-over.mp3")
son_GameOver.set_volume(0.5)

i = 0

# Police de texte
font = pygame.font.Font(None, 30)


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
    from Menu import main_menu
    main_menu()
    print("Ouverture d'une nouvelle fenêtre")

def draw_Nauffrage(next_button):
    global i
    screen.blit(background_image, (0, 0))

    # Dessiner les boutons
    next_button.draw()

    pygame.display.flip()


def main_FIN():
    global i
    son_GameOver.play(-1)
    pygame.mixer.music.set_volume(0.5)
    pygame.display.set_caption("Game Over")
    # pygame.display.set_icon(icon)

    next_button = Button(700, 550, 100, 50, "Menu", open_new_window_choix1)

    running = True


    # Dessiner les boutons et le bouton "Suite >>"
    draw_Nauffrage(next_button)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.rect.collidepoint(event.pos):
                    # Action pour le bouton "Suite >>"
                    if next_button.action:
                        son_GameOver.stop()
                        next_button.action()
                        i = 0
                        open_new_window_choix1()

            pygame.display.flip()

if __name__ == "__main__":
    main_FIN()

son_GameOver.stop()

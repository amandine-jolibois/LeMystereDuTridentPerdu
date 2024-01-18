import pygame
import sys
from pygame import image, transform
from SuivreCarte import main_SuivreCarte
from Quitter import main_Quitter

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

background_image = pygame.image.load("fonds\\plage.jpeg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Chargez les images
hero = image.load("personages\\hero.png")
chienoff = image.load("personages\\chienoff.png")
herooff = image.load("personages\\herooff.png")
chien = image.load("personages\\chien.png")

hero = pygame.transform.scale(hero, (100, 200))
chienoff = pygame.transform.scale(chienoff, (200, 400))
herooff = pygame.transform.scale(herooff, (200, 400))
chien = pygame.transform.scale(chien, (200, 400))

# Chargez les images
left_images = [image.load("personages\\hero.png"), image.load("personages\\herooff.png"), image.load("personages\\hero.png"), image.load("personages\\herooff.png")]
right_images = [image.load("personages\\transparent.png"), image.load("personages\\chien.png"), image.load("personages\\chienoff.png"), image.load("personages\\chien.png")]

for i in range(len(left_images)):
    left_images[i] = pygame.transform.scale(left_images[i], (200, 400))
    right_images[i] = pygame.transform.scale(right_images[i], (200, 400))

son_pas_Chien = pygame.mixer.Sound("Son\\Chien\\Respiration chien.mp3")
son_pas_Chien.set_volume(0.8)

i = 0
global AvoirCouteau
AvoirCouteau = False

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


text_box = TextBox(0, 400, screen_width, 200)

def open_new_window_choix1():
    main_SuivreCarte()
    print("Ouverture d'une nouvelle fenêtre")


def open_new_window_choix2():
    main_Quitter()
    print("Ouverture d'une nouvelle fenêtre")


current_left_image_index = 0
current_right_image_index = 0

def change_images_left():
    global current_left_image_index
    left_image = left_images[current_left_image_index]
    current_left_image_index = (current_left_image_index + 1) % len(left_images)
    return left_image

def change_images_right():
    global current_right_image_index
    right_image = right_images[current_right_image_index]
    current_right_image_index = (current_right_image_index + 1) % len(right_images)
    return right_image

def draw_Nauffrage(choix1, choix2, text_box):
    global i
    screen.blit(background_image, (0, 0))

    # Dessinez les images à côté des boutons
    screen.blit(change_images_left(), (40, 0))
    screen.blit(change_images_right(), (560, 60))

    # Dessiner la boîte de texte semi-transparente en bas
    text_box.draw()

    choix1.draw()
    choix2.draw()

    pygame.display.flip()


def main_Couteau():
    global i
    global AvoirCouteau
    AvoirCouteau = False
    pygame.mixer.music.load("Son\\Environnement\\Embiance.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    pygame.display.set_caption("Couteau")
    # pygame.display.set_icon(icon)

    choix1 = Button(screen_width // 3, 220, screen_width // 3, 50, "Suivre le chien", open_new_window_choix1)
    choix2 = Button(screen_width // 3, 300, screen_width // 3, 50, "Prendre le bateau", open_new_window_choix2)

    # Créer une instance de TextBox et définir le texte
    text_box = TextBox(0, 400, screen_width, 200)
    son_pas_Chien.play()
    text_box.set_text(" \n  Vous avez pris le couteau, il a beau être en piteux état il pourrait bien servir.")

    next_button = Button(700, 550, 100, 50, "Suite>>", text_box.clear_text)

    running = True

    # Dessiner la boîte de texte
    text_box.draw()

    # Dessiner les boutons et le bouton "Suite >>"
    draw_Nauffrage(choix1, choix2, text_box)

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
                        AvoirCouteau = True
                        son_pas_Chien.stop()
                        choix1.action()
                elif choix2.rect.collidepoint(event.pos):
                    # Action pour le bouton "choix2"
                    if choix2.action:
                        pygame.mixer.music.stop()
                        son_pas_Chien.stop()
                        choix2.action()
                    running = False

            pygame.display.flip()

if __name__ == "__main__":
    main_Couteau()

pygame.mixer.music.stop()

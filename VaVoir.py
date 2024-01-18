import pygame
import sys
from pygame import image, transform
from Prisonnier import main_Prisonnier

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Définition des couleurs
BLACK = (0, 0, 0, 128)  # 128 pour de la transparence
WHITE = (255, 255, 255)
FORET = (23 , 89 , 47)

# Configuration de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#icon = pygame.image.load("fonds\\Tete-Trident.ico").convert_alpha()

background_image = pygame.image.load("fonds\\foret.jpeg")
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
left_images = [image.load("personages\\hero.png"), image.load("personages\\herooff.png"), image.load("personages\\hero.png"), image.load("personages\\herooff.png"), image.load("personages\\hero.png"), image.load("personages\\herooff.png"), image.load("personages\\hero.png"), image.load("personages\\herooff.png"), image.load("personages\\hero.png")]
right_images = [image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png")]

for i in range(len(left_images)):
    left_images[i] = pygame.transform.scale(left_images[i], (200, 400))
    right_images[i] = pygame.transform.scale(right_images[i], (200, 400))

son_Ligotement = pygame.mixer.Sound("Son\\Song Part2\\ligotement.mp3")
son_Ligotement.set_volume(0.8)

i = 0

# Police de texte
font = pygame.font.Font(None, 30)


class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, FORET, self.rect)
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

def open_new_window_choix1():
    main_Prisonnier()
    print("Ouverture d'une nouvelle fenêtre")

def draw_Nauffrage(text_box, next_button):
    global i
    screen.blit(background_image, (0, 0))

    # Dessinez les images à côté des boutons
    screen.blit(change_images_left(), (40, 0))
    screen.blit(change_images_right(), (560, 0))

    # Dessiner la boîte de texte semi-transparente en bas
    text_box.draw()

    # Dessiner les boutons
    next_button.draw()

    pygame.display.flip()


def main_VaVoir():
    global i
    pygame.display.set_caption("Dommage..")
    # pygame.display.set_icon(icon)

    # Créer une instance de TextBox et définir le texte
    text_box = TextBox(0, 400, screen_width, 200)
    text_box.set_text(" \n  Ce sont des voix, je ne suis peut être pas tout seul sur cette île.\n \n  Ils pourront peut être m’aider\n \n  Alors que vous vous approchez des voix vous rencontrez trois personnes.")

    next_button = Button(700, 550, 100, 50, "Suite>>", text_box.clear_text)

    running = True

    # Dessiner la boîte de texte
    text_box.draw()

    # Dessiner les boutons et le bouton "Suite >>"
    draw_Nauffrage(text_box, next_button)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.rect.collidepoint(event.pos):
                    # Action pour le bouton "Suite >>"
                    if next_button.action:
                        next_button.action()
                        if i == 0:
                            text_box.set_new_text("\n  Dépêchez-vous de décharger le matériel ! On a pas toute la journée !")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 1:
                            text_box.set_new_text("\n  L’homme à la barbe va se retourner vers vous, il ne semblait pas commode.")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 2:
                            text_box.set_new_text("\n  Qu’est ce que tu veux toi ? Tu viens pour nous devancer ?")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 3:
                            text_box.set_new_text("\n  Non, je suis perdu sur l’île, je ne sais même pas ce que vous cherchez !")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 4:
                            text_box.set_new_text("\n  Tu ne viendrait pas sur l’île sans vouloir obtenir le trident caché.")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 5:
                            text_box.set_new_text("\n  C’est donc là que ça mène…")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 6:
                            text_box.set_new_text("\n  Donc tu es bien là pour nous devancer !\n \n  Capturez le et empêchez le de nous voler le trident.")
                            draw_Nauffrage(text_box, next_button)
                            son_Ligotement.play()
                        elif i == 7:
                            text_box.set_new_text("\n  Les sbires vont vous attraper sans que aillez le temps de réagir et vous\n \n  attaqueront les mains dans le dos avant de vous accrocher à un arbre pour\n \n  ne pas que vous vous mettiez en travers de leur chemin.")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 8:
                            son_Ligotement.stop()
                            open_new_window_choix1()

                        i += 1

            pygame.display.flip()

if __name__ == "__main__":
    main_VaVoir()

pygame.mixer.music.stop()

import pygame
import sys
from pygame import image, transform
from FIN import main_FIN


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

background_image = pygame.image.load("fonds\\plage.jpeg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Chargez les images
hero = image.load("personages\\hero.png")
herooff = image.load("personages\\herooff.png")

hero = pygame.transform.scale(hero, (100, 200))
herooff = pygame.transform.scale(herooff, (200, 400))

# Chargez les images
left_images = [image.load("personages\\hero.png")]

for i in range(len(left_images)):
    left_images[i] = pygame.transform.scale(left_images[i], (200, 400))

son_Gonfle = pygame.mixer.Sound("Son\\Song Part2\\Gonflage bateau.mp3")
son_Gonfle.set_volume(0.3)

son_Degonfle = pygame.mixer.Sound("Son\\Song Part2\\degonflage bateau.mp3")
son_Degonfle.set_volume(0.3)

son_Plouf = pygame.mixer.Sound("Son\\Song Part2\\Plouf.mp3")
son_Plouf.set_volume(0.3)


i = 0

# Police de texte
font = pygame.font.Font(None, 30)


class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, MER, self.rect)
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
    main_FIN()
    print("Ouverture d'une nouvelle fenêtre")


current_left_image_index = 0

def change_images_left():
    global current_left_image_index
    left_image = left_images[current_left_image_index]
    current_left_image_index = (current_left_image_index + 1) % len(left_images)
    return left_image

def draw_Nauffrage(text_box, next_button):
    global i
    screen.blit(background_image, (0, 0))

    # Dessinez les images à côté des boutons
    screen.blit(change_images_left(), (40, 0))

    # Dessiner la boîte de texte semi-transparente en bas
    text_box.draw()

    # Dessiner les boutons
    next_button.draw()

    pygame.display.flip()


def main_Quitter():
    global i
    #show_buttons = False
    pygame.display.set_caption("Bateau sur l'eau")
    # pygame.display.set_icon(icon)

    choix1 = Button(screen_width // 3, 220, screen_width // 3, 50, "Suivre le chien", open_new_window_choix1)

    # Créer une instance de TextBox et définir le texte
    text_box = TextBox(0, 400, screen_width, 200)
    son_Gonfle.play()
    text_box.set_text(" \n  Vous avez pris le bateau, après une heure à souffler dedans pour le gonfler vous\n \n  pouvez enfin prendre la mer")

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
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.rect.collidepoint(event.pos):
                    # Action pour le bouton "Suite >>"
                    if next_button.action:
                        next_button.action()
                        if i == 0:
                            son_Gonfle.stop()
                            text_box.set_new_text("\n  Cependant, une fois éloigné des côtes au point de ne plus les voir vous vous\n \n  rendez compte que le bateau se dégonfle.\n \n  Ce qui vous fait tomber à la mer.")
                            son_Degonfle.play()
                            draw_Nauffrage(text_box, next_button)
                            i += 1
                        elif i == 1:
                            son_Plouf.play()
                            text_box.set_new_text("\n  Cette fois malheureusement vous n’atteindrez pas la terre")
                            son_Degonfle.stop()
                            draw_Nauffrage(text_box, next_button)
                            i += 1
                        elif i == 2:
                            son_Plouf.stop()
                            pygame.mixer.music.stop()
                            i=0
                            open_new_window_choix1()

            pygame.display.flip()

if __name__ == "__main__":
    main_Quitter()

pygame.mixer.music.stop()

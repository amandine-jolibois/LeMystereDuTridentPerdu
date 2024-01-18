import pygame
import sys
from pygame import image, transform
from CroiserFauxAllier import main_CroiserFauxAllier

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
left_images = [image.load("personages\\hero.png"), image.load("personages\\herooff.png"), image.load("personages\\hero.png"), image.load("personages\\hero.png")]
right_images = [image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png"), image.load("personages\\sbire.png"), image.load("personages\\sbireoff.png")]

for i in range(len(left_images)):
    left_images[i] = pygame.transform.scale(left_images[i], (200, 400))
    right_images[i] = pygame.transform.scale(right_images[i], (200, 400))

son_buissons = pygame.mixer.Sound("Son\\Song Part2\\buisson.mp3")
son_buissons.set_volume(0.8)

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

def draw_Nauffrage(text_box, next_button):
    global i
    screen.blit(background_image, (0, 0))

    # Dessinez les images à côté des boutons
    screen.blit(change_images_left(), (40, 0))
    screen.blit(change_images_right(), (560, 60))

    # Dessiner la boîte de texte semi-transparente en bas
    text_box.draw()

    # Dessiner les boutons
    next_button.draw()

    pygame.display.flip()


def main_SeCacher():
    global i
    pygame.display.set_caption(" Chuuuut..")
    # pygame.display.set_icon(icon)

    # Créer une instance de TextBox et définir le texte
    text_box = TextBox(0, 400, screen_width, 200)
    son_buissons.play()
    text_box.set_text(" \n  Des voix… je vais me cacher pour le moment, elles sont peut être hostiles.\n \n  Vous décidez de vous cacher derrière des buissons pour juger les voix,\n \n  voir si elles sont dignes de confiance.")

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
                            text_box.set_new_text("\n  Dépêchez vous de décharger le matériel ! On a pas toute la journée !\n \n  Et prenez des explosifs, si le trident est caché on fait tout pour le trouver !\n \n  Et vérifiez vos armes, si il y a des gêneurs on les traitera comme il se doit !\n \n  Les conventions ne s’appliquent pas sur une île abandonnée.\n \n  A VOS ORDRES CHEF!")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 1:
                            text_box.set_new_text("\n  Une fois le groupe passé vous sortez de votre cachette pour continuer\n \n  le chemin indiqué par la carte.\n \n  Je ferais mieux de ne pas me frotter à ces gens là… Ils n’ont pas l’air commodes…\n \n  En avançant vous sortirez de la forêt pour tomber de nouveau sur une\n \n  plage.")
                            draw_Nauffrage(text_box, next_button)
                        elif i == 2:
                            son_buissons.stop()
                            i = 0
                            main_CroiserFauxAllier()

                        i += 1

            pygame.display.flip()

if __name__ == "__main__":
    main_SeCacher()

pygame.mixer.music.stop()

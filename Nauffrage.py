import pygame
import sys
from pygame import image, transform
from SuivreCarte import main_SuivreCarte
from Sac import main_Sac

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

son_vague = pygame.mixer.Sound("Son\\Environnement\\eau.mp3")
son_vague.set_volume(0.3)

son_pas_Chien = pygame.mixer.Sound("Son\\Chien\\Respiration chien.mp3")
son_pas_Chien.set_volume(0.8)

son_Aboye = pygame.mixer.Sound("Son\\Chien\\aboiement de chien.mp3")
son_Aboye.set_volume(0.4)


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


text_box = TextBox(0, 400, screen_width, 200)

def open_new_window_choix1():
    main_SuivreCarte()
    print("Ouverture d'une nouvelle fenêtre")


def open_new_window_choix2():
    main_Sac()
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

def draw_Nauffrage(choix1, choix2, text_box, next_button):
    global i
    screen.blit(background_image, (0, 0))

    # Dessinez les images à côté des boutons
    screen.blit(change_images_left(), (40, 0))
    screen.blit(change_images_right(), (560, 60))

    # Dessiner la boîte de texte semi-transparente en bas
    text_box.draw()

    # Dessiner les boutons
    if i < 2:
        next_button.draw()

    if i == 2:
        choix1.draw()
        choix2.draw()

    pygame.display.flip()


def main_Nauffrage():
    global i
    son_vague.play()
    #show_buttons = False
    pygame.display.set_caption("Nauffrage")
    # pygame.display.set_icon(icon)

    choix1 = Button(screen_width // 3, 220, screen_width // 3, 50, "Suivre le chien", open_new_window_choix1)
    choix2 = Button(screen_width // 3, 300, screen_width // 3, 50, "Fouiller le sac", open_new_window_choix2)

    # Créer une instance de TextBox et définir le texte
    text_box = TextBox(0, 400, screen_width, 200)
    text_box.set_text(" \n  kof kof…Arghhhh… qu’est ce qu’il s’est passé, où suis-je ?\n \n  La dernière chose dont je me souvienne c’est d'être monté sur un bateau pour\n  partir en croisière… \n  \n  Après c’est le noir complet…")

    next_button = Button(700, 550, 100, 50, "Suite>>", text_box.clear_text)

    running = True

    # Dessiner la boîte de texte
    text_box.draw()

    # Dessiner les boutons et le bouton "Suite >>"
    draw_Nauffrage(choix1, choix2, text_box, next_button)

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
                        son_Aboye.stop()
                        i = 0
                        choix1.action()
                elif choix2.rect.collidepoint(event.pos):
                    # Action pour le bouton "choix2"
                    if choix2.action:
                        son_Aboye.stop()
                        i = 0
                        choix2.action()
                    running = False
                elif next_button.rect.collidepoint(event.pos):
                    # Action pour le bouton "Suite >>"
                    if next_button.action:
                        next_button.action()
                        if i == 0:
                            son_vague.stop()
                            text_box.set_new_text("\n  Un Chien va arriver vers Maïko, il ne semblait montrer aucune hostilité.")
                            son_pas_Chien.play()
                            draw_Nauffrage(choix1, choix2, text_box, next_button)
                        elif i == 1:
                            son_pas_Chien.stop()
                            text_box.set_new_text("\n  Un chien ? Que fait-il ici.")
                            draw_Nauffrage(choix1, choix2, text_box, next_button)
                        elif i == 2:
                            text_box.set_new_text("\n  Le chien aboyait comme s'il voulais qu'il le suive.")
                            son_Aboye.play()
                            draw_Nauffrage(choix1, choix2, text_box, next_button)

                        i += 1

            pygame.display.flip()

if __name__ == "__main__":
    main_Nauffrage()

pygame.mixer.music.stop()

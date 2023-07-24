import pygame
from pygame.locals import *
import sys
import os
from game import GameScene

INITIAL_WIDTH = 1080
INITIAL_HEIGHT = 720

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_SPACING = 40
FONT_SIZE = 40
FONT_COLOR = (255, 255, 255)
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 20

SPRITE_PATH = 'src/sprites/menu.jpg'
LOGO_PATH = 'src/sprites/logo.png'
BUTTON_PAPER_PATH = 'src/sprites/button_paper.png'

RESOLUTIONS = [
    (1920, 720),
    (1080, 720),
]

class Menu:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw(self, surface):
        button_paper = pygame.image.load(BUTTON_PAPER_PATH)
        button_paper = pygame.transform.scale(button_paper, (BUTTON_WIDTH, BUTTON_HEIGHT))
        surface.blit(button_paper, (self.rect.x, self.rect.y))

        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(self.text, True, FONT_COLOR)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

class SettingsMenu:
    def __init__(self):
        self.background = pygame.image.load(SPRITE_PATH)
        self.background = pygame.transform.scale(self.background, (INITIAL_WIDTH, INITIAL_HEIGHT))
        self.logo = pygame.image.load(LOGO_PATH)
        logo_sprite = pygame.image.load(LOGO_PATH)
        self.logo = pygame.transform.scale(logo_sprite, (300, 450))
        
        self.buttons = []
        self.buttons.append(Menu("Submit", INITIAL_WIDTH / 2 + 300 - BUTTON_WIDTH / 2, INITIAL_HEIGHT / 2 + 150 - BUTTON_HEIGHT - BUTTON_SPACING))
        self.buttons.append(Menu("Back", INITIAL_WIDTH / 2 + 300 - BUTTON_WIDTH / 2, INITIAL_HEIGHT / 2 + 100 + BUTTON_SPACING))
        self.slider_rect = pygame.Rect(INITIAL_WIDTH / 2 +200 - SLIDER_WIDTH / 2, INITIAL_HEIGHT / 2  -50 - SLIDER_HEIGHT / 2, SLIDER_WIDTH, SLIDER_HEIGHT)
        self.slider_pos = 0
        self.selected_resolution = RESOLUTIONS[0]

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.logo, (INITIAL_WIDTH / 2 - 370, 135))

        pygame.draw.rect(surface, (150, 150, 150), self.slider_rect)
        pygame.draw.circle(surface, (255, 0, 0), (int(self.slider_rect.x + self.slider_pos), int(self.slider_rect.centery)), 10)

        for button in self.buttons:
            button.draw(surface)

        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(f"Resolution: {self.selected_resolution[0]}x{self.selected_resolution[1]}", True, FONT_COLOR)
        text_rect = text.get_rect(center=(INITIAL_WIDTH / 2 + 200, INITIAL_HEIGHT / 2 -50- BUTTON_SPACING))
        surface.blit(text, text_rect)

    def handle_click(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    if button.text == "Submit":
                        pygame.display.set_mode(self.selected_resolution, RESIZABLE)
                    elif button.text == "Back":
                        return "Menu"  # Go back to the main menu
        elif event.type == MOUSEMOTION and event.buttons[0]:  # Check if the mouse is clicked and moved
            if self.slider_rect.collidepoint(event.pos):
                self.slider_pos = min(max(0, event.pos[0] - self.slider_rect.x), SLIDER_WIDTH)
                slider_steps = len(RESOLUTIONS) - 1
                index = int(round(self.slider_pos / SLIDER_WIDTH * slider_steps))
                self.selected_resolution = RESOLUTIONS[index]

        return "Settings"  # Stay on the settings menu


class JournalMenu:
    def __init__(self):
        self.background = pygame.image.load(SPRITE_PATH)
        self.background = pygame.transform.scale(self.background, (INITIAL_WIDTH, INITIAL_HEIGHT))
        self.sprites = []
        self.load_sprites()

        self.buttons = []
        self.buttons.append(Menu("Back", INITIAL_WIDTH - BUTTON_WIDTH - BUTTON_SPACING - 75, INITIAL_HEIGHT - 90 - BUTTON_HEIGHT - BUTTON_SPACING))

    def load_sprites(self):
        sprite_folder = 'src/sprites/Journal'
        sprite_files = os.listdir(sprite_folder)
        sprite_files = [file for file in sprite_files if file.endswith('.png')]

        for i, sprite_file in enumerate(sprite_files):
            sprite_path = os.path.join(sprite_folder, sprite_file)
            sprite = pygame.image.load(sprite_path)
            sprite = pygame.transform.scale(sprite, (200, 200))
            x = 100 + (i % 2) * 200 + 20
            y = 200 + (i // 2) * 200 - 100
            self.sprites.append((sprite, (x, y)))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        for sprite, pos in self.sprites:
            surface.blit(sprite, pos)

        for button in self.buttons:
            button.draw(surface)


def run():
    pygame.init()
    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), RESIZABLE)
    pygame.display.set_caption("Tavern 21")

    sprite = pygame.image.load(SPRITE_PATH)
    logo_sprite = pygame.image.load(LOGO_PATH)
    logo_sprite = pygame.transform.scale(logo_sprite, (300, 450))

    menu_buttons = []
    menu_buttons.append(Menu("New game", (INITIAL_WIDTH - BUTTON_WIDTH) / 2 + 300, INITIAL_HEIGHT / 2 - BUTTON_HEIGHT - BUTTON_SPACING - 130))
    menu_buttons.append(Menu("Settings", (INITIAL_WIDTH - BUTTON_WIDTH) / 2 + 300, INITIAL_HEIGHT / 2 - 130))
    menu_buttons.append(Menu("Journal", (INITIAL_WIDTH - BUTTON_WIDTH) / 2 + 300, INITIAL_HEIGHT / 2 - 30))
    menu_buttons.append(Menu("Exit", (INITIAL_WIDTH - BUTTON_WIDTH) / 2 + 300, INITIAL_HEIGHT / 2 + BUTTON_HEIGHT + BUTTON_SPACING + 90))

    settings_menu = SettingsMenu()
    journal_menu = JournalMenu()

    current_menu = "Menu"

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)

            if current_menu == "Menu":
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for button in menu_buttons:
                        if button.rect.collidepoint(event.pos):
                            if button.text == "Exit":
                                pygame.quit()
                                sys.exit()
                            elif button.text == "New game":
                                game_scene = GameScene()
                                game_scene.run()
                            elif button.text == "Settings":
                                current_menu = "Settings"
                                screen.fill((0, 0, 0))  # Clear the screen for the new menu
                            elif button.text == "Journal":
                                current_menu = "Journal"
                                screen.fill((0, 0, 0))  # Clear the screen for the new menu

            elif current_menu == "Settings":
                new_menu = settings_menu.handle_click(event)
                if new_menu is not None:
                    current_menu = new_menu
                    screen.fill((0, 0, 0))  # Clear the screen for the new menu

            elif current_menu == "Journal":
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for button in journal_menu.buttons:
                        if button.rect.collidepoint(event.pos) and button.text == "Back":
                            current_menu = "Menu"
                            screen.fill((0, 0, 0))  # Clear the screen for the new menu

        if current_menu == "Menu":
            screen.fill((0, 0, 0))
            screen.blit(pygame.transform.scale(sprite, screen.get_size()), (0, 0))

            logo_rect = logo_sprite.get_rect(center=(INITIAL_WIDTH / 4 + 50, INITIAL_HEIGHT / 2))
            screen.blit(logo_sprite, logo_rect)

            for button in menu_buttons:
                button.draw(screen)

        elif current_menu == "Settings":
            screen.fill((0, 0, 0))
            settings_menu.draw(screen)

        elif current_menu == "Journal":
            journal_menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    run()

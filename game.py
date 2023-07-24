import pygame
import random
from pygame.locals import *
import sys
import os
import re


INITIAL_WIDTH = 1080
INITIAL_HEIGHT = 720

BACKGROUND_IMAGE_PATH = 'src/sprites/background.jpg'
ENEMY_SIZE = (500, 500)

CARD_SPRITES = [
    'src/sprites/Cards/card-diamonds-1.png',
    'src/sprites/Cards/card-diamonds-2.png',
    'src/sprites/Cards/card-diamonds-3.png',
    'src/sprites/Cards/card-diamonds-4.png',
    'src/sprites/Cards/card-diamonds-5.png',
    'src/sprites/Cards/card-diamonds-6.png',
    'src/sprites/Cards/card-diamonds-7.png',
    'src/sprites/Cards/card-diamonds-8.png',
    'src/sprites/Cards/card-diamonds-9.png',
    'src/sprites/Cards/card-diamonds-10.png',
    'src/sprites/Cards/card-diamonds-Q.png',
    'src/sprites/Cards/card-diamonds-K.png',
    'src/sprites/Cards/card-diamonds-J.png'
]

SCROLL_WINDOW_WIDTH = 600
SCROLL_WINDOW_HEIGHT = 50
SCROLL_WINDOW_COLOR = (150, 150, 150)

SCROLL_WINDOW_TEXT_WIN = """I saw this here about a couple of days ago..."""
SCROLL_WINDOW_TEXT_LOOSE = """If life were a deck of cards, then the casino would inevitably take away your tokens!"""

BUTTON_COLOR = (200, 200, 200)
BUTTON_WOOD_PATH = 'src/sprites/button_wood.png'
BUTTON_PAPER_PATH = 'src/sprites/button_paper.png'
BUTTON_PAPER_WIDTH = 250
BUTTON_PAPER_HEIGHT = 50

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80

CARD_SIZE = (80, 120)
CARD_BACK_IMAGE_PATH = 'src/sprites/Cards/card-back-red.png'


def get_random_enemy_sprite():
    enemy_sprites_path = 'src/sprites/Enemys'
    enemy_sprites = os.listdir(enemy_sprites_path)

    matching_sprites_g = [sprite for sprite in enemy_sprites if re.match(r"enemy_g_[1-4]-1\.png", sprite)]
    matching_sprites_m = [sprite for sprite in enemy_sprites if re.match(r"enemy_m_[0-2]\.png", sprite)]

    matching_sprites = matching_sprites_g + matching_sprites_m

    if matching_sprites:
        return os.path.join(enemy_sprites_path, random.choice(matching_sprites))
    else:
        return None

def get_random_win_sprite():
    win_sprites_path = 'src/sprites/Journal'
    win_sprites = os.listdir(win_sprites_path)

    if win_sprites:
        return os.path.join(win_sprites_path, random.choice(win_sprites))
    else:
        return None

def get_next_enemy_sprite(enemy_sprite_path, wins):
    index = 0
    path = 'src/sprites/Enemys/'
    match = re.search(r'\d+', enemy_sprite_path)
    if match:
        index = int(match.group())

    new_enemy_path = "{0}enemy_g_{1}-{2}.png".format(path, index, wins)
    return new_enemy_path

        
class GameScene:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), RESIZABLE)
        pygame.display.set_caption("Tavern 21")

        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)

        self.enemy_image_path = get_random_enemy_sprite()
        self.enemy_image = pygame.transform.scale(pygame.image.load(self.enemy_image_path), ENEMY_SIZE)
        self.enemy_rect = self.enemy_image.get_rect(center=(INITIAL_WIDTH / 2, INITIAL_HEIGHT / 4 + 120))

        self.clock = pygame.time.Clock()

        self.button_paper = pygame.image.load(BUTTON_WOOD_PATH)
        self.button_paper = pygame.transform.scale(self.button_paper, (BUTTON_WIDTH, BUTTON_HEIGHT))

        self.win_image_path = get_random_win_sprite()
        self.win_image = pygame.transform.scale(pygame.image.load(self.win_image_path), ENEMY_SIZE)
        self.win_rect = self.win_image.get_rect(center=(INITIAL_WIDTH / 2, INITIAL_HEIGHT / 4 + 120))

        self.wins = 1   
        self.last_wins = False
        self.ultra_win = False

        self.player_money = 500
        self.enemy_money = 500

        self.is_popup_visible = False
        self.is_result_visible = False

        self.player_cards = []
        self.enemy_cards = []

        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 20)

        self.take_button_rect = None
        self.stand_button_rect = None

        self.current_bet = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit_game()
                elif event.type == VIDEORESIZE:
                    self.handle_resize(event.size)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.is_popup_visible:
                            self.hide_popup()
                        else:
                            self.show_popup()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click(event.pos)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()


            self.screen.blit(pygame.transform.scale(self.background_image, self.screen.get_size()), (0, 0))
            self.screen.blit(self.enemy_image, self.enemy_rect)

            if self.is_popup_visible:
                self.draw_popup()
            elif self.is_result_visible:
                self.draw_result()
            else:
                self.draw_game()

            pygame.display.flip()
            self.clock.tick(60)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_resize(self, size):
        self.screen = pygame.display.set_mode(size, RESIZABLE)

    def handle_mouse_click(self, pos):
        if self.is_popup_visible:
            self.handle_popup_click(pos)
        elif self.is_result_visible:
            self.hide_result()
        else:
            if self.take_button_rect.collidepoint(pos):
                self.take_card()
            elif self.stand_button_rect.collidepoint(pos):
                self.stand()
            elif self.bet_increase_rect.collidepoint(pos):
                self.current_bet += 50
            elif self.bet_decrease_rect.collidepoint(pos):
                self.current_bet = max(0, self.current_bet - 50)

    def show_popup(self):
        self.is_popup_visible = True

    def hide_popup(self):
        self.is_popup_visible = False

    def draw_popup(self):
        button_spacing = 20
        button_x = INITIAL_WIDTH / 2 - BUTTON_PAPER_WIDTH / 2
        button_y = INITIAL_HEIGHT / 2 - BUTTON_PAPER_HEIGHT - button_spacing

        buttons = ["New game", "Continue", "Exit"]

        for button_text in buttons:
            button_rect = pygame.Rect(button_x, button_y, BUTTON_PAPER_WIDTH, BUTTON_PAPER_HEIGHT)
            button_paper = pygame.image.load(BUTTON_PAPER_PATH)
            button_paper = pygame.transform.scale(button_paper, (BUTTON_PAPER_WIDTH, BUTTON_PAPER_HEIGHT))
            self.screen.blit(button_paper, (button_x, button_y))

            text = self.small_font.render(button_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

            button_y += BUTTON_PAPER_HEIGHT + button_spacing

    def handle_popup_click(self, pos):
        button_width = 200
        button_height = 40
        button_spacing = 20
        button_x = INITIAL_WIDTH / 2 - button_width / 2
        button_y = INITIAL_HEIGHT / 2 - button_height - button_spacing

        buttons = ["New game", "Continue", "Exit"]

        for button_text in buttons:
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            if button_rect.collidepoint(pos):
                if button_text == "New game":
                    self.hide_popup()
                    self.restart_game()
                elif button_text == "Continue":
                    self.hide_popup()
                elif button_text == "Exit":
                    self.quit_game()

            button_y += button_height + button_spacing

    @staticmethod
    def text_wrap(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            if font.size(' '.join(current_line + [word]))[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def draw_money(self):
        player_text = self.font.render("Player Money: " + str(self.player_money), True, (255, 255, 255))
        player_text_rect = player_text.get_rect(topleft=(10, INITIAL_HEIGHT - 700))
        self.screen.blit(player_text, player_text_rect)

        enemy_text = self.font.render("Enemy Money: " + str(self.enemy_money), True, (255, 255, 255))
        enemy_text_rect = enemy_text.get_rect(topleft=(10, player_text_rect.bottom + 20))
        self.screen.blit(enemy_text, enemy_text_rect)

    def draw_win_result(self, win_text, scroll_text):
        button_paper = pygame.image.load(BUTTON_PAPER_PATH)
        button_paper = pygame.transform.scale(button_paper, (100, 40))
       
        win_text_surface = self.font.render(win_text, True, (255, 255, 255))
        win_text_rect = win_text_surface.get_rect(center=(INITIAL_WIDTH / 2, INITIAL_HEIGHT / 2))
        self.screen.blit(win_text_surface, win_text_rect)

        scroll_text_surface = self.small_font.render(scroll_text, True, (255, 255, 255))
        scroll_text_rect = scroll_text_surface.get_rect(center=(INITIAL_WIDTH / 2, INITIAL_HEIGHT - 100))
        self.screen.blit(scroll_text_surface, scroll_text_rect)

        next_button_rect = pygame.Rect(INITIAL_WIDTH - 150, INITIAL_HEIGHT - 50, 100, 40)
        self.screen.blit(button_paper, next_button_rect)

        next_text = self.small_font.render("Next", True, (255, 255, 255))
        next_text_rect = next_text.get_rect(center=next_button_rect.center)
        self.screen.blit(next_text, next_text_rect)

        if next_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.restart_game()

    def draw_result(self):
        if self.enemy_money <= 0:
            if "_m_" in self.enemy_image_path:
                self.draw_win_result("Player Win!", SCROLL_WINDOW_TEXT_WIN)
                self.win_image_path = get_random_win_sprite()
                self.screen.blit(self.win_image, self.win_rect)
            else:
                self.draw_win_result("Player Win!", "    ")
        
        elif self.player_money <= 0:
            if "_m_" in self.enemy_image_path:
                self.draw_win_result("Player lost...", SCROLL_WINDOW_TEXT_LOOSE)
            else:
                self.draw_win_result("Player lost...", "    ")
        else:
            player_result_text = self.font.render("Player Result: " + str(self.get_cards_value(self.player_cards)), True, (255, 255, 255))
            player_result_rect = player_result_text.get_rect(topleft=(10, INITIAL_HEIGHT - 160))
            self.screen.blit(player_result_text, player_result_rect)

            enemy_result_text = self.font.render("Enemy Result: " + str(self.get_cards_value(self.enemy_cards)), True, (255, 255, 255))
            enemy_result_rect = enemy_result_text.get_rect(topleft=(10, player_result_rect.bottom + 10))
            self.screen.blit(enemy_result_text, enemy_result_rect)

            result_text, result_color = self.get_game_result_text()
            result_text_surface = self.font.render(result_text, True, result_color)
            result_rect = result_text_surface.get_rect(center=(INITIAL_WIDTH / 2, INITIAL_HEIGHT / 2))
            self.screen.blit(result_text_surface, result_rect)

    def get_game_result_text(self):
        if self.get_cards_value(self.player_cards) > 21:
            self.last_wins = False
            return "Player Bust! Enemy Wins!", (255, 255, 255)
        elif self.get_cards_value(self.enemy_cards) > 21:
            self.last_wins = True
            if "_g_" in self.enemy_image_path:
                self.enemy_image_path = get_next_enemy_sprite(self.enemy_image_path, self.wins)
                self.enemy_image = pygame.transform.scale(pygame.image.load(self.enemy_image_path), ENEMY_SIZE)
                self.screen.blit(self.enemy_image, self.enemy_rect)
            else:
                pass
        
            return "Enemy Bust! Player Wins!", (255, 255, 255)
        elif self.get_cards_value(self.player_cards) > self.get_cards_value(self.enemy_cards):
            self.last_wins = True
            if "_g_" in self.enemy_image_path:
                self.enemy_image_path = get_next_enemy_sprite(self.enemy_image_path, self.wins)
                self.enemy_image = pygame.transform.scale(pygame.image.load(self.enemy_image_path), ENEMY_SIZE)
                self.screen.blit(self.enemy_image, self.enemy_rect)
            else:
                pass

            return "Player Wins!", (255, 255, 255)
        elif self.get_cards_value(self.enemy_cards) > self.get_cards_value(self.player_cards):
            self.last_wins = False
            return "Enemy Wins!", (255, 255, 255)
        else: 
            self.last_wins = False
            return "Draw!", (255, 255, 255)



    def draw_game(self):
        self.draw_money()

        self.draw_player_cards()
        self.draw_enemy_cards()

        self.take_button_rect = pygame.Rect(INITIAL_WIDTH - 220, INITIAL_HEIGHT - 90, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_paper = pygame.image.load(BUTTON_WOOD_PATH)
        button_paper = pygame.transform.scale(button_paper, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.screen.blit(button_paper, (self.take_button_rect.x, self.take_button_rect.y))

        take_button_text = self.font.render("Hit", True, (255, 255, 255))
        take_button_rect = take_button_text.get_rect(center=self.take_button_rect.center)
        self.screen.blit(take_button_text, take_button_rect)

        self.stand_button_rect = pygame.Rect(INITIAL_WIDTH - 220, INITIAL_HEIGHT - 190, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_paper = pygame.image.load(BUTTON_WOOD_PATH)
        button_paper = pygame.transform.scale(button_paper, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.screen.blit(button_paper, (self.stand_button_rect.x, self.stand_button_rect.y))

        stand_button_text = self.font.render("Stand", True, (255, 255, 255))
        stand_button_rect = stand_button_text.get_rect(center=self.stand_button_rect.center)
        self.screen.blit(stand_button_text, stand_button_rect)

        current_bet_text = self.font.render("Current Bet: " + str(self.current_bet), True, (255, 255, 255))
        current_bet_rect = current_bet_text.get_rect(topright=(INITIAL_WIDTH - 10, 10))
        self.screen.blit(current_bet_text, current_bet_rect)

        bet_increase_button_rect = pygame.Rect(INITIAL_WIDTH - 50, 40, 40, 40)
        button_paper = pygame.image.load(BUTTON_WOOD_PATH)
        button_paper = pygame.transform.scale(button_paper, (40, 40))
        self.screen.blit(button_paper, (bet_increase_button_rect.x, bet_increase_button_rect.y))

        bet_increase_text = self.small_font.render("+", True, (255, 255, 255))
        bet_increase_text_rect = bet_increase_text.get_rect(center=bet_increase_button_rect.center)
        self.screen.blit(bet_increase_text, bet_increase_text_rect)
        self.bet_increase_rect = bet_increase_button_rect

        bet_decrease_button_rect = pygame.Rect(INITIAL_WIDTH - 145, 40, 40, 40)
        button_paper = pygame.image.load(BUTTON_WOOD_PATH)
        button_paper = pygame.transform.scale(button_paper, (40, 40))
        self.screen.blit(button_paper, (bet_decrease_button_rect.x, bet_decrease_button_rect.y))

        bet_decrease_text = self.small_font.render("-", True, (255, 255, 255))
        bet_decrease_text_rect = bet_decrease_text.get_rect(center=bet_decrease_button_rect.center)
        self.screen.blit(bet_decrease_text, bet_decrease_text_rect)
        self.bet_decrease_rect = bet_decrease_button_rect

    def draw_player_cards(self):
        player_cards_rect = pygame.Rect(50, INITIAL_HEIGHT - 170, 130, 160)

        x_offset = 10
        for card in self.player_cards:
            card_image = pygame.image.load(card)
            card_image = pygame.transform.scale(card_image, CARD_SIZE)
            self.screen.blit(card_image, (player_cards_rect.left + x_offset, player_cards_rect.top + 20))
            x_offset += 30

    def draw_enemy_cards(self):
        enemy_cards_rect = pygame.Rect(500, 550, 130, 160)

        x_offset = 10
        for card in self.enemy_cards:
            card_image = pygame.image.load(CARD_BACK_IMAGE_PATH)
            card_image = pygame.transform.scale(card_image, CARD_SIZE)
            self.screen.blit(card_image, (enemy_cards_rect.left + x_offset, enemy_cards_rect.top + 20))
            x_offset += 30

    def take_card(self):
        card = random.choice(CARD_SPRITES)
        self.player_cards.append(card)
        self.enemy_cards.append(random.choice(CARD_SPRITES))

    def stand(self):
        while self.get_cards_value(self.enemy_cards) < 17:
            card = random.choice(CARD_SPRITES)
            self.enemy_cards.append(card)

        #self.player_money -= self.current_bet
        #self.enemy_money -= self.current_bet

        if self.get_cards_value(self.player_cards) > self.get_cards_value(self.enemy_cards) or self.get_cards_value(self.enemy_cards) > 21:
            self.player_money += self.current_bet
            self.enemy_money -= self.current_bet
        elif self.get_cards_value(self.enemy_cards) > self.get_cards_value(self.player_cards) or self.get_cards_value(self.player_cards) > 21:
            self.player_money -= self.current_bet
            self.enemy_money += self.current_bet
        else:
            self.player_money += self.current_bet

        
        if self.last_wins:
            if self.wins == 3:
                pass
            else: 
                self.wins = min(max(self.wins + 1, 1), 3)
            
            #if self.enemy_image_path.find("_g_"):
            #    self.enemy_image_path = get_next_enemy_sprite(self.enemy_image_path, self.wins)
            #else:
            #    pass
                    
            #self.enemy_image = pygame.transform.scale(pygame.image.load(self.enemy_image_path), ENEMY_SIZE)
            #self.screen.blit(self.enemy_image, self.enemy_rect)
        else:
            pass

        self.is_result_visible = True

    def get_cards_value(self, cards):
        total_value = 0
        ace_count = 0

        for card in cards:
            rank = card.split("-")[-1].split(".")[0]

            if rank.isdigit():
                total_value += int(rank)
            elif rank in ["K", "Q", "J"]:
                total_value += 10
            elif rank == "A":
                ace_count += 1

        for _ in range(ace_count):
            if total_value + 11 <= 21:
                total_value += 11
            else:
                total_value += 1


        return total_value

    def hide_result(self):
        self.is_result_visible = False

        self.player_cards = []
        self.enemy_cards = []

        self.take_button_rect = None
        self.stand_button_rect = None

    def restart_game(self):
        self.hide_result()

        self.wins = 1
        self.win_image_path = get_random_win_sprite()
        #self.win_image = pygame.transform.scale(pygame.image.load(self.win_image_path), ENEMY_SIZE)
        #self.win_rect = self.win_image.get_rect(center=(INITIAL_WIDTH / 2, INITIAL_HEIGHT / 4 + 120))

        self.enemy_image_path = get_random_enemy_sprite()
        self.enemy_image = pygame.transform.scale(pygame.image.load(self.enemy_image_path), ENEMY_SIZE)
        self.screen.blit(self.enemy_image, self.enemy_rect)

        self.current_bet = 0
        self.player_money = 500
        self.enemy_money = 500


if __name__ == '__main__':
    game_scene = GameScene()
    game_scene.run()

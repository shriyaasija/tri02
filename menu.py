import pygame
import os
from states import State
import tictactoe
import connect4
import isolation

class Menu(State):
    def __init__(self,game):
        self.game = game
        State.__init__(self,game)
        self.grass_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))
        self.menu_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "menu1.png"))
        self.menu_rect = self.menu_img.get_rect()
        
        self.text_mainmenu = self.game.font.render("MAIN MENU", True, (0,0,0))
        self.text_mainmenu_rect = self.text_mainmenu.get_rect(center = (238,50))
        self.text_ttt = self.game.font.render("TicTacToe", True, (0,0,0))
        self.text_ttt_rect = self.text_ttt.get_rect(center = (238,103))
        self.text_connect4 = self.game.font.render("Connect 4", True, (0,0,0))
        self.text_connect4_rect = self.text_connect4.get_rect(center = (238,135))
        self.text_isolation = self.game.font.render("Isolation", True, (0,0,0))
        self.text_isolation_rect = self.text_isolation.get_rect(center = (238,168))
        self.text_exit = self.game.font.render("Exit Game", True, (0,0,0))
        self.text_exit_rect = self.text_exit.get_rect(center=(238,200))

        self.menu_rect.center = (self.game.GAME_W*.5, self.game.GAME_H*.5)
        self.menu_options = {0:"TicTacToe", 1:"Connect4", 2:"Isolation", 3:"Exit"}
        self.index = 0

        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "cursor.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_y = self.menu_rect.y + 40
        self.cursor_rect.x, self.cursor_rect.y = self.menu_rect.x - 43, self.cursor_pos_y

    def update(self, actions):
        self.update_cursor(actions)
        if actions["start"]:
            self.transition_state()
        if actions["back"]:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        display.blit(self.grass_img, (0,0))
        #display.blit(self.menu_img, self.menu_rect)
        display.blit(self.text_mainmenu, self.text_mainmenu_rect)
        display.blit(self.text_ttt, self.text_ttt_rect)
        display.blit(self.text_connect4, self.text_connect4_rect)
        display.blit(self.text_isolation, self.text_isolation_rect)
        display.blit(self.text_exit, self.text_exit_rect)
        display.blit(self.cursor_img, self.cursor_rect)

    def update_cursor(self, actions):
        if actions["down"]:
            self.index = (self.index + 1) % len(self.menu_options)
        elif actions["up"]:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + (self.index * 32)

    def transition_state(self):
        if self.menu_options[self.index] == "TicTacToe":
            tictactoe.main()
        elif self.menu_options[self.index] == "Connect4":
            connect4.main()
        elif self.menu_options[self.index] == "Isolation":
            isolation.main()
        elif self.menu_options[self.index] == "Exit":
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()

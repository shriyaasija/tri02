import pygame
import sys
import time
from pygame.locals import *

draw_tic_tac_toe = None
XO = "x"
ttt_board = [[None]*3, [None]*3, [None]*3]
winner_tic_tac_toe = None

def main():
    WIDTH, HEIGHT = 560, 560
    #XO = "x"
    WHITE = (255,255,255)
    BLACK = (0, 0, 0)


    line_color = (0,0,0)
    winner_tic_tac_toe = None
    draw_tic_tac_toe = None

    def initiate_ttt_board():
        global clock, screen, font
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.Font(None, 40)
        screen.fill(WHITE)

        pygame.draw.line(screen, line_color, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
        pygame.draw.line(screen, line_color, (WIDTH / 3 * 2, 0),
                    (WIDTH / 3 * 2, HEIGHT), 7)

        # drawing horizontal lines
        pygame.draw.line(screen, line_color, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
        pygame.draw.line(screen, line_color, (0, HEIGHT / 3 * 2),
                    (WIDTH, HEIGHT / 3 * 2), 7)
        
        draw_status()

    def draw_status():

        for event in pygame.event.get():
            if(event.type == pygame.MOUSEBUTTONDOWN):
                x, y = pygame.mouse.get_pos()
                user_click(x,y)
        
        pygame.display.update()

    def check_win_tic_tac_toe():
        global ttt_board, winner_tic_tac_toe, draw_tic_tac_toe

        for row in range(0,3):
            if((ttt_board[row][0] == ttt_board[row][1] == ttt_board[row][2]) and (ttt_board[row][0] is not None)):
                winner_tic_tac_toe = ttt_board[row][0]
                pygame.draw.line(screen, (250, 0, 0),(0, (row+1)*HEIGHT / 3 - HEIGHT / 6), (WIDTH, (row+1)*HEIGHT / 3 - HEIGHT / 6), 4)

                break

        for col in range(0,3):
            if ((ttt_board[0][col] == ttt_board[1][col] == ttt_board[2][col]) and ttt_board[0][col] is not None):
                winner_tic_tac_toe = ttt_board[0][col]
                pygame.draw.line(screen, (250, 0, 0), ((col + 1) * WIDTH / 3 - WIDTH / 6, 0),((col + 1) * WIDTH / 3 - WIDTH / 6, HEIGHT), 4)

                break
        
        # check for diagonal winners
        if (ttt_board[0][0] == ttt_board[1][1] == ttt_board[2][2]) and (ttt_board[0][0] is not None):
        
            #game won diagonally left to right
            winner_tic_tac_toe = ttt_board[0][0]
            pygame.draw.line(screen, (250, 70, 70), (90, 100), (467, 467), 4)

        if (ttt_board[0][2] == ttt_board[1][1] == ttt_board[2][0]) and (ttt_board[0][2] is not None):
            #game won diagonally right to left
            winner_tic_tac_toe = ttt_board[0][2]
            pygame.draw.line(screen, (250, 70, 70), (467, 90), (90, 467), 4)

        if (all([all(row) for row in ttt_board]) and winner_tic_tac_toe is None):
            draw_tic_tac_toe = True

        draw_status()

    def drawXO(row, col):
        global ttt_board, XO

        if row == 1:
            posy = 97

        elif row == 2:
            posy = 284

        elif row == 3:
            posy = 466

        if col == 1:
            posx = 90

        elif col == 2:
            posx = 279

        elif col == 3:
            posx = 467

        ttt_board[row-1][col-1] = XO
        print(XO)
        text = font.render(XO, True, BLACK)
        text_rect = text.get_rect(center = (posx, posy))
        screen.blit(text, text_rect)
        pygame.display.update()

        print(ttt_board)

        if XO == "x":
            XO ="o"

        else:
            XO = "x"

        pygame.display.update()

    def user_click(x, y):

            if x < 185 :
                col = 1
            
            elif x < 372:
                col = 2

            elif x < WIDTH:
                col = 3

            else: 
                col = None
            
            if y < 186:
                row = 1

            elif y < 372:
                row = 2

            elif y < HEIGHT:
                row = 3
            
            else:
                row = None


            print(x,y)
            print(row,col)

            if row and col and ttt_board[row-1][col-1] is None:
                drawXO(row,col)
                check_win_tic_tac_toe()

    def reset_tic_tac_toe():
        global ttt_board, winner_tic_tac_toe, XO, draw_tic_tac_toe

        XO = "x"
        draw_tic_tac_toe = False
        winner_tic_tac_toe = None
        ttt_board = [[None]*3, [None]*3, [None]*3]
        initiate_ttt_board()

    initiate_ttt_board()

    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type  == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                print(x,y)
                user_click(x, y)
            if(winner_tic_tac_toe or draw_tic_tac_toe):
                reset_tic_tac_toe()
        pygame.display.update()

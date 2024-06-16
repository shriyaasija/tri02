import pygame
import sys
import math
from pygame.locals import *

chance = "x"
ttt_board = [[None]*3, [None]*3, [None]*3]

def main():

    WIDTH, HEIGHT = 560, 560
    GREEN = (84, 184, 121)
    WHITE = (240, 233, 242)

    line_color = (240, 233, 242)

    def initiate_ttt_board():
        global clock, screen, font, draw_tic_tac_toe, winner_tic_tac_toe
        pygame.init()
        draw_tic_tac_toe = None
        winner_tic_tac_toe = None
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        font = pygame.font.Font(None, 60)
        screen.fill(GREEN)

        #drawing vertical lines
        pygame.draw.line(screen, line_color, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 7)
        pygame.draw.line(screen, line_color, (WIDTH / 3 * 2, 0),
                    (WIDTH / 3 * 2, HEIGHT), 7)

        # drawing horizontal lines
        pygame.draw.line(screen, line_color, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 7)
        pygame.draw.line(screen, line_color, (0, HEIGHT / 3 * 2),
                    (WIDTH, HEIGHT / 3 * 2), 7)
        
        

    def check_win_tic_tac_toe():
        global ttt_board, winner_tic_tac_toe, draw_tic_tac_toe

        #checking horizontal and vertical win
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
            
        #if draw
        if (all([all(row) for row in ttt_board]) and winner_tic_tac_toe is None):
            draw_tic_tac_toe = True


    def drawXO(row, col):
        global ttt_board, chance
        posx = 0

        #row and col poistion to pixel
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

        #updating board
        ttt_board[row-1][col-1] = chance
        text = font.render(chance, True, WHITE)
        text_rect = text.get_rect(center = (posx, posy))
        screen.blit(text, text_rect)
        pygame.display.update()

        #switching chance
        if chance == "x":
            chance ="o"

        else:
            chance = "x"
        pygame.display.update()


    def user_click(x, y):

        #user click to row and col conversion
        
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


        if row and col and ttt_board[row-1][col-1] is None:
            drawXO(row,col)
            check_win_tic_tac_toe()


    def reset_tic_tac_toe():
        global ttt_board, winner_tic_tac_toe, chance, draw_tic_tac_toe
        #resetting variables to restart game
        chance = "x"
        draw_tic_tac_toe = False
        winner_tic_tac_toe = None
        ttt_board = [[None]*3, [None]*3, [None]*3]
        initiate_ttt_board()


    def remainingMoves(board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == None: 
                    return False
        return True

    def check_winner_minimax():
        for row in range(3):
            if(ttt_board[row][0] == ttt_board[row][1] == ttt_board[row][2]):
                return ttt_board[row][0]
            
        for col in range(3):
            if(ttt_board[0][col] == ttt_board[1][col] == ttt_board[2][col]):
                return ttt_board[0][col]
        
        if(ttt_board[0][0] == ttt_board[1][1] == ttt_board[2][2]):
            return ttt_board[0][0]
            
        if(ttt_board[0][2] == ttt_board[1][1] == ttt_board[2][0]):
            return ttt_board[0][2]
        
        return None
            
    def minimax(board, depth, maximizingPlayer):
        winner = check_winner_minimax()
        result = None

        if winner:
            if winner == "o":
                result = 1
            if winner == "x":
                result = -1 
            elif remainingMoves(board) == True:
                result = 0
            else:
                result = None

        if result is not None:
            return result
        
        if maximizingPlayer:
            max_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == None:
                        board[i][j] = "o"

                        score = minimax(board, depth+1, False)
                        if score == -math.inf:
                            score = 1
                        board[i][j] = None

                        max_score = max(max_score, score)
            
            return max_score
        
        else:
            min_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == None:
                        board[i][j] = "x"

                        score = minimax(board, depth+1, True)
                        if score == -math.inf:
                            score = 0
                        board[i][j] = None

                        min_score = min(min_score, score)
            
            return min_score

    def winning_move():
        global ttt_board
        best_score = -math.inf
        best_move = (-2,-2)
        #b_copy = copy.deepcopy(board)

        for i in range(3):
            for j in range(3):
                if ttt_board[i][j] == None:
                    ttt_board[i][j] = "o"
            
                    val = minimax(ttt_board, 0, False)
                    ttt_board[i][j] = None

                    if val > best_score:
                        best_move = (i, j)
                        best_score = val

        return best_move
    
    initiate_ttt_board()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                game_over = True
                sys.exit()
            elif event.type  == pygame.MOUSEBUTTONDOWN:
                if chance == "x":
                    x,y = pygame.mouse.get_pos()
                    user_click(x, y)
                    
                if(winner_tic_tac_toe or draw_tic_tac_toe):
                    game_over = True
            
        if chance == "o" and not game_over:
            move = winning_move()
            if move:
                row, col = move
                drawXO(row+1,col+1)
                check_win_tic_tac_toe()
            
        if winner_tic_tac_toe or draw_tic_tac_toe:
            game_over = True
            
        pygame.display.update()


        if game_over:
            pygame.time.wait(3000)
            reset_tic_tac_toe()
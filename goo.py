import random, pygame, sys
from pygame.locals import *

FPS = 30  
width = 430 
heigth = 500  
BOXSIZE = 50  
GAPSIZE = 10  
BOARDWIDTH = 7
BOARDHEIGHT = 7

darkblue = (69,97,163)
lightblue = (123,155,179)

green = (30,110,47)
black = (0, 0, 0)
white = (255,255,255)

BGCOLOR = lightblue
BOXCOLOR = darkblue
LINECOLOR = lightblue
LEGALCOLOR = green
LASTCOLOR = black
LASTCOLOR2 = white

O = 'O'
X = 'X'


def possible_move(board, r, c):
    if r < 0 or r >= BOARDWIDTH:
        return False
    if c < 0 or c >= BOARDWIDTH:
        return False
    if board[r][c] != 'b':
        return False

    return True


def legal_moves(board, move):
    r, c = move
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions if possible_move(board, r + dr, c + dc)]

    return valid_moves


legal_moves_O = []
legal_moves_X = []


def main():
    global clock, screen
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, heigth))

    mouse_x = 0  # used to store x coordinate of mouse event
    mouse_y = 0  # used to store y coordinate of mouse event
    pygame.display.set_caption('Game: Isolation')

    mainBoard = [['b' for x in range(BOARDHEIGHT)] for y in range(BOARDWIDTH)]
    playerTurn = 'O'
    legal_moves_O = [(r, c) for r in range(BOARDWIDTH) for c in range(BOARDHEIGHT)]
    legal_moves_X = []
    firstSelection = None  # stores the (x, y) of the first box clicked.
    move_cnt = 0

    screen.fill(BGCOLOR)
    drawBoard(mainBoard, playerTurn)
    drawStatus(playerTurn)
    move_cnt = 0

    last_move_X = None
    last_move_O = None

    while True:  # main body
        mouseClicked = False

        screen.fill(BGCOLOR)
        if playerTurn == 'O':
            drawBoard(mainBoard, 'O', legal_moves_O, last_move_O, last_move_X)
            drawStatus('O', move_cnt, len(legal_moves_O) == 0)
        else:
            drawBoard(mainBoard, 'O', legal_moves_X, last_move_X, last_move_O)
            drawStatus('X', move_cnt, len(legal_moves_X) == 0)


        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClicked = True    
            

        box_x, box_y = getBoxAtPixel(mouse_x, mouse_y)
        if box_x != None and box_y != None:
            if mainBoard[box_x][box_y] == 'b' and mouseClicked:
                if playerTurn == 'O' and (box_x, box_y) in legal_moves_O:
                    mainBoard[box_x][box_y] = playerTurn
                    if move_cnt == 0:
                        legal_moves_X = legal_moves_O.copy()
                        legal_moves_X.remove((box_x, box_y))
                    else:
                        legal_moves_X = legal_moves(mainBoard, last_move_X)
                    legal_moves_O = legal_moves(mainBoard, (box_x, box_y))
                    last_move_O = (box_x, box_y)
                elif playerTurn == 'X' and (box_x, box_y) in legal_moves_X:
                    mainBoard[box_x][box_y] = playerTurn
                    legal_moves_X = legal_moves(mainBoard, (box_x, box_y))
                    last_move_X = (box_x, box_y)
                    legal_moves_O = legal_moves(mainBoard, last_move_O)
                else:
                    continue
                drawXO(playerTurn, box_x, box_y)

                move_cnt += 1
                if playerTurn == 'X':
                    playerTurn = 'O'
                else:
                    playerTurn = 'X'

        pygame.display.update()
        clock.tick(FPS)


def getBoxAtPixel(x, y): # Draw Box on display surface    
    for box_x in range(BOARDWIDTH):
        for box_y in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (box_x, box_y)
    return (None, None)

def drawStatus(PlayerTurn, count = 0, lose = False):
    left, top = leftTopCoordsOfBox(0, BOARDHEIGHT)
    myfont = pygame.font.SysFont(None, 24)
    turnstr = PlayerTurn + "'s turn"
    label = myfont.render(turnstr, 1, (0, 0, 0))
    screen.blit(label, (left, top))

    cntstr = "Count: " + str(count)
    labelcnt = myfont.render(cntstr, 1, (0, 0, 0))
    screen.blit(labelcnt, (left, top + 25))

    if lose == True:
        losestr = PlayerTurn + " lost :(((("
        labellose = myfont.render(losestr, 1, (200, 0, 0))
        screen.blit(labellose, (left, top + 50))

    left, top = leftTopCoordsOfBox(2, BOARDHEIGHT)
    redstr = "Green: Possible move"
    labelred = myfont.render(redstr, 1, LEGALCOLOR)
    screen.blit(labelred, (left, top))

    greenstr = "Black: Your last position"
    labelgreen = myfont.render(greenstr, 1, LASTCOLOR)
    screen.blit(labelgreen, (left, top + 25))


def drawBoard(board, playerTurn, legal_moves=[], last_move_own=None, last_move_opp=None):
    # Draws all of the boxes in their covered or revealed state.
    
    for box_x in range(BOARDWIDTH):
        for box_y in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(box_x, box_y)
            if (box_x, box_y) == last_move_own:
                pygame.draw.rect(screen, LASTCOLOR, (left, top, BOXSIZE, BOXSIZE))
                drawXO(board[box_x][box_y], box_x, box_y)
                continue
            elif (box_x, box_y) == last_move_opp:
                pygame.draw.rect(screen, LASTCOLOR2, (left, top, BOXSIZE, BOXSIZE))
                drawXO(board[box_x][box_y], box_x, box_y)
                continue

            if board[box_x][box_y] == 'b':
                if (box_x, box_y) in legal_moves:
                    pygame.draw.rect(screen, LEGALCOLOR, (left, top, BOXSIZE, BOXSIZE))
                else:
                    pygame.draw.rect(screen, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                pygame.draw.rect(screen, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
                drawXO(board[box_x][box_y], box_x, box_y)


def leftTopCoordsOfBox(box_x, box_y): # Convert board coordinates to pixel
    left = box_x * (BOXSIZE + GAPSIZE) + GAPSIZE
    top = box_y * (BOXSIZE + GAPSIZE) + GAPSIZE
    return (left, top)

def drawXO(playerTurn, box_x, box_y):
    left, top = leftTopCoordsOfBox(box_x, box_y)
    if playerTurn == 'X':
        pygame.draw.line(screen, LINECOLOR, (left + 3, top + 3), (left + BOXSIZE - 3, top + BOXSIZE - 3), 4)
        pygame.draw.line(screen, LINECOLOR, (left + BOXSIZE - 3, top + 3), (left + 3, top + BOXSIZE - 3), 4)
    elif playerTurn == 'O':
        HALF = int(BOXSIZE / 2)
        pygame.draw.circle(screen, LINECOLOR, (left + HALF, top + HALF), HALF - 3, 4)


def hasWon(board):# Returns True if player 1 or 2 wins
    return True


def hasDraw(board):# Returns True if all the boxes have been filled
    for i in board:
        if None in i:
            return False
    return True


if __name__ == '__main__':
    main()
import pygame, sys
from random import randint
from tile import Tile
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 1000
WINDOWHEIGHT = 800
REVEALSPEED = 8  # speed boxes' sliding reveals and covers
BOXSIZE = 30
GAPSIZE = 10
BOARDWIDTH = 16
BOARDHEIGHT = 16
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
NUMMINES = 40

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
BURGUNDY = (128, 0, 32)
BLACK = (0, 0, 0)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

BOMB = 'bomb'

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    pygame.display.set_caption('Minesweeper')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    flaggedBoxes = generateFlaggedBoxesData(False)

    DISPLAYSURF.fill(BGCOLOR)

    run = True
    win = True

    while run:  # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)  # drawing the window
        drawBoard(mainBoard, revealedBoxes, flaggedBoxes)
        selection = 0
        mouseLeftClicked = False
        mouseRightClicked = False

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if event.button == 3:
                    mouseRightClicked = True
                else:
                    mouseLeftClicked = True
            elif selection != 0 and selection == True:
                pygame.quit()
                sys.exit()

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseLeftClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True  # set the box as "revealed"
                selection = mainBoard[boxx][boxy].getMine()
                if selection:
                    revealedBoxes = gameOverAnimation(revealedBoxes)
                    win = False
                revealedBoxes = checkBox(mainBoard, revealedBoxes, boxx, boxy)
            if not flaggedBoxes[boxx][boxy] and not revealedBoxes[boxx][boxy] and mouseRightClicked:
                drawFlag(boxx, boxy)
                flaggedBoxes[boxx][boxy] = True
            elif hasWon(mainBoard, revealedBoxes) and win:
                gameWonAnimation(mainBoard)
                pygame.time.wait(2000)

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomizedBoard():
    # Return a list with all the values of the position of each bomb.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            if randint(1, 101) < 16:
                block = Tile(True, 0)
            else:
                block = Tile(False, 0)
            column.append(block)
        board.append(column)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            num = 0
            if board[x][y].getMine() == True:
                num = 0
            elif x == 0 and y == 0:
                if board[1][0].getMine() == True:
                    num += 1
                if board[0][1].getMine() == True:
                    num += 1
                if board[1][1].getMine() == True:
                    num += 1
            elif x == 0 and y == BOARDHEIGHT - 1:
                if board[0][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
                if board[1][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
                if board[1][BOARDHEIGHT - 1].getMine() == True:
                    num += 1
            elif y == 0 and x == BOARDWIDTH - 1:
                if board[BOARDWIDTH - 2][0].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 2][1].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 1][1].getMine() == True:
                    num += 1
            elif y == BOARDHEIGHT - 1 and x == BOARDWIDTH - 1:
                if board[BOARDWIDTH - 2][BOARDHEIGHT - 1].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 2][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 1][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
            elif x == 0:
                if board[0][y - 1].getMine() == True:
                    num += 1
                if board[1][y - 1].getMine() == True:
                    num += 1
                if board[1][y].getMine() == True:
                    num += 1
                if board[1][y + 1].getMine() == True:
                    num += 1
                if board[0][y + 1].getMine() == True:
                    num += 1
            elif x == BOARDWIDTH - 1:
                if board[BOARDWIDTH - 1][y - 1].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 2][y - 1].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 2][y].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 2][y + 1].getMine() == True:
                    num += 1
                if board[BOARDWIDTH - 1][y + 1].getMine() == True:
                    num += 1
            elif y == 0:
                if board[x - 1][0].getMine() == True:
                    num += 1
                if board[x - 1][1].getMine() == True:
                    num += 1
                if board[x][1].getMine() == True:
                    num += 1
                if board[x + 1][1].getMine() == True:
                    num += 1
                if board[x + 1][0].getMine() == True:
                    num += 1
            elif y == BOARDHEIGHT - 1:
                if board[x - 1][BOARDHEIGHT - 1].getMine() == True:
                    num += 1
                if board[x - 1][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
                if board[x][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
                if board[x + 1][BOARDHEIGHT - 2].getMine() == True:
                    num += 1
                if board[x + 1][BOARDHEIGHT - 1].getMine() == True:
                    num += 1
            else:
                if board[x - 1][y - 1].getMine() == True:
                    num += 1
                if board[x][y - 1].getMine() == True:
                    num += 1
                if board[x + 1][y - 1].getMine() == True:
                    num += 1
                if board[x + 1][y].getMine() == True:
                    num += 1
                if board[x + 1][y + 1].getMine() == True:
                    num += 1
                if board[x][y + 1].getMine() == True:
                    num += 1
                if board[x - 1][y + 1].getMine() == True:
                    num += 1
                if board[x - 1][y].getMine() == True:
                    num += 1
            board[x][y].changeNumber(num)
    return board


def drawBoard(board, revealed, flagged):
    # Draws all of the boxes in their covered, revealed, or flagged state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy] and not flagged[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            elif revealed[boxx][boxy]:
                # Draw the (revealed) icon.
                mine = board[boxx][boxy].getMine()
                number = board[boxx][boxy].getNumber()
                drawIcon(mine, number, boxx, boxy)
            else:
                # Draw the flagged box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
                drawFlag(boxx, boxy)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

def generateFlaggedBoxesData(val):
    flaggedBoxes = []
    for i in range(BOARDWIDTH):
        flaggedBoxes.append([val] * BOARDHEIGHT)
    return flaggedBoxes


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        mine = board[box[0]][box[1]].getMine()
        number = board[box[0]][box[1]].getNumber()
        drawIcon(mine, number, box[0], box[1])
        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def drawIcon(bom, numb, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)  # get pixel coords from board coords
    # Draw the shapes
    if bom:
        pygame.draw.circle(DISPLAYSURF, BLACK, (left + half, top + half), half - 5)
    if numb == 1:
        one = pygame.image.load("number1.png")
        one = pygame.transform.scale(one, (20, 20))
        DISPLAYSURF.blit(one, (left, top))
    if numb == 2:
        two = pygame.image.load("number2.png")
        two = pygame.transform.scale(two, (20, 20))
        DISPLAYSURF.blit(two, (left, top))
    if numb == 3:
        three = pygame.image.load("number3.png")
        three = pygame.transform.scale(three, (20, 20))
        DISPLAYSURF.blit(three, (left, top))
    if numb == 4:
        four = pygame.image.load("number4.png")
        four = pygame.transform.scale(four, (20, 20))
        DISPLAYSURF.blit(four, (left, top))
    if numb == 5:
        five = pygame.image.load("number5.png")
        five = pygame.transform.scale(five, (20, 20))
        DISPLAYSURF.blit(five, (left, top))
    if numb == 6:
        six = pygame.image.load("number6.png")
        six = pygame.transform.scale(six, (20, 20))
        DISPLAYSURF.blit(six, (left, top))
    if numb == 7:
        seven = pygame.image.load("number7.png")
        seven = pygame.transform.scale(seven, (20, 20))
        DISPLAYSURF.blit(seven, (left, top))
    if numb == 8:
        eight = pygame.image.load("number8.png")
        eight = pygame.transform.scale(eight, (20, 20))
        DISPLAYSURF.blit(eight, (left, top))

def drawFlag(boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)  # get pixel coords from board coords
    # Draw the flag
    pygame.draw.line(DISPLAYSURF, BLACK, (left + half, top), (left + half, top + BOXSIZE), 2)
    pygame.draw.polygon(DISPLAYSURF, RED, ((left + half, top), (left + quarter, top + BOXSIZE - quarter), (left + half, top + half)), quarter)

def checkBox(board, revealed, x, y):
    if x == 0 and y == 0 and board[0][0].getNumber() == 0 and board[0][0].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[1][0] == True
        revealed[0][1] == True
        revealed[1][1] == True
        if board[1][0].getNumber == 0 and board[1][0].getExpand() == False:
            revealed = checkBox(board, revealed, 1, 0)
        if board[0][1].getNumber == 0 and board[0][1].getExpand() == False:
            revealed = checkBox(board, revealed, 0, 1)
        if board[1][1].getNumber == 0 and board[1][1].getExpand() == False:
            revealed = checkBox(board, revealed, 1, 1)
    elif x == 0 and y == BOARDHEIGHT - 1 and board[0][BOARDHEIGHT - 1].getNumber() == 0 and board[0][BOARDHEIGHT - 1].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[0][BOARDHEIGHT - 2] = True
        revealed[1][BOARDHEIGHT - 2] = True
        revealed[1][BOARDHEIGHT - 1] = True
        if board[0][BOARDHEIGHT - 2].getNumber() == 0 and board[0][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, 0, BOARDHEIGHT - 2)
        if board[1][BOARDHEIGHT - 2].getNumber() == 0 and board[1][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, 1, BOARDHEIGHT - 2)
        if board[1][BOARDHEIGHT - 1].getNumber() == 0 and board[1][BOARDHEIGHT - 1].getExpand() == False:
            revealed = checkBox(board, revealed, 1, BOARDHEIGHT - 1)
    elif y == 0 and x == BOARDWIDTH - 1 and board[BOARDWIDTH - 1][0].getNumber() == 0 and board[BOARDWIDTH - 1][0].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[BOARDWIDTH - 2][0] = True
        revealed[BOARDWIDTH - 2][1] = True
        revealed[BOARDWIDTH - 1][1] = True
        if board[BOARDWIDTH - 2][0].getNumber() == 0 and board[BOARDWIDTH - 2][0].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, 0)
        if board[BOARDWIDTH - 2][1].getNumber() == 0 and board[BOARDWIDTH - 2][1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, 1)
        if board[BOARDWIDTH - 1][1].getNumber() == 0 and board[BOARDWIDTH - 1][1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 1, 1)
    elif y == BOARDHEIGHT - 1 and x == BOARDWIDTH - 1 and board[BOARDWIDTH - 1][BOARDHEIGHT - 1].getNumber() == 0 and board[BOARDWIDTH - 1][BOARDHEIGHT - 1].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[BOARDWIDTH - 2][BOARDHEIGHT - 1] = True
        revealed[BOARDWIDTH - 2][BOARDHEIGHT - 2] = True
        revealed[BOARDWIDTH - 1][BOARDHEIGHT - 2] = True
        if board[BOARDWIDTH - 2][BOARDHEIGHT - 1].getNumber() == 0 and board[BOARDWIDTH - 2][BOARDHEIGHT - 1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, BOARDHEIGHT - 1)
        if board[BOARDWIDTH - 2][BOARDHEIGHT - 2].getNumber() == 0 and board[BOARDWIDTH - 2][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, BOARDHEIGHT - 2)
        if board[BOARDWIDTH - 1][BOARDHEIGHT - 2].getNumber() == 0 and board[BOARDWIDTH - 1][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 1, BOARDHEIGHT - 2)
    elif x == 0 and board[0][y].getNumber() == 0 and board[0][y].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[0][y - 1] = True
        revealed[1][y - 1] = True
        revealed[1][y] = True
        revealed[1][y + 1] = True
        revealed[0][y + 1] = True
        if board[0][y - 1].getNumber() == 0 and board[0][y - 1].getExpand() == False:
            revealed = checkBox(board, revealed, 0, y - 1)
        if board[1][y - 1].getNumber() == 0 and board[1][y - 1].getExpand() == False:
            revealed = checkBox(board, revealed, 1, y - 1)
        if board[1][y].getNumber() == 0 and board[1][y].getExpand() == False:
            revealed = checkBox(board, revealed, 1, y)
        if board[1][y + 1].getNumber() == 0 and board[1][y + 1].getExpand() == False:
            revealed = checkBox(board, revealed, 1, y + 1)
        if board[0][y + 1].getNumber() == 0 and board[0][y + 1].getExpand() == False:
            revealed = checkBox(board, revealed, 0, y + 1)
    elif x == BOARDWIDTH - 1 and board[BOARDWIDTH - 1][y].getNumber() == 0 and board[BOARDWIDTH - 1][y].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[BOARDWIDTH - 1][y - 1] = True
        revealed[BOARDWIDTH - 2][y - 1] = True
        revealed[BOARDWIDTH - 2][y] = True
        revealed[BOARDWIDTH - 2][y + 1] = True
        revealed[BOARDWIDTH - 1][y + 1] = True
        if board[BOARDWIDTH - 1][y - 1].getNumber() == 0 and board[BOARDWIDTH - 1][y - 1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 1, y - 1)
        if board[BOARDWIDTH - 2][y - 1].getNumber() == 0 and board[BOARDWIDTH - 2][y - 1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, y - 1)
        if board[BOARDWIDTH - 2][y].getNumber() == 0 and board[BOARDWIDTH - 2][y].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, y)
        if board[BOARDWIDTH - 2][y + 1].getNumber() == 0 and board[BOARDWIDTH - 2][y + 1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 2, y + 1)
        if board[BOARDWIDTH - 1][y + 1].getNumber() == 0 and board[BOARDWIDTH - 1][y + 1].getExpand() == False:
            revealed = checkBox(board, revealed, BOARDWIDTH - 1, y + 1)
    elif y == 0 and board[x][0].getNumber() == 0 and board[x][0].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[x - 1][0] = True
        revealed[x - 1][1] = True
        revealed[x][1] = True
        revealed[x + 1][1] = True
        revealed[x + 1][0] = True
        if board[x - 1][0].getNumber() == 0 and board[x - 1][0].getExpand() == False:
            revealed = checkBox(board, revealed, x - 1, 0)
        if board[x - 1][1].getNumber() == 0 and board[x - 1][1].getExpand() == False:
            revealed = checkBox(board, revealed, x - 1, 1)
        if board[x][1].getNumber() == 0 and board[x][1].getExpand() == False:
            revealed = checkBox(board, revealed, x, 1)
        if board[x + 1][1].getNumber() == 0 and board[x + 1][1].getExpand() == False:
            revealed = checkBox(board, revealed, x + 1, 1)
        if board[x + 1][0].getNumber() == 0 and board[x + 1][0].getExpand() == False:
            revealed = checkBox(board, revealed, x + 1, 0)
    elif y == BOARDHEIGHT - 1 and board[x][BOARDHEIGHT - 1].getNumber() == 0 and board[x][BOARDHEIGHT - 1].getMine() == False:
        board[x][y].changeExpand(True)
        revealed[x - 1][BOARDHEIGHT - 1] = True
        revealed[x - 1][BOARDHEIGHT - 2] = True
        revealed[x][BOARDHEIGHT - 2] = True
        revealed[x + 1][BOARDHEIGHT - 2] = True
        revealed[x + 1][BOARDHEIGHT - 1] = True
        if board[x - 1][BOARDHEIGHT - 1].getNumber() == 0 and board[x - 1][BOARDHEIGHT - 1].getExpand() == False:
            revealed = checkBox(board, revealed, x - 1, BOARDHEIGHT - 1)
        if board[x - 1][BOARDHEIGHT - 2].getNumber() == 0 and board[x - 1][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, x - 1, BOARDHEIGHT - 2)
        if board[x][BOARDHEIGHT - 2].getNumber() == 0 and board[x][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, x, BOARDHEIGHT - 2)
        if board[x + 1][BOARDHEIGHT - 2].getNumber() == 0 and board[x + 1][BOARDHEIGHT - 2].getExpand() == False:
            revealed = checkBox(board, revealed, x + 1, BOARDHEIGHT - 2)
        if board[x + 1][BOARDHEIGHT - 1].getNumber() == 0 and board[x + 1][BOARDHEIGHT - 1].getExpand() == False:
            revealed = checkBox(board, revealed, x + 1, BOARDHEIGHT - 1)
    else:
        if board[x][y].getNumber() == 0 and board[x][y].getMine() == False:
            board[x][y].changeExpand(True)
            revealed[x- 1][y - 1] = True
            revealed[x][y- 1] = True
            revealed[x + 1][y - 1] = True
            revealed[x + 1][y] = True
            revealed[x + 1][y + 1] = True
            revealed[x][y + 1] = True
            revealed[x - 1][y + 1] = True
            revealed[x - 1][y] = True
            if board[x - 1][y - 1].getNumber() == 0 and board[x- 1][y - 1].getExpand() == False:
                revealed = checkBox(board, revealed, x - 1, y - 1)
            if board[x][y - 1].getNumber() == 0 and board[x][y- 1].getExpand() == False:
                revealed = checkBox(board, revealed, x, y - 1)
            if board[x + 1][y - 1].getNumber() == 0 and board[x + 1][y - 1].getExpand() == False:
                revealed = checkBox(board, revealed, x + 1, y - 1)
            if board[x + 1][y].getNumber() == 0 and board[x + 1][y].getExpand() == False:
                revealed = checkBox(board, revealed, x + 1, y)
            if board[x + 1][y + 1].getNumber() == 0 and board[x + 1][y + 1].getExpand() == False:
                revealed = checkBox(board, revealed, x + 1, y + 1)
            if board[x][y + 1].getNumber() == 0 and board[x][y + 1].getExpand() == False:
                revealed = checkBox(board, revealed, x, y + 1)
            if board[x - 1][y + 1].getNumber() == 0 and board[x - 1][y + 1].getExpand() == False:
                revealed = checkBox(board, revealed, x - 1, y + 1)
            if board[x - 1][y].getNumber() == 0 and board[x - 1][y].getExpand() == False:
                revealed = checkBox(board, revealed, x - 1, y)
    return revealed

def hasWon(board, revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if not revealedBoxes[x][y] and not board[x][y].getMine():
                return False
    return True

def gameOverAnimation(revealed):
    pygame.draw.line(DISPLAYSURF, RED, (0, 0), (1000, 800), 5)
    pygame.draw.line(DISPLAYSURF, RED, (0, 800), (1000, 0), 5)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            revealed[boxx][boxy] = True
    return revealed

def gameWonAnimation(board):
    pygame.draw.line(DISPLAYSURF, GREEN, (0, 400), (500, 800), 5)
    pygame.draw.line(DISPLAYSURF, GREEN, (500, 800), (1000, 0), 5)

if __name__ == '__main__':
    main()
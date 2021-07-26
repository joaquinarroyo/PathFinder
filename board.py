import pygame, time
from data import *

# module -> Path finding board

# initializes the board
def get_board(init, final):
    board = {}
    for x in range(0, int(SIZE[0]/SQUARE_L)):
        for y in range(0, int(SIZE[1]/SQUARE_L)):
            if x == 0 or (x == int(SIZE[0]/SQUARE_L) - 1) or y == 0 or (y == int(SIZE[1]/SQUARE_L) - 1):
                board[(x, y)] = WALL
            elif x == init[0] and y == init[1]:
                board[(x, y)] = INIT
            elif x == final[0] and y == final[1]:
                board[(x, y)] = FINAL
            else:
                board[(x, y)] = NULL
    return board

# draws the grid
def draw_grid(height, width, board, screen):
    for x in range(0, int(SIZE[0]/SQUARE_L)):
        for y in range(0, int(SIZE[1]/SQUARE_L)):
            r = board.get((x, y))
            if r == NULL:
                pygame.draw.rect(screen, BLACK, [height, width, SQUARE_L, SQUARE_L], 1)
            elif r == INIT: 
                pygame.draw.rect(screen, C_INIT, [height, width, SQUARE_L, SQUARE_L], 0)
                pygame.draw.rect(screen, BLACK, [height, width, SQUARE_L, SQUARE_L], 1)
            elif r == FINAL:
                pygame.draw.rect(screen, C_FINAL, [height, width, SQUARE_L, SQUARE_L], 0)
                pygame.draw.rect(screen, BLACK, [height, width, SQUARE_L, SQUARE_L], 1)
            elif r == WALL:
                pygame.draw.rect(screen, C_WALL, [height, width, SQUARE_L, SQUARE_L], 0)
                pygame.draw.rect(screen, BLACK, [height, width, SQUARE_L, SQUARE_L], 1)
            width += SQUARE_L
        width = 0
        height += SQUARE_L

# draws a wall in (x_10, y_10)
def draw_wall(x, y, board, screen, init, final):
    x -= x % SQUARE_L
    y -= y % SQUARE_L
    x_10 = int(x/SQUARE_L)
    y_10 = int(y/SQUARE_L)
    if (x_10, y_10) != init and (x_10, y_10) != final:
        if x < SIZE[0]-1 and x > 0 and y < SIZE[1]-1 and y > 0:
            pygame.draw.rect(screen, C_WALL, [x, y, SQUARE_L, SQUARE_L], 0)
            pygame.draw.rect(screen, BLACK, [x, y, SQUARE_L, SQUARE_L], 1)
            pygame.display.update()
            board[(x_10, y_10)] = WALL
    return board

# draws the start cell and erase the previous one
def draw_init(x, y, board, screen, init, final):
    x -= x % SQUARE_L
    y -= y % SQUARE_L
    x1_10 = int(x/SQUARE_L)
    y1_10 = int(y/SQUARE_L)
    x2_10 = init[0]*SQUARE_L
    y2_10 = init[1]*SQUARE_L
    if (x1_10, y1_10) != init and (x1_10, y1_10) != final:
        if x < SIZE[0]-1 and x > 0 and y < SIZE[1]-1 and y > 0:
            pygame.draw.rect(screen, C_INIT, [x, y, SQUARE_L, SQUARE_L], 0)
            pygame.draw.rect(screen, BLACK, [x, y, SQUARE_L, SQUARE_L], 1)
            pygame.draw.rect(screen, GREY, [x2_10, y2_10, SQUARE_L, SQUARE_L], 0)
            pygame.draw.rect(screen, BLACK, [x2_10, y2_10, SQUARE_L, SQUARE_L], 1)
            pygame.display.update()
            board[(init[0], init[1])] = NULL
            board[(x1_10, y1_10)] = INIT
    return board

# draws the end cell and erase the previous one
def draw_end(x, y, board, screen, init, final):
    x -= x % SQUARE_L
    y -= y % SQUARE_L
    x1_10 = int(x/SQUARE_L)
    y1_10 = int(y/SQUARE_L)
    x2_10 = final[0]*SQUARE_L
    y2_10 = final[1]*SQUARE_L
    if (x1_10, y1_10) != init and (x1_10, y1_10) != final:
        if x < SIZE[0]-1 and x > 0 and y < SIZE[1]-1 and y > 0:
            pygame.draw.rect(screen, C_FINAL, [x, y, SQUARE_L, SQUARE_L], 0)
            pygame.draw.rect(screen, BLACK, [x, y, SQUARE_L, SQUARE_L], 1)
            pygame.draw.rect(screen, GREY, [x2_10, y2_10, SQUARE_L, SQUARE_L], 0)
            pygame.draw.rect(screen, BLACK, [x2_10, y2_10, SQUARE_L, SQUARE_L], 1)
            pygame.display.update()
            board[(final[0], final[1])] = NULL
            board[(x1_10, y1_10)] = FINAL
    return board

# erase a wall in (x_10, y_10)
def erase_wall(x, y, board, screen, init, final):
    x -= x % SQUARE_L
    y -= y % SQUARE_L
    x_10 = int(x/SQUARE_L)
    y_10 = int(y/SQUARE_L)
    if (x_10, y_10) != init and (x_10, y_10) != final:
        if x < SIZE[0] and x > 0 and y < SIZE[1] and y > 0 and x_10 < int(SIZE[0]/SQUARE_L)-1 and y_10 < int(SIZE[1]/SQUARE_L)-1:
            pygame.draw.rect(screen, GREY, [x, y, SQUARE_L, SQUARE_L], 0)
            pygame.draw.rect(screen, BLACK, [x, y, SQUARE_L, SQUARE_L], 1)
            pygame.display.update()
            board[(x_10, y_10)] = NULL
    return board

# draws all the potential paths
def draw_square(x, y, screen, init, final, color):
    x_10 = int(x*SQUARE_L)
    y_10 = int(y*SQUARE_L)
    if (x, y) != init and (x, y) != final:
        pygame.draw.rect(screen, color, [x_10, y_10, SQUARE_L, SQUARE_L], 0)
        pygame.draw.rect(screen, BLACK, [x_10, y_10, SQUARE_L, SQUARE_L], 1)
        pygame.display.update()

# draws the path
def draw_path(path, screen, init, final):
    for (x, y) in path:
        draw_square(x, y, screen, init, final, C_PATH)
        time.sleep(0.01)

# resets the board
def reset(height, width, board, screen, init, final):
    for x in range(1, int(SIZE[0]/SQUARE_L)-1):
        for y in range(1,int(SIZE[1]/SQUARE_L)-1):
            if (x, y) != init and (x,y) != final:
                r = board.get((x, y))
                pygame.draw.rect(screen, GREY, [height, width, SQUARE_L, SQUARE_L])
                pygame.draw.rect(screen, BLACK, [height, width, SQUARE_L, SQUARE_L], 1)
                if r == WALL:
                    board[(x, y)] = 0
            width += SQUARE_L
        width = SQUARE_L
        height += SQUARE_L
    return board

# resets the board without erasing the walls
def reset_path(height, width, board, screen, init, final):
    for x in range(1, int(SIZE[0]/SQUARE_L)-1):
        for y in range(1,int(SIZE[1]/SQUARE_L)-1):
            if (x, y) != init and (x,y) != final and board.get((x, y)) != 1:
                r = board.get((x, y))
                pygame.draw.rect(screen, GREY, [height, width, SQUARE_L, SQUARE_L])
                pygame.draw.rect(screen, BLACK, [height, width, SQUARE_L, SQUARE_L], 1)
            width += SQUARE_L
        width = SQUARE_L
        height += SQUARE_L
    return board
import pygame, os
from typing import Tuple

# module -> Path finding data

# Algorithms
A_STAR = "A-star"        # A* algorithm
DIJKSTRAS = "Dijsktra's"     # Dijkstra's algorithm
ALGORITHMS = [A_STAR, DIJKSTRAS]

# Colors
C_INIT = (0, 170, 0)            # Green
C_FINAL = (255, 0, 0)           # Red
C_WALL = (255, 255, 255)        # White
C_PATH = (51, 51, 255)          # Blue
C_CLOSED = (204, 204, 0)        # Yellow
C_OPEN = (255, 128, 0)          # orange
C_BUTTON = (200, 0, 0)          # Red
C_OVER_BUTTON = (255, 51, 51)   # Ligth red
BLACK = (0, 0, 0)               # Black
GREY = (96, 96, 96)             # Grey
L_GREY = (165, 165, 165)        # Light grey
L_GREEN = (51, 255, 51)         # Light green

# Representations:
NULL = 0    # empty cell
INIT = -1   # start cell
WALL = 1    # wall cell
FINAL = 2   # end cell

# Sizes
SIZE = [800, 600]   # board size
P_SIZE = [800, 690] # screen size
SQUARE_L = 15       # cell side size


# Limits coords
L_INIT = 1, 1
L_FINAL = int(SIZE[0]/SQUARE_L) - 2, int(SIZE[1]/SQUARE_L) - 2

# Path
PATH = os.path.dirname(os.path.realpath(__file__))

# class used for the algorithms
class Node:
    # Constructor
    def __init__(self, position:Tuple, parent:Tuple):
        self.position = position
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
        self.value = 1

    # Instance for compare
    def __eq__(self, other):
        return self.position == other.position
    # Instance for sort

    def __lt__(self, other):
         return self.f < other.f

# class used for the buttons
class button():
    # Constructor
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # This method to draws the button on the screen
    def draw(self,win, tam = 60, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4), 0)
    
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', tam)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
    
    # This method return True if pos is in button, else return False
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True 
        return False
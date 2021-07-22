import math, threading, time
from data import *
from board import draw_square
from tkinter import *

# module -> Path finding algorithms

painted_open = []
painted_closed = []
painted = []
sem = threading.Semaphore(1)

############################## A #################################################
# A* path finding algorithm
def astar_search(board, start, end, screen, show_steps):

    # painted lists
    painted_open = []
    painted_closed = []

    # Create lists for open and closed nodes
    open = []
    closed = []

    # Create a start node and an end node
    start_node = Node(start, None)
    end_node = Node(end, None)

    # Add the start node
    open.append(start_node)

    # Loop until the open list is empty
    while len(open) > 0:
        sem.acquire()

        # sort the open list
        open.sort()

        # take the current node
        current_node = open.pop(0)

        # append the current node to close
        closed.append(current_node)

        # if current_node == end_node, we return the path(reversed)
        if current_node == end_node:
            sem.release()
            t1.join()
            t2.join()
            path = []
            while current_node != start_node:
                x1, y1 = current_node.position
                path.append((x1, y1))
                current_node = current_node.parent
            del path[0]
            return path[::-1]

        # take the current position
        x, y = current_node.position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]

        for next in neighbors:
            board_value = board.get(next)

            # if it's a wall
            if board_value == WALL:
                continue
            
            # take the neighbor of the current_node
            neighbor = Node(next, current_node)

            # if it's in closed
            if neighbor in closed:
                continue
            
            # calculate the heuristics
            neighbor.g = current_node.g + math.sqrt((current_node.position[0] - neighbor.position[0])**2 + (current_node.position[1] - neighbor.position[1] )**2)
            neighbor.h = math.sqrt((end[0] - neighbor.position[0])**2 + (end[1] - neighbor.position[1] )**2)
            neighbor.f = neighbor.g + neighbor.h

            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor)):
                # add neighbor to the open list
                open.append(neighbor)
            
        sem.release()
        if show_steps:
            t1 = threading.Thread(name="draw1", target=draw, args=(open, painted_open, screen, start, end, C_OPEN))
            t2 = threading.Thread(name="draw2", target=draw, args=(closed, painted_closed, screen, start, end, C_CLOSED))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
    
    # if we dont find path, return []
    return []

# check if neighbor can be added to open
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

############################## B #################################################
# Dijkstra's path finding algorithm

def dijkstras_search(board, start, end, screen, show_steps):

    # list of panted nodes
    painted = []

    # list of visited nodes
    not_visited = []
    visited = []

    # Create a start node
    start_node = Node(start, None)

    for i in range(int(SIZE[0]/SQUARE_L)):
        for j in range(int(SIZE[1]/SQUARE_L)):
            if (i, j) != start:
                not_visited.append((i, j))

    # Add the start node to visited
    visited.append(start_node)

    # Loop until the visited list is empty
    while len(not_visited) > 0:

        # sort the list
        visited.sort()

        # take the current node
        current_node = visited.pop(0)

        # if current_node == end_node, we return the path(reversed)
        if board.get(current_node.position) == FINAL:
            path = []
            t1.join()
            while current_node != start_node:
                x1, y1 = current_node.position
                path.append((x1, y1))
                current_node = current_node.parent
            del path[0]
            return path[::-1]

        # take the current position
        x, y = current_node.position
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        for next in neighbors:
            board_value = board.get(next)

            # if it's a wall
            if board_value == WALL:
                continue

            neighbor = Node(next, current_node)
            neighbor.f = current_node.f + 1

            # if one neighbor is in final coords break
            if board_value == FINAL:
                neighbor.f = 0
                visited.append(neighbor)
                break
            
            # if neighbor not in visited
            if neighbor.position in not_visited:
                visited.append(neighbor)
                not_visited.remove(neighbor.position)

        # if show steps is active
        if show_steps:
            t1 = threading.Thread(name="draw1", target=draw, args=(visited, painted, screen, start, end, C_CLOSED))
            t1.start()
            t1.join()
    
    # if we dont find path, return []
    return []


#######################################################################################################################
# receives a list of nodes, a list of painted nodes, and draws the nodes in screen with color
def draw(l, c_painted, screen, start, end, color):
    for z in l:
        x1, y1 = z.position
        if y1 < int(SIZE[1]/SQUARE_L) and z not in c_painted:
            c_painted.append(z)
            draw_square(x1, y1, screen, start, end, color)
import pygame, sys
from data import *
from board import *
from algorithms import *

# module -> Path finding main file

# call the algorithm to find the path
def findPath(algorithm, reseted, board, screen, init, final, show_steps):
    # resets the board
    if not reseted:
            board = reset_path(SQUARE_L, SQUARE_L, board, screen, init, final)

    # runs A* algorithm
    if algorithm == A_STAR:
        path = astar_search(board, init, final, screen, show_steps)
    
    # runs dijsktra's algorithm
    elif algorithm == DIJKSTRAS:
        path = dijkstras_search(board, init, final, screen, show_steps)

    reseted = False
    # draw the path
    draw_path(path, screen, init ,final)
    return reseted, board

# run the program
def run():
    # init the program
    pygame.init()

    # Default coords
    init = L_INIT
    final = L_FINAL

    # window image
    windowImg = pygame.image.load(PATH + "/imgs/icon.jpg")

    # init the screen
    screen = pygame.display.set_mode(P_SIZE)
    screen.fill(GREY)
    clock = pygame.time.Clock()
    pygame.display.set_icon(windowImg)          # window image
    pygame.display.set_caption("Path finder")   # window name

    # buttons
    init_button = button(C_BUTTON, 10, 620, 150, 50, "Run")
    reset_all_button = button(C_BUTTON, 170, 620, 150, 25, "Reset all")
    reset_path_button = button(C_BUTTON, 170, 645, 150, 25, "Reset path")
    set_init_button = button(C_BUTTON, 330, 620, 150, 25, "Set start coords")
    set_final_button = button(C_BUTTON, 330, 645, 150, 25, "Set end coords")
    change_algo_button = button(C_BUTTON, 495, 620, 140, 25, "Change algorithm")
    show_steps_button = button(C_INIT, 650, 620, 140, 50, "Show steps")

    # make the board
    board = get_board(init, final)

    # draw the grid
    draw_grid(0, 0, board, screen)

    # default settings
    running = False
    reseted = True
    set_init = False
    set_end = False
    show_steps = True

    algo_index = 0
    algorithm = ALGORITHMS[algo_index]

    # program loop
    while True:
        # show algorithm
        show_algorithm = button(GREY, 495, 645, 140, 25, algorithm)
        show_running = button(GREY, 10, 600, 60, 18)

        # draw and update buttons 
        init_button.draw(screen, 60, BLACK)
        reset_all_button.draw(screen, 27, BLACK)
        reset_path_button.draw(screen, 27, BLACK)
        set_init_button.draw(screen, 27, BLACK)
        set_final_button.draw(screen, 27, BLACK)
        show_steps_button.draw(screen, 27, BLACK)
        change_algo_button.draw(screen, 23, BLACK)
        show_algorithm.draw(screen, 27, BLACK)

        if pygame.event.peek:
            event = pygame.event.poll()
        # for event in pygame.event.get():
            if not running:
                # QUIT event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse leftclick event
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    # Start button
                    if init_button.isOver(pos):
                        running = True
                        show_running.text = "Running..."
                        show_running.draw(screen, 18)
                        pygame.display.update()
                        reseted, board = findPath(algorithm, reseted, board, screen, init, final, show_steps)
                        show_running.text = ""
                        show_running.draw(screen, 18)
                        running = False
                    
                    # Reset all button
                    elif reset_all_button.isOver(pos):
                        board = reset(SQUARE_L, SQUARE_L, board, screen, init, final)
                        reseted = True
                    
                    # Reset path button
                    elif reset_path_button.isOver(pos):
                        board = reset_path(SQUARE_L, SQUARE_L, board, screen, init, final)
                        reseted = True
                    
                    # Set start button
                    elif set_init_button.isOver(pos) and reseted:
                        set_init = True
                        set_end = False

                    # Set end button  
                    elif set_final_button.isOver(pos) and reseted:
                        set_end = True
                        set_init = False
                    
                    # Change algorithm button
                    elif change_algo_button.isOver(pos):
                        algo_index +=1
                        if algo_index == len(ALGORITHMS):
                            algo_index = 0
                        algorithm = ALGORITHMS[algo_index]

                    # Show steps button
                    elif show_steps_button.isOver(pos):
                        if show_steps:
                            show_steps = False
                        else:
                            show_steps = True

                    elif reseted:
                        x_10 = int(x/SQUARE_L)
                        y_10 = int(y/SQUARE_L)
                        if board.get((x_10, y_10)) != 1 and x < SIZE[0] and y < SIZE[1]:
                            # Place start
                            if set_init:
                                board = draw_init(x, y, board, screen, init, final)
                                init = x_10, y_10
                                set_init = False
                            # Place end
                            elif set_end:
                                board = draw_end(x, y, board, screen, init, final)
                                x_10 = int(x/SQUARE_L)
                                y_10 = int(y/SQUARE_L)
                                final = x_10, y_10
                                set_end = False
                            # Place wall
                            else:
                                board = draw_wall(x, y, board, screen, init, final)

                # Mouse rigthclick event
                if pygame.mouse.get_pressed()[2] and reseted:
                    x, y = pygame.mouse.get_pos()
                    board = erase_wall(x, y, board, screen, init, final)
                
                # Mouse motion event
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()

                    if init_button.isOver(pos):
                        init_button.color = C_OVER_BUTTON
                    else:
                        init_button.color = C_BUTTON

                    if reset_all_button.isOver(pos):
                        reset_all_button.color = C_OVER_BUTTON
                    else:
                        reset_all_button.color = C_BUTTON
                    
                    if reset_path_button.isOver(pos):
                        reset_path_button.color = C_OVER_BUTTON
                    else:
                        reset_path_button.color = C_BUTTON

                    if set_init_button.isOver(pos):
                        set_init_button.color = C_OVER_BUTTON
                    else:
                        set_init_button.color = C_BUTTON

                    if set_final_button.isOver(pos):
                        set_final_button.color = C_OVER_BUTTON
                    else:
                        set_final_button.color = C_BUTTON

                    if change_algo_button.isOver(pos):
                        change_algo_button.color = C_OVER_BUTTON
                    else:
                        change_algo_button.color = C_BUTTON
                    
                    if show_steps_button.isOver(pos):
                        if show_steps:
                            show_steps_button.color = L_GREEN
                        else:
                            show_steps_button.color = C_OVER_BUTTON
                    else:
                        if show_steps:
                            show_steps_button.color = C_INIT
                        else:
                            show_steps_button.color = C_BUTTON
        pygame.event.wait()
        pygame.event.clear()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run()

import numpy as np
import pygame
from pygame.locals import *
import sys

def main():
    
    dim_1, dim_2 = 20, 20                                    # one is welcome to change those vars
    window_x, window_y = 600, 600
    FPS = 10

    tile_x, tile_y = int(window_x/dim_1), int(window_y/dim_2)

    pygame.init()

    table = np.zeros((dim_1, dim_2), np.int32)               # game matrix
    
    WHITE = pygame.Color(255, 255, 255)
    BLACK = pygame.Color(0,0,0)

    fpsClock = pygame.time.Clock()

    game_window = pygame.display.set_mode((window_x, window_y))
    pygame.display.set_caption("Game of life")

    def place_tile(x, y):
        # Placing tiles before the start of game
        index_x, index_y = x//tile_x, y//tile_y 
        table[index_y, index_x] = 1
        for row in table:
            for col in row:
                pygame.draw.rect(game_window, WHITE, [(x//tile_x)*tile_x, (y//tile_y)*tile_y] + [tile_x, tile_y])

    def draw_next_move():
        for row in range(table.shape[0]):
            for col in range(table.shape[1]):
                if table[row, col] == 1:
                    pygame.draw.rect(game_window, WHITE, [col*tile_x, row*tile_y] + [tile_x, tile_y])

    def calc_next_move(table, dim_1 = dim_1, dim_2 = dim_2):
        # Game logic
        calc = np.zeros((dim_1, dim_2), np.int32)                                                                                 # game matrix cannot be modified in-place explicitly
        for i in range(dim_1):
            for j in range(dim_2):
                calc[i, j] = (table[(i-1)%dim_1, (j-1)%dim_2] + table[(i-1)%dim_1, (j)%dim_2] + table[(i-1)%dim_1, (j+1)%dim_2] + # row above
                            table[(i)%dim_1, (j-1)%dim_2] + table[(i)%dim_1, (j+1)%dim_2] +                                       # current row
                            table[(i+1)%dim_1, (j-1)%dim_2] + table[(i+1)%dim_1, (j)%dim_2] + table[(i+1)%dim_1, (j+1)%dim_2])    # row below
        calc = np.where(((calc == 2) & (table == 1)) | ((calc == 3) & (table == 1)) | ((calc == 3) & (table == 0)), 1, 0)
        table = np.copy(calc)
        return table
        
    game_started = 0

    while True:

        game_window.fill(BLACK)
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
             
            if event.type == KEYDOWN: 
                game_started = 1

            if event.type == MOUSEBUTTONDOWN and game_started == 0:
                x, y = pygame.mouse.get_pos()
                place_tile(x, y)
        
        draw_next_move()

        if game_started:
            table = calc_next_move(table)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
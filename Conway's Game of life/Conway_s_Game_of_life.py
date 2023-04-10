import numpy as np
import pygame
from random import randint


# Define the size of the grid
N = 100

# Create an empty grid
grid = np.zeros((N, N), dtype=int)

# Define the initial configuration of the grid
# Here, we'll use a glider as an example
grid[1, 3] = 1
grid[2, 1:4] = 1
grid[3, 2] = 1

# Define the rules for the Game of Life
def evolve(grid):
    new_grid = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            neighbors = np.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            # Apply the rules
            if grid[i, j] == 1 and neighbors < 2:
                new_grid[i, j] = 0
            elif grid[i, j] == 1 and neighbors > 3:
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and neighbors == 3:
                new_grid[i, j] = 1
            else:
                new_grid[i, j] = grid[i, j]
    return new_grid

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width = 500
height = 500

# Create a window surface
screen = pygame.display.set_mode((width, height))

# Set the title of the window
pygame.display.set_caption("10x10 Array")

# Define the size of the grid cells
cell_size = width//N


def drawGrid():
    # Draw the grid.
    for row in range(N):
        for column in range(N):
            # Define the cell coordinatates.
            x = column * cell_size
            y = row * cell_size

            # Rainbow Colors!!!
            if grid[row][column] == 1:
                color = (randint(0,255), randint(0,255), randint(0,255))  # white
            else:
                color = (0, 0, 0)  # black

            # Draw cell
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))


# Game loop.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the cell coordinates of the clicked cell
            x, y = pygame.mouse.get_pos()
            row = y // cell_size
            column = x // cell_size
            # Toggle the state of the cell
            grid[row][column] = 1 - grid[row][column]
    drawGrid()
    pygame.display.update()
    grid = evolve(grid)
    pygame.time.delay(100)

# Quit Pygame
pygame.quit()

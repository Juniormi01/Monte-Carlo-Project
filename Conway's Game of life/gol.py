import numpy
import pygame
from random import randint
from random import choice
import patterns
import attributes

# Classic rules
def evolve(N, grid):
    new_grid = numpy.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            neighbors = numpy.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            # Apply the rules
            # If neighbors < 2
            if grid[i, j] == 1 and neighbors < 2:
                new_grid[i, j] = 0
            #elif grid[i, j] == 1 and neighbors > 3:
            elif grid[i, j] == 1 and neighbors > 3:
                new_grid[i, j] = 0
            #elif grid[i, j] == 0 and neighbors == 3:
            elif grid[i, j] == 0 and neighbors == 3:
                new_grid[i, j] = 1
            else:
                new_grid[i, j] = grid[i, j]
    return new_grid
# First new pattern found
def evolve_new(N, grid):
    new_grid = numpy.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            neighbors = numpy.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            # Apply the rules
            # If neighbors < 2
            if grid[i, j] == 1 and neighbors < 2:
                new_grid[i, j] = 0
            #elif grid[i, j] == 1 and neighbors > 3:
            elif grid[i, j] == 1 and neighbors > 4:
                new_grid[i, j] = 0
            #elif grid[i, j] == 0 and neighbors == 3:
            elif grid[i, j] == 0 and neighbors >= 3:
                new_grid[i, j] = 1
            else:
                new_grid[i, j] = grid[i, j]
    return new_grid
# Rule that kind of looks like a brain for a brief moment
def evolve_brain(N, grid):
    new_grid = numpy.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            neighbors = numpy.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            # Apply the rules
            # If neighbors < 2
            if grid[i, j] == 1 and neighbors < 2:
                new_grid[i, j] = 0
            #elif grid[i, j] == 1 and neighbors > 4:
            elif grid[i, j] == 1 and neighbors > 4:
                new_grid[i, j] = 0
            #elif grid[i, j] == 0 and neighbors == 3:
            elif grid[i, j] == 0 and neighbors == 3:
                new_grid[i, j] = 1
            else:
                new_grid[i, j] = grid[i, j]
    return new_grid
# Looks like it has a couple fireworks shooting off, works best with F-Pentomino
def evolve_spark(N, grid):
    new_grid = numpy.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            neighbors = numpy.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            # Apply the rules
            # If neighbors < 2
            if grid[i, j] == 1 and neighbors < 5:
                new_grid[i, j] = 0
            #elif grid[i, j] == 1 and neighbors > 4:
            elif grid[i, j] == 1 and neighbors > 4:
                new_grid[i, j] = 0
            #elif grid[i, j] == 0 and neighbors == 3:
            elif grid[i, j] == 0 and neighbors == 2:
                new_grid[i, j] = 1
            else:
                new_grid[i, j] = grid[i, j]
    return new_grid
# The outside of the pattern growth creates blocks
def evolve_block(N, grid):
    new_grid = numpy.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            # Count the number of live neighbors
            neighbors = numpy.sum(grid[i-1:i+2, j-1:j+2]) - grid[i, j]
            # Apply the rules
            # If neighbors < 4
            if grid[i, j] == 1 and neighbors < 7:
                new_grid[i, j] = 0
            #elif grid[i, j] == 1 and neighbors > 4:
            elif grid[i, j] == 1 and neighbors > 3:
                new_grid[i, j] = 0
            #elif grid[i, j] == 0 and neighbors == 4:
            elif grid[i, j] == 0 and neighbors == 1:
                new_grid[i, j] = 1
            else:
                new_grid[i, j] = grid[i, j]
    return new_grid

def run_simulation(patternid):
    N = attributes.grid_size
    grid = numpy.zeros((N, N), dtype=int)
    # Creates the pattern for demonstration
    patterns.create_pattern(grid, patternid)

    # Initialize PyGame
    pygame.init()

    def drawGrid():
        # Draw the grid.
        for row in range(N):
            for column in range(N):
                # Define the cell coordinatates.
                x = (column * cell_size)
                y = (row * cell_size)

                # Rainbow Colors!!!
                if grid[row][column] == 1:
                    color = (randint(0, 255), randint(0, 255), randint(0, 255))
                    #color = (255, 255, 255)
                else:
                    color = (0, 0, 0)  # black

                # Draw cell
                pygame.draw.rect(screen, color, (y, x, cell_size, cell_size))

    width = 1000
    height = 1000

    # Create a window surface
    screen = pygame.display.set_mode((width, height))

    # Set the title of the window
    pygame.display.set_caption(patternid)

    # Define the size of the grid cells
    cell_size = width // N

    # Text displaying iterations
    iterations = 0

    running = attributes.paused
    while running:
        iterations += 1
        iterationsString = str("Iterations: " + str(iterations))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                pygame.quit()
            font = pygame.font.SysFont("Arial", 18)
        textsurf = font.render(iterationsString, True, (255, 255, 255))
        drawGrid()
        screen.blit(textsurf, (10, 10))
        pygame.display.update()
        if attributes.rule_set == "classic":
            grid = evolve(N, grid)
        elif attributes.rule_set == "new_rule":
            grid = evolve_new(N, grid)
        elif attributes.rule_set == "brain":
            grid = evolve_brain(N, grid)
        elif attributes.rule_set == "spark":
            grid = evolve_spark(N, grid)
        elif attributes.rule_set == "block":
            grid = evolve_block(N, grid)
        
        pygame.time.delay(attributes.simulation_speed)
    
    # Debugging mode
    while running == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        drawGrid()
        pygame.display.update()
        pygame.time.delay(attributes.simulation_speed)

    pygame.quit()
                




 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

# Define the animation function
def animate(frame):
    global grid
    grid = evolve(grid)
    plt.imshow(grid, cmap='binary')
    plt.axis('off')

# Create the animation
fig = plt.figure(figsize=(5, 5))
ani = animation.FuncAnimation(fig, animate, frames=100, interval=100, blit=False)

# Show the animation
plt.show()


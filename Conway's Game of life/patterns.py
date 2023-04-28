# I think it's [Y, X]
def create_pattern(grid, patternid):
    if patternid == "simple":
        grid[50, 53] = 1
        grid[51, 51:54] = 1
        grid[52, 52] = 1
    elif patternid == "rpentomino":
        grid[20, 20:22] = 1
        grid[21, 19:21] = 1
        grid[22, 20] = 1
    elif patternid == "fpentomino":
        grid[50, 79] = 1
        grid[51, 81] = 1
        grid[52, 78:80] = 1
        grid[52, 82:85] = 1
    elif patternid == "glider":
        grid[20, 10] = 1
        grid[21, 11] = 1
        grid[22, 9:12] = 1
    elif patternid == "gospergg":
        # Left block
        grid[10, 10] = 1
        grid[11, 10] = 1
        grid[10, 11] = 1
        grid[11, 11] = 1

        # Circle (left)
        grid[20, 10] = 1
        grid[20, 11] = 1
        grid[20, 12] = 1
        # Circle (top)
        grid[21, 9] = 1
        grid[22, 8] = 1
        grid[23, 8] = 1
        # Circle (bottom)
        grid[21, 13] = 1
        grid[22, 14] = 1
        grid[23, 14] = 1
        # The dot
        grid[24, 11] = 1

        # Circle (right)
        grid[26, 11] = 1
        grid[27, 11] = 1
        grid[26, 10] = 1
        grid[25, 9] = 1
        grid[26, 12] = 1
        grid[25, 13] = 1

        # Right ship
        grid[30, 8] = 1
        grid[31, 8] = 1
        grid[30, 9] = 1
        grid[31, 9] = 1
        grid[30, 10] = 1
        grid[31, 10] = 1
        grid[32, 11] = 1
        grid[34, 11] = 1
        grid[34, 12] = 1
        grid[32, 7] = 1
        grid[34, 7] = 1
        grid[34, 6] = 1
        # Right dot
        grid[44, 8] = 1
        grid[45, 8] = 1
        grid[44, 9] = 1
        grid[45, 9] = 1
    elif patternid == "mininf":
        grid[80, 80] = 1
        grid[82, 80] = 1
        grid[82, 79] = 1
        grid[84, 78] = 1
        grid[84, 77] = 1
        grid[84, 76] = 1
        grid[86, 77] = 1
        grid[86, 76] = 1
        grid[86, 75] = 1
        grid[87, 76] = 1
    elif patternid == "stillife":
        # Block
        grid[5, 5] = 1
        grid[6, 5] = 1
        grid[5, 6] = 1
        grid[6, 6] = 1
        # bee-hive
        grid[10, 5] = 1
        grid[11, 4] = 1
        grid[12, 4] = 1
        grid[11, 6] = 1
        grid[12, 6] = 1
        grid[13, 5] = 1
        # Loaf
        grid[5, 10] = 1
        grid[6, 10] = 1
        grid[4, 11] = 1
        grid[7, 11] = 1
        grid[5, 12] = 1
        grid[7, 12] = 1
        grid[6, 13] = 1
        # Tub
        grid[13, 10] = 1
        grid[12, 11] = 1
        grid[14, 11] = 1
        grid[13, 12] = 1
        # Boat
        grid[17, 5] = 1
        grid[18, 5] = 1
        grid[17, 6] = 1
        grid[19, 6] = 1
        grid[18, 7] = 1
    elif patternid == "test":
        grid[0,0] = 1
        grid[1,1] = 1
        grid[2,2] = 1
        grid[3,3] = 1
        grid[4,4] = 1
        grid[5,5] = 1
        grid[0,0] = 1
        grid[8,8] = 1
        grid[0,0] = 1
        grid[2,2] = 1
        grid[4,4] = 1
        grid[5,5] = 1
        grid[6,6] = 1
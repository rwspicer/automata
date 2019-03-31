import numpy as np
import copy

ROW, COL = 0, 1

T = 2
M = 1
B = 0

L = 2
R = 0

def neighbors(grid, idx):
    if 0 < idx[ROW] < grid.shape[ROW]-1 and  0 < idx[COL] < grid.shape[COL]-1:
        # print('totaly in bounds')
        return grid[idx[ROW]-1:idx[ROW]+2,idx[COL]-1:idx[COL]+2][::-1]
    # special cases
    hood = np.zeros([3,3]) - 1
    if idx == [0,0]:
        # print ("top left corner")
        hood[1:,1:] = grid[:idx[ROW]+2,:idx[COL]+2]
    elif idx == [0,grid.shape[COL]-1]:
        # print("top right corner")
        hood[1:,:-1] = grid[:idx[ROW]+2,idx[COL]-1:idx[COL]+2]
    elif idx == [grid.shape[ROW]-1,0]:
        # print ("bottom left corner")
        hood[:-1,1:] = grid[idx[ROW]-1:,:idx[COL] +2]
    elif idx == [grid.shape[ROW]-1,grid.shape[COL]-1]:
        # print ("bottop right corner")
        hood[:-1,:-1] = grid[idx[ROW]-1:,idx[COL]-1:]
    elif idx[ROW] == 0:
        # print('top')
        hood[1:,:] = grid[idx[ROW]:idx[ROW]+2,idx[COL]-1:idx[COL]+2]
    elif idx[COL] == 0:
        # print('left')
        hood[:,1:] = grid[idx[ROW]-1:idx[ROW]+2,0:idx[COL]+2]
    elif idx[COL] == grid.shape[COL] - 1:
        # print('right')
        hood[:,:-1] = grid[idx[ROW]-1:idx[ROW]+2,idx[COL]-1:]
    elif idx[ROW] == grid.shape[ROW] - 1:
        # print('bottom')
        hood[:-1,:] = grid[idx[ROW]-1:,idx[COL]-1:idx[COL]+2]
    else:
        # print ("out of bounds")
        hood[:] = np.nan
    return hood[::-1]

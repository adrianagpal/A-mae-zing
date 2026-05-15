import numpy as np
import random
#import matplotlib.pyplot as plt

class MazeGenerator():
    def __init__(self, size: tuple[int, int], seed: int = 42):
        self.size = size
        self.seed = seed

    def generate(self, entry, exit_coord):
        np.random.seed(self.seed)

        # Creates a matrix of zeros
        mat = np.zeros(self.size, dtype=int)
        #mat[entry[0], entry[1]] = 16
        #mat[exit_coord[0], exit_coord[1]] = 17
        
        pad_mat = np.pad(mat, pad_width=1, mode='constant', constant_values=15)

        return mat
    
    def paint_42(self, mat):

        if self.size[0] > 5 and self.size[1] > 7:

            n_blocks = max(min(int(self.size[0]/(3 * 2)), 
                            int(self.size[1]/(3 * 2))), 3)
            space = 1
            n_width = n_blocks * 2 + space
            n_height = n_width - 2

            x = int(self.size[1]/2 - n_height/2) - 1
            y = int(self.size[0]/2 - n_width/2) + 1
            
            for i in range(0, n_blocks):
                mat[y + i][x] = 15
                mat[y + n_blocks - 1][x + i] = 15
                mat[y + n_blocks + i - 1][x + n_blocks - 1] = 15
            
            for j in range(0, n_blocks):
                mat[y][x + n_blocks + j + space] = 15
                mat[y + j][x + 2 * n_blocks + space - 1] = 15
                mat[y + n_blocks - 1][x + n_blocks + space + j] = 15
                mat[y + n_blocks + j - 1][x + n_blocks + space] = 15
                mat[y + 2 * n_blocks - 2][x + n_blocks + space + j] = 15       

        #plt.imshow(mat, cmap='viridis', vmin=1, vmax=10)
        #plt.show()  

        return mat

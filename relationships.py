import random
import numpy as np
from color_map import COLOR_MAP

class Relationship:
    def __init__(self):
        self.colors = random.sample(list(COLOR_MAP.keys()), k=2)

    def get_description(self):
        raise NotImplementedError("Subclasses must implement this method")

    def apply(self, grid):
        raise NotImplementedError("Subclasses must implement this method")

    def get_code(self):
        raise NotImplementedError("Subclasses must implement this method")

class ColorSwapRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.color1, self.color2 = self.colors

    def get_description(self):
        return f"Swap all {self.color1} tiles with {self.color2} tiles."

    def apply(self, grid):
        grid[grid == self.color1] = 'temp'
        grid[grid == self.color2] = self.color1
        grid[grid == 'temp'] = self.color2
        return grid

    def get_code(self):
        return f"""
def apply(grid):
    grid[grid == '{self.color1}'] = 'temp'
    grid[grid == '{self.color2}'] = '{self.color1}'
    grid[grid == 'temp'] = '{self.color2}'
    return grid
"""

class ColorFillRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.target_color, self.fill_color = self.colors
        self.threshold = random.uniform(0.3, 0.7)

    def get_description(self):
        return f"If more than {self.threshold:.0%} of the grid is {self.target_color}, fill the rest with {self.fill_color}."

    def apply(self, grid):
        total_cells = grid.size
        target_count = np.sum(grid == self.target_color)
        if target_count / total_cells > self.threshold:
            grid[grid != self.target_color] = self.fill_color
        return grid

    def get_code(self):
        return f"""
def apply(grid):
    total_cells = grid.size
    target_count = np.sum(grid == '{self.target_color}')
    if target_count / total_cells > {self.threshold}:
        grid[grid != '{self.target_color}'] = '{self.fill_color}'
    return grid
"""

class ColorBorderRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.inner_color, self.border_color = self.colors

    def get_description(self):
        return f"Add a border of {self.border_color} around areas of {self.inner_color}."

    def apply(self, grid):
        height, width = grid.shape
        for i in range(height):
            for j in range(width):
                if grid[i, j] == self.inner_color:
                    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < height and 0 <= nj < width and grid[ni, nj] != self.inner_color:
                            grid[ni, nj] = self.border_color
        return grid

    def get_code(self):
        return f"""
def apply(grid):
    height, width = grid.shape
    for i in range(height):
        for j in range(width):
            if grid[i, j] == '{self.inner_color}':
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width and grid[ni, nj] != '{self.inner_color}':
                        grid[ni, nj] = '{self.border_color}'
    return grid
"""

def get_random_relationship():
    return random.choice([ColorSwapRelationship(), ColorFillRelationship(), ColorBorderRelationship()])

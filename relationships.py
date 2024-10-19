import random
import numpy as np
from color_map import COLOR_MAP

class Relationship:
    def get_description(self):
        raise NotImplementedError("Subclasses must implement this method")

    def apply(self, grid):
        raise NotImplementedError("Subclasses must implement this method")

    def get_code(self, arg_info=None):
        raise NotImplementedError("Subclasses must implement this method")

    def can_apply(self, grid):
        return True

class ColorSwapRelationship(Relationship):
    def __init__(self):
        self.color1, self.color2 = random.sample(list(COLOR_MAP.keys()), k=2)
        self.arg_info = {"color1": self.color1, "color2": self.color2}

    def get_description(self):
        return f"If both {self.color1} and {self.color2} are present, swap all {self.color1} tiles with {self.color2} tiles."

    def apply(self, grid):
        if np.any(grid == self.color1) and np.any(grid == self.color2):
            grid[grid == self.color1] = 'temp'
            grid[grid == self.color2] = self.color1
            grid[grid == 'temp'] = self.color2
            return grid
        return "reject"

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    if np.any(grid == '{arg_info['color1']}') and np.any(grid == '{arg_info['color2']}'):
        grid[grid == '{arg_info['color1']}'] = 'temp'
        grid[grid == '{arg_info['color2']}'] = '{arg_info['color1']}'
        grid[grid == 'temp'] = '{arg_info['color2']}'
    return grid
"""

class ColorBorderRelationship(Relationship):
    def __init__(self):
        self.inner_color, self.border_color = random.sample(list(COLOR_MAP.keys()), k=2)
        self.arg_info = {"inner_color": self.inner_color, "border_color": self.border_color}

    def get_description(self):
        return f"If {self.inner_color} is present, add a border of {self.border_color} around areas of {self.inner_color}. Otherwise, return the original grid."

    def apply(self, grid):
        if np.any(grid == self.inner_color):
            height, width = grid.shape
            for i in range(height):
                for j in range(width):
                    if grid[i, j] == self.inner_color:
                        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < height and 0 <= nj < width and grid[ni, nj] != self.inner_color:
                                grid[ni, nj] = self.border_color
            return grid
        return "reject"

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    height, width = grid.shape
    for i in range(height):
        for j in range(width):
            if grid[i, j] == '{arg_info['inner_color']}':
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width and grid[ni, nj] != '{arg_info['inner_color']}':
                        grid[ni, nj] = '{arg_info['border_color']}'
    return grid
"""

class ReplaceRowIfColorPresent(Relationship):
    def __init__(self):
        self.target_color = random.choice(list(COLOR_MAP.keys()))
        self.new_color = random.choice(list(COLOR_MAP.keys()))
        self.arg_info = {"target_color": self.target_color, "new_color": self.new_color}

    def get_description(self):
        return f"If {self.target_color} is present in any row, replace the entire row with {self.new_color}."

    def apply(self, grid):
        height, width = grid.shape
        for i in range(height):
            if self.target_color in grid[i, :]:
                grid[i, :] = self.new_color
        return grid

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    height, width = grid.shape
    for i in range(height):
        if '{arg_info['target_color']}' in grid[i, :]:
            grid[i, :] = '{arg_info['new_color']}'
    return grid
"""

class ReplaceColumnIfColorPresent(Relationship):
    def __init__(self):
        self.target_color = random.choice(list(COLOR_MAP.keys()))
        self.new_color = random.choice(list(COLOR_MAP.keys()))
        self.arg_info = {"target_color": self.target_color, "new_color": self.new_color}

    def get_description(self):
        return f"If {self.target_color} is present in any column, replace the entire column with {self.new_color}."

    def apply(self, grid):
        height, width = grid.shape
        for j in range(width):
            if self.target_color in grid[:, j]:
                grid[:, j] = self.new_color
        return grid

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    height, width = grid.shape
    for j in range(width):
        if '{arg_info['target_color']}' in grid[:, j]:
            grid[:, j] = '{arg_info['new_color']}'
    return grid
"""

class FractalGridRelationship(Relationship):
    def __init__(self):
        self.arg_info = {}

    def get_description(self):
        return "Replace each tile with a copy of the original grid or a black mini-grid if the tile is empty."

    def apply(self, grid):
        if not self.can_apply(grid):
            return "reject"
        height, width = grid.shape
        new_grid = np.empty((height * height, width * width), dtype=object)
        
        for i in range(height):
            for j in range(width):
                # This condition will trigger the error
                if grid[i, j] == 'Empty':
                    new_grid[i*height:(i+1)*height, j*width:(j+1)*width] = 'Empty'
                else:
                    new_grid[i*height:(i+1)*height, j*width:(j+1)*width] = grid
        
        return new_grid

    def get_code(self, arg_info=None):
        return """
def apply(grid):
    height, width = grid.shape
    new_grid = np.empty((height * height, width * width), dtype=object)
    
    for i in range(height):
        for j in range(width):
            if grid[i, j] == 'Empty':
                new_grid[i*height:(i+1)*height, j*width:(j+1)*width] = 'Empty'
            else:
                new_grid[i*height:(i+1)*height, j*width:(j+1)*width] = grid
    
    return new_grid
"""

    def can_apply(self, grid):
        return grid.size <= 20

def get_random_relationship():
    return random.choice([ColorSwapRelationship(), ColorBorderRelationship(),
                          ReplaceRowIfColorPresent(), ReplaceColumnIfColorPresent(), FractalGridRelationship()])

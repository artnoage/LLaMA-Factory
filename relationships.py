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

class ColorSwapRelationship(Relationship):
    def __init__(self):
        self.color1, self.color2 = random.sample(list(COLOR_MAP.keys()), k=2)
        self.arg_info = {"color1": self.color1, "color2": self.color2}

    def get_description(self):
        return f"Swap all {self.color1} tiles with {self.color2} tiles."

    def apply(self, grid):
        grid[grid == self.color1] = 'temp'
        grid[grid == self.color2] = self.color1
        grid[grid == 'temp'] = self.color2
        return grid

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    grid[grid == '{arg_info['color1']}'] = 'temp'
    grid[grid == '{arg_info['color2']}'] = '{arg_info['color1']}'
    grid[grid == 'temp'] = '{arg_info['color2']}'
    return grid
"""

class ColorFillRelationship(Relationship):
    def __init__(self):
        self.target_color, self.fill_color = random.sample(list(COLOR_MAP.keys()), k=2)
        self.threshold = random.uniform(0.3, 0.7)
        self.arg_info = {"target_color": self.target_color, "fill_color": self.fill_color, "threshold": self.threshold}

    def get_description(self):
        return f"If more than {self.threshold:.0%} of the grid is {self.target_color}, fill the rest with {self.fill_color}."

    def apply(self, grid):
        total_cells = grid.size
        target_count = np.sum(grid == self.target_color)
        if target_count / total_cells > self.threshold:
            grid[grid != self.target_color] = self.fill_color
        return grid

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    total_cells = grid.size
    target_count = np.sum(grid == '{arg_info['target_color']}')
    if target_count / total_cells > {arg_info['threshold']}:
        grid[grid != '{arg_info['target_color']}'] = '{arg_info['fill_color']}'
    return grid
"""

class ColorBorderRelationship(Relationship):
    def __init__(self):
        self.inner_color, self.border_color = random.sample(list(COLOR_MAP.keys()), k=2)
        self.arg_info = {"inner_color": self.inner_color, "border_color": self.border_color}

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

class ChangeRowRelationship(Relationship):
    def __init__(self):
        self.row_index = None  # Will be set in apply()
        self.new_color = random.choice(list(COLOR_MAP.keys()))
        self.arg_info = {"new_color": self.new_color}

    def get_description(self):
        return f"Change a whole row to {self.new_color}."

    def apply(self, grid):
        height, width = grid.shape
        self.row_index = random.randint(0, height - 1)
        grid[self.row_index, :] = self.new_color
        self.arg_info["row_index"] = self.row_index
        return grid

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    grid[{arg_info['row_index']}, :] = '{arg_info['new_color']}'
    return grid
"""

class ChangeColumnRelationship(Relationship):
    def __init__(self):
        self.column_index = None  # Will be set in apply()
        self.new_color = random.choice(list(COLOR_MAP.keys()))
        self.arg_info = {"new_color": self.new_color}

    def get_description(self):
        return f"Change a whole column to {self.new_color}."

    def apply(self, grid):
        height, width = grid.shape
        self.column_index = random.randint(0, width - 1)
        grid[:, self.column_index] = self.new_color
        self.arg_info["column_index"] = self.column_index
        return grid

    def get_code(self, arg_info=None):
        if arg_info is None:
            arg_info = self.arg_info
        return f"""
def apply(grid):
    grid[:, {arg_info['column_index']}] = '{arg_info['new_color']}'
    return grid
"""

def get_random_relationship():
    return random.choice([ColorSwapRelationship(), ColorFillRelationship(), ColorBorderRelationship(),
                          ChangeRowRelationship(), ChangeColumnRelationship()])

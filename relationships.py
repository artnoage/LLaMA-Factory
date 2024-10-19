import random
from color_map import COLOR_MAP

class Relationship:
    def __init__(self):
        self.color = random.choice(list(COLOR_MAP.keys()))
        self.extra_params = {}

    def get_description(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_code(self):
        raise NotImplementedError("Subclasses must implement this method")

    def apply(self, grid):
        raise NotImplementedError("Subclasses must implement this method")

class ColorRowRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.extra_params = {"row_probability": random.uniform(0.3, 0.7)}

    def get_description(self):
        return f"If a tile has color {self.color}, replace the whole row with the color {self.color} with probability {self.extra_params['row_probability']:.2f}."

    def get_code(self):
        return f"""
def apply_relationship(grid):
    for i in range(grid.shape[0]):
        if '{self.color}' in grid[i] and random.random() < {self.extra_params['row_probability']}:
            grid[i] = '{self.color}'
    return grid
"""

    def apply(self, grid):
        for i in range(grid.shape[0]):
            if self.color in grid[i] and random.random() < self.extra_params['row_probability']:
                grid[i] = self.color
        return grid

class ColorColumnRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.extra_params = {"column_probability": random.uniform(0.3, 0.7)}

    def get_description(self):
        return f"If a tile has color {self.color}, replace the whole column with the color {self.color} with probability {self.extra_params['column_probability']:.2f}."

    def get_code(self):
        return f"""
def apply_relationship(grid):
    for j in range(grid.shape[1]):
        if '{self.color}' in grid[:, j] and random.random() < {self.extra_params['column_probability']}:
            grid[:, j] = '{self.color}'
    return grid
"""

    def apply(self, grid):
        for j in range(grid.shape[1]):
            if self.color in grid[:, j] and random.random() < self.extra_params['column_probability']:
                grid[:, j] = self.color
        return grid

def get_random_relationship():
    return random.choice([ColorRowRelationship(), ColorColumnRelationship()])

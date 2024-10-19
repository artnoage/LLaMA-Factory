import random
from color_map import COLOR_MAP

class Relationship:
    def __init__(self):
        self.color = random.choice(list(COLOR_MAP.keys()))

    def get_description(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_code(self):
        raise NotImplementedError("Subclasses must implement this method")

    def apply(self, grid):
        raise NotImplementedError("Subclasses must implement this method")

class ColorRowRelationship(Relationship):
    def get_description(self):
        return f"If a tile has color {self.color}, replace the whole row with the color {self.color}."

    def get_code(self):
        return f"""
def apply_relationship(grid):
    for i in range(grid.shape[0]):
        if '{self.color}' in grid[i]:
            grid[i] = '{self.color}'
    return grid
"""

    def apply(self, grid):
        for i in range(grid.shape[0]):
            if self.color in grid[i]:
                grid[i] = self.color
        return grid

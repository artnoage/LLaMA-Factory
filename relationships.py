import random
import numpy as np
from color_map import COLOR_MAP

class Relationship:
    def __init__(self):
        self.colors = random.sample(list(COLOR_MAP.keys()), k=random.randint(2, 4))
        self.extra_params = {}

    def get_description(self):
        raise NotImplementedError("Subclasses must implement this method")

    def apply(self, grid):
        raise NotImplementedError("Subclasses must implement this method")

class ColorPatternRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.pattern_length = random.randint(2, 3)
        self.pattern = [random.choice(self.colors) for _ in range(self.pattern_length)]
        self.direction = random.choice(['row', 'column', 'diagonal'])
        self.action = random.choice(['replace', 'insert'])
        self.replacement_color = random.choice(self.colors)

    def get_description(self):
        pattern_str = ' -> '.join(self.pattern)
        return f"If the pattern '{pattern_str}' is found in a {self.direction}, {self.action} with {self.replacement_color}."

    def apply(self, grid):
        height, width = grid.shape
        if self.direction == 'row':
            for i in range(height):
                self._apply_to_line(grid[i], axis=1)
        elif self.direction == 'column':
            for j in range(width):
                self._apply_to_line(grid[:, j], axis=0)
        else:  # diagonal
            for i in range(height - self.pattern_length + 1):
                for j in range(width - self.pattern_length + 1):
                    if all(grid[i+k, j+k] == self.pattern[k] for k in range(self.pattern_length)):
                        if self.action == 'replace':
                            for k in range(self.pattern_length):
                                grid[i+k, j+k] = self.replacement_color
                        else:  # insert
                            grid[i+self.pattern_length, j+self.pattern_length] = self.replacement_color
        return grid

    def _apply_to_line(self, line, axis):
        pattern_found = np.all(np.lib.stride_tricks.sliding_window_view(line, self.pattern_length) == self.pattern, axis=1)
        if self.action == 'replace':
            line[pattern_found] = self.replacement_color
        else:  # insert
            insert_positions = np.where(pattern_found)[0] + self.pattern_length
            np.put(line, insert_positions, self.replacement_color, mode='clip')

class ColorProximityRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.color1, self.color2 = random.sample(self.colors, 2)
        self.proximity = random.randint(1, 3)
        self.action_color = random.choice(self.colors)

    def get_description(self):
        return f"If {self.color1} is within {self.proximity} tiles of {self.color2}, change it to {self.action_color}."

    def apply(self, grid):
        height, width = grid.shape
        for i in range(height):
            for j in range(width):
                if grid[i, j] == self.color1:
                    neighborhood = grid[max(0, i-self.proximity):min(height, i+self.proximity+1),
                                        max(0, j-self.proximity):min(width, j+self.proximity+1)]
                    if self.color2 in neighborhood:
                        grid[i, j] = self.action_color
        return grid

class ColorMajorityRelationship(Relationship):
    def __init__(self):
        super().__init__()
        self.threshold = random.uniform(0.4, 0.7)
        self.majority_color = random.choice(self.colors)
        self.action_color = random.choice(self.colors)

    def get_description(self):
        return f"If more than {self.threshold:.0%} of the grid is {self.majority_color}, change all other colors to {self.action_color}."

    def apply(self, grid):
        total_cells = grid.size
        majority_count = np.sum(grid == self.majority_color)
        if majority_count / total_cells > self.threshold:
            grid[grid != self.majority_color] = self.action_color
        return grid

def get_random_relationship():
    return random.choice([ColorPatternRelationship(), ColorProximityRelationship(), ColorMajorityRelationship()])

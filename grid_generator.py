import numpy as np
import random

COLOR_MAP = {
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'Cyan': (0, 255, 255),
    'Magenta': (255, 0, 255)
}

def generate_grid(name, min_width=3, max_width=20, min_height=3, max_height=20):
    width = random.randint(min_width, max_width)
    height = random.randint(min_height, max_height)
    tile_size = random.randint(20, 50)
    
    colors = list(COLOR_MAP.keys())
    n_colors = len(colors)
    
    # Initialize base weights
    base_weight = {c: 1 for c in colors}
    base_weight['Black'] = 6  # Higher base weight for black
    beta = 4  # Influence of neighboring colors
    
    # Initialize grid
    grid = np.full((height, width), None, dtype=object)
    
    for i in range(height):
        for j in range(width):
            # Initialize weights with base weights
            weight = {c: base_weight[c] for c in colors}
            
            # Collect neighboring colors
            neighbors = []
            if i > 0 and j > 0:
                neighbors.append(grid[i-1, j-1])
            if i > 0:
                neighbors.append(grid[i-1, j])
            if i > 0 and j < width -1:
                neighbors.append(grid[i-1, j+1])
            if j > 0:
                neighbors.append(grid[i, j-1])
            
            # Update weights based on neighboring colors
            for neighbor_color in neighbors:
                if neighbor_color is not None:
                    weight[neighbor_color] += beta
            
            # Convert weights to probabilities
            total_weight = sum(weight.values())
            probabilities = [weight[c] / total_weight for c in colors]
            
            # Select color
            grid[i, j] = np.random.choice(colors, p=probabilities)
    
    return {
        'name': name,
        'width': width,
        'height': height,
        'tile_size': tile_size,
        'array': grid
    }

def place_grids(grids, canvas_size, margin):
    placed_grids = []
    for grid in grids:
        grid_width = grid['width'] * grid['tile_size']
        grid_height = grid['height'] * grid['tile_size']
        
        for _ in range(100):  # Try 100 times to place the grid
            x = random.randint(margin, canvas_size[0] - grid_width - margin)
            y = random.randint(margin, canvas_size[1] - grid_height - margin)
            
            # Check if this position overlaps with any previously placed grid
            overlap = any(
                rect_overlap(
                    (x, y, x + grid_width, y + grid_height),
                    (pg['position'][0], pg['position'][1], 
                     pg['position'][0] + pg['width'] * pg['tile_size'],
                     pg['position'][1] + pg['height'] * pg['tile_size'])
                )
                for pg in placed_grids
            )
            
            if not overlap:
                grid['position'] = (x, y)
                placed_grids.append(grid)
                break
        else:
            return False  # Couldn't place all grids
    
    return True

def rect_overlap(rect1, rect2):
    return not (rect1[2] <= rect2[0] or rect1[0] >= rect2[2] or
                rect1[3] <= rect2[1] or rect1[1] >= rect2[3])

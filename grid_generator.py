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
    
    # Initialize transition matrix
    colors = list(COLOR_MAP.keys())
    n_colors = len(colors)
    transition_matrix = np.ones((n_colors, n_colors))
    
    # Increase probability of black and same color
    black_index = colors.index('Black')
    for i in range(n_colors):
        transition_matrix[i, i] = 3  # Higher probability for same color
        transition_matrix[i, black_index] = 6  # 60% probability for black
    
    # Normalize probabilities
    transition_matrix /= transition_matrix.sum(axis=1, keepdims=True)
    
    # Generate grid
    grid = np.empty((height, width), dtype=object)
    for i in range(height):
        for j in range(width):
            if i == 0 and j == 0:
                grid[i, j] = np.random.choice(colors, p=[0.6 if c == 'Black' else 0.4/(n_colors-1) for c in colors])
            else:
                if i > 0:
                    prev_color = grid[i-1, j]
                else:
                    prev_color = grid[i, j-1]
                prev_index = colors.index(prev_color)
                grid[i, j] = np.random.choice(colors, p=transition_matrix[prev_index])
    
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

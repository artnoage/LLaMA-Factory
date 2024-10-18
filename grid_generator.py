import numpy as np
import random

COLOR_MAP = {
    'Magenta': (255, 0, 255),
    'Dark Red': (139, 0, 0),
    'Red': (255, 0, 0),
    'Orange': (255, 165, 0),
    'Yellow': (255, 255, 0),
    'Green': (0, 128, 0),
    'Light Blue': (173, 216, 230),
    'Blue': (0, 0, 255),
    'Gray': (128, 128, 128),
    'Black': (0, 0, 0)  # Represents empty
}

def weighted_random(min_val, max_val):
    weights = [1 / (np.log(i - min_val + 2)) for i in range(min_val, max_val+1)]
    return random.choices(range(min_val, max_val+1), weights=weights)[0]

def generate_grid(name, min_width=3, max_width=20, min_height=3, max_height=20):
    width = weighted_random(min_width, max_width)
    height = weighted_random(min_height, max_height)
    
    # Calculate tile size inversely proportional to the grid dimensions
    # Larger grids get smaller tiles
    max_dimension = max(width, height)
    tile_size = int(200 / max_dimension)
    noise = random.uniform(0.8, 1.2)  # Add noise factor
    tile_size = max(5, min(50, int(tile_size * noise)))
    
    colors = list(COLOR_MAP.keys())
    black_probability = 0.7  # Increased probability for black
    other_color_probability = (1 - black_probability) / (len(colors) - 1)
    base_probabilities = [black_probability if color == 'Black' else other_color_probability for color in colors]
    base_probabilities = np.array(base_probabilities)
    base_probabilities /= base_probabilities.sum()
    
    # Ensure probabilities sum to 1
    base_probabilities /= base_probabilities.sum()
    
    # Create transition matrix for Markov chain
    transition_matrix = np.zeros((len(colors), len(colors)))
    black_index = colors.index('Black')
    for i in range(len(colors)):
        for j in range(len(colors)):
            if i == j:
                transition_matrix[i][j] = 0.8 if i == black_index else 0.6  # Higher chance of same color, especially for black
            elif j == black_index:
                transition_matrix[i][j] = 0.3 if i != black_index else 0.1  # Higher chance of transitioning to black
            else:
                transition_matrix[i][j] = (1 - transition_matrix[i, i] - transition_matrix[i, black_index]) / (len(colors) - 2)
    
    grid_array = np.empty((height, width), dtype=object)
    for i in range(height):
        for j in range(width):
            if i == 0 and j == 0:
                grid_array[i][j] = np.random.choice(colors, p=base_probabilities)
            else:
                prev_colors = []
                if j > 0:
                    prev_colors.append(grid_array[i][j-1])
                if i > 0:
                    prev_colors.append(grid_array[i-1][j])
                
                if prev_colors:
                    prev_color = random.choice(prev_colors)
                    prev_color_index = colors.index(prev_color)
                    grid_array[i][j] = np.random.choice(colors, p=transition_matrix[prev_color_index])
                else:
                    grid_array[i][j] = np.random.choice(colors, p=base_probabilities)
    
    return {
        'name': name,
        'width': width,
        'height': height,
        'array': grid_array,
        'tile_size': tile_size
    }

def place_grids(grids, canvas_size, margin, max_attempts=10000):
    occupied_areas = []
    for grid in grids:
        placed = False
        attempts = 0
        while not placed and attempts < max_attempts:
            grid_width_in_pixels = grid['width'] * grid['tile_size']
            grid_height_in_pixels = grid['height'] * grid['tile_size']
            max_x = canvas_size[0] - grid_width_in_pixels - margin
            max_y = canvas_size[1] - grid_height_in_pixels - margin
            if max_x <= margin or max_y <= margin:
                break
            x = random.randint(margin, max_x)
            y = random.randint(margin, max_y)
            new_area = (
                x - margin,
                y - margin,
                x + grid_width_in_pixels + margin,
                y + grid_height_in_pixels + margin
            )
            overlap = any(
                new_area[0] < area[2] and new_area[2] > area[0] and
                new_area[1] < area[3] and new_area[3] > area[1]
                for area in occupied_areas
            )
            if not overlap:
                occupied_areas.append(new_area)
                grid['position'] = (x, y)
                placed = True
            attempts += 1
        if not placed:
            return False
    return True

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

# Constants and Configuration
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

CANVAS_SIZE = (1000, 1000)
MARGIN = 10
MIN_TILE_SIZE = 5
MAX_TILE_SIZE = 50

def generate_grid(name, min_width=3, max_width=20, min_height=3, max_height=20):
    def weighted_random(min_val, max_val):
        weights = [1 / (np.log(i - min_val + 2)) for i in range(min_val, max_val+1)]
        return random.choices(range(min_val, max_val+1), weights=weights)[0]
    
    width = weighted_random(min_width, max_width)
    height = weighted_random(min_height, max_height)
    
    # Calculate tile size inversely proportional to the grid dimensions
    # Larger grids get smaller tiles
    max_dimension = max(width, height)
    tile_size = int(200 / max_dimension)
    noise = random.uniform(0.8, 1.2)  # Add noise factor
    tile_size = max(MIN_TILE_SIZE, min(MAX_TILE_SIZE, int(tile_size * noise)))
    
    colors = list(COLOR_MAP.keys())
    black_probability = 0.7  # Increased probability for black
    other_color_probability = (1 - black_probability) / (len(colors) - 1)
    base_probabilities = [black_probability if color == 'Black' else other_color_probability for color in colors]
    base_probabilities = np.array(base_probabilities)
    base_probabilities /= base_probabilities.sum()
    
    # Ensure probabilities sum to 1
    base_probabilities /= base_probabilities.sum()
    
    # Debug output
    print(f"Base probabilities: {base_probabilities}")
    print(f"Sum of base probabilities: {base_probabilities.sum()}")
    
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

def place_grids(grids, max_attempts=10000):
    occupied_areas = []
    for grid in grids:
        placed = False
        attempts = 0
        while not placed and attempts < max_attempts:
            grid_width_in_pixels = grid['width'] * grid['tile_size']
            grid_height_in_pixels = grid['height'] * grid['tile_size']
            max_x = CANVAS_SIZE[0] - grid_width_in_pixels - MARGIN
            max_y = CANVAS_SIZE[1] - grid_height_in_pixels - MARGIN
            if max_x <= MARGIN or max_y <= MARGIN:
                break
            x = random.randint(MARGIN, max_x)
            y = random.randint(MARGIN, max_y)
            new_area = (
                x - MARGIN,
                y - MARGIN,
                x + grid_width_in_pixels + MARGIN,
                y + grid_height_in_pixels + MARGIN
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

def render_image(grids):
    # Light gray background color
    background_color = (245, 245, 245)
    canvas = Image.new('RGB', CANVAS_SIZE, background_color)
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    for grid in grids:
        x_start, y_start = grid['position']
        tile_size = grid['tile_size']
        bbox = font.getbbox(grid['name'])
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x_start + (grid['width'] * tile_size - text_width) / 2
        text_y = y_start - text_height - 5
        draw.text((text_x, text_y), grid['name'], fill=(0, 0, 0), font=font)

        for i in range(grid['height']):
            for j in range(grid['width']):
                color_name = grid['array'][i][j]
                color = COLOR_MAP[color_name]
                x0 = x_start + j * tile_size
                y0 = y_start + i * tile_size
                x1 = x0 + tile_size
                y1 = y0 + tile_size
                draw.rectangle([x0, y0, x1, y1], fill=color)
    return canvas

# Import question functions
from questions import (
    count_color_in_grid,
    total_color_in_all_grids,
    compare_colors_between_grids,
    which_grid_has_most_color,
    is_color_present_in_grid,
    compare_grid_sizes,
    compare_total_tiles,
    create_meta_question_and_answer
)
from complex_questions import (
    rotate_grid_90_clockwise,
    count_color_patterns,
    find_largest_single_color_area,
    create_complex_meta_question_and_answer
)

def generate_datum():
    min_num_grids = 4
    max_num_grids = 7
    min_grid_width = 3
    max_grid_width = 20
    min_grid_height = 3
    max_grid_height = 20
    for attempt in range(10):
        try:
            num_grids = random.randint(min_num_grids, max_num_grids)
            grids = [generate_grid(
                f"Grid_{i+1}",
                min_width=min_grid_width,
                max_width=max_grid_width,
                min_height=min_grid_height,
                max_height=max_grid_height
                ) for i in range(num_grids)]
            if not place_grids(grids):
                raise Exception("Failed to place all grids")
            image = render_image(grids)

            simple_question_functions = [
                count_color_in_grid,
                total_color_in_all_grids,
                compare_colors_between_grids,
                which_grid_has_most_color,
                is_color_present_in_grid,
                compare_grid_sizes,
                compare_total_tiles
            ]
            complex_question_functions = [
                rotate_grid_90_clockwise,
                count_color_patterns,
                find_largest_single_color_area
            ]
            num_simple_questions = random.randint(3, 5)
            num_complex_questions = random.randint(1, 2)
            question_answer_pairs = []

            for _ in range(num_simple_questions):
                func = random.choice(simple_question_functions)
                if func == count_color_in_grid:
                    grid_name = random.choice([g['name'] for g in grids])
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_name, color)
                elif func == total_color_in_all_grids:
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, color)
                elif func == compare_colors_between_grids:
                    grid_names = random.sample([g['name'] for g in grids], 2)
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_names[0], grid_names[1], color)
                elif func == which_grid_has_most_color:
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, color)
                elif func == is_color_present_in_grid:
                    grid_name = random.choice([g['name'] for g in grids])
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_name, color)
                elif func == compare_grid_sizes:
                    grid_names = random.sample([g['name'] for g in grids], 2)
                    qa = func(grids, grid_names[0], grid_names[1])
                elif func == compare_total_tiles:
                    qa = func(grids)
                
                if qa[0] and qa[1]:
                    question_answer_pairs.append(qa)

            for _ in range(num_complex_questions):
                func = random.choice(complex_question_functions)
                if func == rotate_grid_90_clockwise:
                    grid_name = random.choice([g['name'] for g in grids])
                    qa = func(grids, grid_name)
                elif func == count_color_patterns:
                    grid_name = random.choice([g['name'] for g in grids])
                    colors = random.sample(list(COLOR_MAP.keys()), 2)
                    qa = func(grids, grid_name, colors[0], colors[1])
                elif func == find_largest_single_color_area:
                    grid_name = random.choice([g['name'] for g in grids])
                    qa = func(grids, grid_name)
                
                if qa[0] and qa[1]:
                    question_answer_pairs.append(qa)

            meta_question, meta_answer = create_complex_meta_question_and_answer(question_answer_pairs)
            if not meta_question or not meta_answer:
                raise Exception("No questions or answers generated.")

            for grid in grids:
                print(f"{grid['name']}: Width={grid['width']}, Height={grid['height']}, Tile Size={grid['tile_size']}")

            return image, meta_question, meta_answer
        except Exception as e:
            print(f"Attempt {attempt + 1}: {e}")
            if max_num_grids > min_num_grids + 1:
                max_num_grids -= 1
            if max_grid_width > min_grid_width + 2:
                max_grid_width -= 1
            if max_grid_height > min_grid_height + 2:
                max_grid_height -= 1
    raise Exception("Failed to generate datum after multiple attempts.")

if __name__ == "__main__":
    image, meta_question, meta_answer = generate_datum()
    image.save('output.png')
    print("Meta-Question:")
    print(meta_question)
    print("\nMeta-Answer:")
    print(meta_answer)

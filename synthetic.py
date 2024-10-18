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

CANVAS_SIZE = (1000, 1000)  # Reduced canvas size
MARGIN = 10  # Reduced margin between grids
MIN_TILE_SIZE = 15
MAX_TILE_SIZE = 40

def calculate_tile_size(width, height):
    # Calculate tile size inversely proportional to grid size
    grid_size = width * height
    base_size = int(1600 / grid_size)  # Adjust this factor as needed
    return max(MIN_TILE_SIZE, min(MAX_TILE_SIZE, base_size))

# Function to generate a single grid with variable sizes
def generate_grid(name, min_width=3, max_width=8, min_height=3, max_height=8):
    # Generate random width and height with even higher probability for smaller dimensions
    def weighted_random(min_val, max_val):
        weights = [1/((i-min_val+1)**2) for i in range(min_val, max_val+1)]
        return random.choices(range(min_val, max_val+1), weights=weights)[0]
    
    width = weighted_random(min_width, max_width)
    height = weighted_random(min_height, max_height)
    
    # Calculate tile size based on grid dimensions
    tile_size = calculate_tile_size(width, height)
    
    # Colors and their probabilities
    colors = list(COLOR_MAP.keys())
    probabilities = []
    for color in colors:
        if color == 'Black':
            probabilities.append(0.6)  # 60% probability for black tiles
        else:
            probabilities.append(0.4 / (len(colors) - 1))  # Evenly distribute the remaining probability
    # Ensure the probabilities sum to 1
    probabilities = np.array(probabilities)
    probabilities /= probabilities.sum()
    
    # Assign colors to each tile based on the probabilities
    grid_array = np.random.choice(colors, size=(height, width), p=probabilities)
    
    grid = {
        'name': name,
        'width': width,
        'height': height,
        'array': grid_array,
        'tile_size': tile_size
    }
    return grid

def place_grids(grids, max_attempts=10000):
    occupied_areas = []
    for grid in grids:
        placed = False
        attempts = 0

        while not placed and attempts < max_attempts:
            max_x = CANVAS_SIZE[0] - grid['width'] * grid['tile_size'] - MARGIN
            max_y = CANVAS_SIZE[1] - grid['height'] * grid['tile_size'] - MARGIN
            if max_x <= MARGIN or max_y <= MARGIN:
                # If the grid is too large, reduce its size
                if grid['width'] > 3:
                    grid['width'] -= 1
                if grid['height'] > 3:
                    grid['height'] -= 1
                grid['tile_size'] = calculate_tile_size(grid['width'], grid['height'])
                continue

            x = random.randint(MARGIN, int(max_x))
            y = random.randint(MARGIN, int(max_y))
            new_area = (
                x - MARGIN,
                y - MARGIN,
                x + grid['width'] * grid['tile_size'] + MARGIN,
                y + grid['height'] * grid['tile_size'] + MARGIN
            )
            overlap = False
            for area in occupied_areas:
                if (new_area[0] < area[2] and new_area[2] > area[0] and
                    new_area[1] < area[3] and new_area[3] > area[1]):
                    overlap = True
                    break
            if not overlap:
                occupied_areas.append(new_area)
                grid['position'] = (x, y)
                placed = True
            attempts += 1

        if not placed:
            return False  # Indicate failure to place all grids
    return True  # All grids placed successfully

def render_image(grids):
    canvas = Image.new('RGB', CANVAS_SIZE, (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    for grid in grids:
        x_start, y_start = grid['position']
        tile_size = grid['tile_size']
        # Updated lines using getbbox()
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

# Question methods remain unchanged

from questions import (
    count_color_in_grid,
    total_color_in_all_grids,
    compare_colors_between_grids,
    which_grid_has_most_color,
    is_color_present_in_grid,
    create_meta_question_and_answer
)

def generate_datum():
    min_num_grids = 3
    max_num_grids = 5
    min_grid_width = 3
    max_grid_width = 8
    min_grid_height = 3
    max_grid_height = 8
    for attempt in range(10):  # Increased number of attempts
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

            question_functions = [
                count_color_in_grid,
                total_color_in_all_grids,
                compare_colors_between_grids,
                which_grid_has_most_color,
                is_color_present_in_grid
            ]
            num_questions = random.randint(1, 5)
            question_answer_pairs = []

            for _ in range(num_questions):
                func = random.choice(question_functions)
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
                else:
                    continue
                if qa[0] and qa[1]:
                    question_answer_pairs.append(qa)

            meta_question, meta_answer = create_meta_question_and_answer(question_answer_pairs)
            # Ensure questions and answers are not empty
            if not meta_question or not meta_answer:
                raise Exception("No questions or answers generated.")

            # Optionally, print grid sizes for verification
            for grid in grids:
                print(f"{grid['name']}: Width={grid['width']}, Height={grid['height']}")

            return image, meta_question, meta_answer
        except Exception as e:
            print(f"Attempt {attempt + 1}: {e}")
            # Adjust parameters for the next attempt, but keep within desired ranges
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

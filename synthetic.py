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

TILE_SIZE = 20  # Pixel size of each tile
CANVAS_SIZE = (1200, 1200)  # Canvas size
MARGIN = 20  # Margin between grids

# Function to generate a single grid with variable sizes
def generate_grid(name, min_width=5, max_width=12, min_height=5, max_height=12):
    # Generate random width and height independently
    width = random.randint(min_width, max_width)
    height = random.randint(min_height, max_height)
    
    # Colors and their probabilities
    colors = list(COLOR_MAP.keys())
    probabilities = []
    for color in colors:
        if color == 'Black':
            probabilities.append(0.4)  # 40% probability for black tiles
        else:
            probabilities.append(0.6 / (len(colors) - 1))  # Evenly distribute the remaining probability
    # Ensure the probabilities sum to 1
    probabilities = np.array(probabilities)
    probabilities /= probabilities.sum()
    
    # Assign colors to each tile based on the probabilities
    grid_array = np.random.choice(colors, size=(height, width), p=probabilities)
    
    grid = {
        'name': name,
        'width': width,
        'height': height,
        'array': grid_array
    }
    return grid

def place_grids(grids, max_attempts=5000):
    occupied_areas = []
    for grid in grids:
        placed = False
        attempts = 0

        while not placed and attempts < max_attempts:
            max_x = CANVAS_SIZE[0] - grid['width'] * TILE_SIZE - MARGIN
            max_y = CANVAS_SIZE[1] - grid['height'] * TILE_SIZE - MARGIN
            if max_x <= MARGIN or max_y <= MARGIN:
                raise Exception(f"{grid['name']} is too large for the canvas with the given margins.")
            x = random.randint(MARGIN, int(max_x))
            y = random.randint(MARGIN, int(max_y))
            new_area = (
                x - MARGIN,
                y - MARGIN,
                x + grid['width'] * TILE_SIZE + MARGIN,
                y + grid['height'] * TILE_SIZE + MARGIN
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
            raise Exception(f"Could not place {grid['name']} without overlapping after {max_attempts} attempts.")

def render_image(grids):
    canvas = Image.new('RGB', CANVAS_SIZE, (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    for grid in grids:
        x_start, y_start = grid['position']
        # Updated lines using getbbox()
        bbox = font.getbbox(grid['name'])
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x_start + (grid['width'] * TILE_SIZE - text_width) / 2
        text_y = y_start - text_height - 5
        draw.text((text_x, text_y), grid['name'], fill=(0, 0, 0), font=font)

        for i in range(grid['height']):
            for j in range(grid['width']):
                color_name = grid['array'][i][j]
                color = COLOR_MAP[color_name]
                x0 = x_start + j * TILE_SIZE
                y0 = y_start + i * TILE_SIZE
                x1 = x0 + TILE_SIZE
                y1 = y0 + TILE_SIZE
                draw.rectangle([x0, y0, x1, y1], fill=color)
    return canvas

# Question methods remain unchanged

def count_color_in_grid(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        count = np.sum(grid['array'] == color)
        question = f"How many {color} tiles are in {grid_name}?"
        answer = str(count)
        return question, answer
    return None, None

def total_color_in_all_grids(grids, color):
    total_count = sum(np.sum(grid['array'] == color) for grid in grids)
    question = f"How many {color} tiles are there in all grids?"
    answer = str(total_count)
    return question, answer

def compare_colors_between_grids(grids, grid_name1, grid_name2, color):
    grid1 = next((g for g in grids if g['name'] == grid_name1), None)
    grid2 = next((g for g in grids if g['name'] == grid_name2), None)
    if grid1 and grid2:
        count1 = np.sum(grid1['array'] == color)
        count2 = np.sum(grid2['array'] == color)
        if count1 > count2:
            comparison = "more"
        elif count1 < count2:
            comparison = "less"
        else:
            comparison = "an equal number of"
        question = f"Does {grid_name1} have more {color} tiles than {grid_name2}?"
        answer = f"{grid_name1} has {comparison} {color} tiles compared to {grid_name2}."
        return question, answer
    return None, None

def which_grid_has_most_color(grids, color):
    max_count = -1
    max_grid = None
    for grid in grids:
        count = np.sum(grid['array'] == color)
        if count > max_count:
            max_count = count
            max_grid = grid['name']
    if max_grid:
        question = f"Which grid has the most {color} tiles?"
        answer = f"{max_grid} has the most {color} tiles."
        return question, answer
    else:
        question = f"Which grid has the most {color} tiles?"
        answer = f"No grid has any {color} tiles."
        return question, answer

def is_color_present_in_grid(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        present = np.any(grid['array'] == color)
        question = f"Is there any {color} tile in {grid_name}?"
        answer = "Yes" if present else "No"
        return question, answer
    return None, None

def create_meta_question_and_answer(question_answer_pairs):
    meta_question = " ".join(q for q, a in question_answer_pairs if q)
    meta_answer = " ".join(a for q, a in question_answer_pairs if a)
    return meta_question, meta_answer

def generate_datum():
    min_num_grids = 5
    max_num_grids = 8
    min_grid_width = 5
    max_grid_width = 12
    min_grid_height = 5
    max_grid_height = 12
    for attempt in range(5):  # Increased number of attempts
        try:
            num_grids = random.randint(min_num_grids, max_num_grids)
            grids = [generate_grid(
                f"Grid_{i+1}",
                min_width=min_grid_width,
                max_width=max_grid_width,
                min_height=min_grid_height,
                max_height=max_grid_height
                ) for i in range(num_grids)]
            place_grids(grids)
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

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
CANVAS_SIZE = (800, 800)  # Size of the overall image canvas

# Function to generate a single grid
def generate_grid(name):
    # Random grid size
    width = random.randint(1, 20)
    height = random.randint(1, 20)
    
    # Randomly assign colors to each tile
    colors = list(COLOR_MAP.keys())
    grid_array = np.random.choice(colors, size=(height, width))
    
    grid = {
        'name': name,
        'width': width,
        'height': height,
        'array': grid_array
    }
    return grid

# Function to place grids on the canvas without overlapping
def place_grids(grids):
    occupied_areas = []
    for grid in grids:
        placed = False
        attempts = 0
        max_attempts = 1000  # Prevent infinite loops
        
        while not placed and attempts < max_attempts:
            # Random position
            x = random.randint(0, CANVAS_SIZE[0] - grid['width'] * TILE_SIZE)
            y = random.randint(0, CANVAS_SIZE[1] - grid['height'] * TILE_SIZE)
            new_area = (x, y, x + grid['width'] * TILE_SIZE, y + grid['height'] * TILE_SIZE)
            
            # Check for overlap
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

# Function to render the grids on the image
def render_image(grids):
    canvas = Image.new('RGB', CANVAS_SIZE, (255, 255, 255))  # White background
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    
    for grid in grids:
        x_start, y_start = grid['position']
        # Optionally, draw the grid name
        draw.text((x_start, y_start - 10), grid['name'], fill=(0, 0, 0), font=font)
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

# Question methods
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
    max_count = 0
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
    return None, None

def is_color_present_in_grid(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        present = np.any(grid['array'] == color)
        question = f"Is there any {color} tile in {grid_name}?"
        answer = "Yes" if present else "No"
        return question, answer
    return None, None

# Function to create the meta-question and meta-answer
def create_meta_question_and_answer(question_answer_pairs):
    meta_question = " ".join(q for q, a in question_answer_pairs if q)
    meta_answer = " ".join(a for q, a in question_answer_pairs if a)
    return meta_question, meta_answer

# Function to generate a single datum
def generate_datum():
    # Step 1: Generate grids
    num_grids = random.randint(1, 9)
    grids = [generate_grid(f"Grid_{i+1}") for i in range(num_grids)]
    
    # Step 2: Place grids on canvas
    place_grids(grids)
    
    # Step 3: Render image
    image = render_image(grids)
    
    # Step 4: Generate questions
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
        # Randomly select parameters based on the function
        if func == count_color_in_grid:
            grid_name = random.choice([g['name'] for g in grids])
            color = random.choice(list(COLOR_MAP.keys()))
            qa = func(grids, grid_name, color)
        elif func == total_color_in_all_grids:
            color = random.choice(list(COLOR_MAP.keys()))
            qa = func(grids, color)
        elif func == compare_colors_between_grids:
            if len(grids) >= 2:
                grid_names = random.sample([g['name'] for g in grids], 2)
                color = random.choice(list(COLOR_MAP.keys()))
                qa = func(grids, grid_names[0], grid_names[1], color)
            else:
                continue  # Cannot compare if less than 2 grids
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
    
    # Step 5: Create meta-question and meta-answer
    meta_question, meta_answer = create_meta_question_and_answer(question_answer_pairs)
    
    return image, meta_question, meta_answer

# Main execution
if __name__ == "__main__":
    # Generate a datum
    image, meta_question, meta_answer = generate_datum()
    
    # Save the image and display the meta-question and meta-answer
    image.save('output.png')
    print("Meta-Question:")
    print(meta_question)
    print("\nMeta-Answer:")
    print(meta_answer)

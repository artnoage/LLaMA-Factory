from PIL import Image, ImageDraw, ImageFont
import random
from grid_generator import generate_grid, place_grids, COLOR_MAP

CANVAS_SIZE = (1000, 1000)
MARGIN = 10

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
    count_color_in_row,
    count_color_in_column,
    count_rows_with_color,
    count_columns_with_color,
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
            if not place_grids(grids, CANVAS_SIZE, MARGIN):
                raise Exception("Failed to place all grids")
            image = render_image(grids)

            simple_question_functions = [
                count_color_in_grid,
                total_color_in_all_grids,
                compare_colors_between_grids,
                which_grid_has_most_color,
                is_color_present_in_grid,
                compare_grid_sizes,
                compare_total_tiles,
                count_color_in_row,
                count_color_in_column,
                count_rows_with_color,
                count_columns_with_color
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
                elif func == count_color_in_row:
                    grid_name = random.choice([g['name'] for g in grids])
                    grid = next(g for g in grids if g['name'] == grid_name)
                    row_index = random.randint(0, grid['height'] - 1)
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_name, row_index, color)
                elif func == count_color_in_column:
                    grid_name = random.choice([g['name'] for g in grids])
                    grid = next(g for g in grids if g['name'] == grid_name)
                    column_index = random.randint(0, grid['width'] - 1)
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_name, column_index, color)
                elif func == count_rows_with_color:
                    grid_name = random.choice([g['name'] for g in grids])
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_name, color)
                elif func == count_columns_with_color:
                    grid_name = random.choice([g['name'] for g in grids])
                    color = random.choice(list(COLOR_MAP.keys()))
                    qa = func(grids, grid_name, color)
                
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

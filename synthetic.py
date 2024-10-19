from PIL import Image, ImageDraw, ImageFont
import random
import os
import json
import argparse
from grid_generator import generate_grid, place_grids, COLOR_MAP

CANVAS_SIZE = (1000, 1000)
MARGIN = 10

def render_image(grids, image_path):
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
    canvas.save(image_path)
    return image_path

# Import question functions
from questions import simple_question_functions, create_meta_question_and_answer
from complex_questions import complex_question_functions

def generate_datum(data_id):
    min_num_grids = 2
    max_num_grids = 5
    min_grid_width = 3
    max_grid_width = 10
    min_grid_height = 3
    max_grid_height = 10
    for attempt in range(20):
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
            image_path = f'data/arc_data/{data_id}.png'
            render_image(grids, image_path)

            num_simple_questions = random.randint(2, 3)
            num_complex_questions = random.randint(1, 2)
            question_answer_pairs = []

            for _ in range(num_simple_questions):
                func = random.choice(simple_question_functions)
                qa = func(grids, COLOR_MAP)
                if qa and qa[0] and qa[1]:
                    question_answer_pairs.append(qa)

            for _ in range(num_complex_questions):
                func = random.choice(complex_question_functions)
                qa = func(grids, COLOR_MAP)
                if qa and qa[0] and qa[1]:
                    question_answer_pairs.append(qa)

            if not question_answer_pairs:
                raise Exception("No questions or answers generated.")

            meta_question, meta_answer = create_meta_question_and_answer(question_answer_pairs)
            if not meta_question or not meta_answer:
                raise Exception("Failed to create meta question and answer.")

            for grid in grids:
                print(f"{grid['name']}: Width={grid['width']}, Height={grid['height']}, Tile Size={grid['tile_size']}")

            data = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"<image>{meta_question}"
                    },
                    {
                        "role": "assistant",
                        "content": meta_answer
                    }
                ],
                "images": [
                    image_path
                ]
            }
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1}: {e}")
            if max_num_grids > min_num_grids + 1:
                max_num_grids -= 1
            if max_grid_width > min_grid_width + 1:
                max_grid_width -= 1
            if max_grid_height > min_grid_height + 1:
                max_grid_height -= 1
    raise Exception("Failed to generate datum after multiple attempts.")

def main(n):
    # Create data directory and subdirectories
    os.makedirs('data/arc_data', exist_ok=True)

    all_data = []

    for _ in range(n):
        # Generate a unique identifier for this data point
        data_id = f"data_{random.randint(1000000, 9999999)}"

        data = generate_datum(data_id)
        all_data.append(data)

        print(f"Image saved to: {data['images'][0]}")
        print("Questions and answers generated successfully.")
        print("---")

    # Save all data to a single JSON file
    json_path = 'data/arc.json'
    with open(json_path, 'w') as f:
        json.dump(all_data, f, indent=2)

    print(f"All data saved to: {json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate grid images and questions.')
    parser.add_argument('-n', type=int, default=100, help='Number of datapoints to generate (default: 100)')
    args = parser.parse_args()
    main(args.n)

import random
import os
import json
import argparse
from PIL import Image, ImageDraw
from question_generator import generate_questions

# Define the colors
colors = {
    'Magenta': (255, 0, 255),
    'Dark Red': (139, 0, 0),
    'Red': (255, 0, 0),
    'Orange': (255, 165, 0),
    'Yellow': (255, 255, 0),
    'Green': (0, 128, 0),
    'Light Blue': (173, 216, 230),
    'Blue': (0, 0, 255),
    'Gray': (128, 128, 128),
    'Black': (0, 0, 0),    # Black color
    'Empty': (0, 0, 0)     # Empty is also black
}

# List of color names, excluding 'Empty' to prevent duplicates in random choices
color_names = ['Magenta', 'Dark Red', 'Red', 'Orange', 'Yellow', 'Green', 'Light Blue', 'Blue', 'Gray', 'Black']

# Configuration
TILE_SIZE = 100  # Size of each tile in the meta-grid
MARGIN = 5       # Margin inside each tile
GRID_SIZE_RANGE = range(1, 21)  # Possible sizes for grid dimensions (1 to 20)

# Generate a random size with decreasing probability
def get_random_size():
    sizes = list(GRID_SIZE_RANGE)
    weights = [1.0 / size for size in sizes]  # Weights decrease with size
    return random.choices(sizes, weights=weights)[0]

# Generate the meta-grid and internal grids
def generate_grids():
    meta_grid = []
    for i in range(3):
        row = []
        for j in range(3):
            has_grid = random.random() < 0.9  # 90% chance to have a grid
            if has_grid:
                grid_width = get_random_size()
                grid_height = get_random_size()
                grid = []
                for y in range(grid_height):
                    grid_row = []
                    for x in range(grid_width):
                        # 40% chance to be 'Empty' (Black), 60% chance to be another color
                        if random.random() < 0.4:
                            color = 'Empty'
                        else:
                            color = random.choice(color_names[:-1])  # Exclude 'Black' to prevent confusion with 'Empty'
                        grid_row.append(color)
                    grid.append(grid_row)
                row.append({
                    'grid': grid,
                    'width': grid_width,
                    'height': grid_height,
                    'position': (i, j)  # Keep track of the grid's position
                })
            else:
                row.append(None)
        meta_grid.append(row)
    return meta_grid

# Draw the image
def draw_image(meta_grid):
    img_size = TILE_SIZE * 3
    image = Image.new('RGB', (img_size, img_size), color='white')
    draw = ImageDraw.Draw(image)

    for i, row in enumerate(meta_grid):
        for j, tile in enumerate(row):
            x_offset = j * TILE_SIZE
            y_offset = i * TILE_SIZE
            # No border drawing since meta-grid lines are invisible
            if tile:
                grid = tile['grid']
                grid_width = tile['width']
                grid_height = tile['height']

                available_width = TILE_SIZE - 2 * MARGIN
                available_height = TILE_SIZE - 2 * MARGIN

                if grid_width >= grid_height:
                    # Scale cell size based on width
                    cell_size = available_width / grid_width
                    total_grid_height = cell_size * grid_height
                    grid_x_start = x_offset + MARGIN
                    grid_y_start = y_offset + MARGIN + (available_height - total_grid_height) / 2
                else:
                    # Scale cell size based on height
                    cell_size = available_height / grid_height
                    total_grid_width = cell_size * grid_width
                    grid_x_start = x_offset + MARGIN + (available_width - total_grid_width) / 2
                    grid_y_start = y_offset + MARGIN

                for y in range(grid_height):
                    for x in range(grid_width):
                        cell_color = colors[grid[y][x]]
                        cell_x = grid_x_start + x * cell_size
                        cell_y = grid_y_start + y * cell_size
                        draw.rectangle([
                            cell_x, cell_y,
                            cell_x + cell_size, cell_y + cell_size
                        ], fill=cell_color)
    return image

# Main function
def main(n):
    # Create data directory and subdirectories
    os.makedirs('data/arc_data', exist_ok=True)

    all_data = []

    for _ in range(n):
        # Generate a unique identifier for this data point
        data_id = f"data_{random.randint(1000000, 9999999)}"

        meta_grid = generate_grids()
        image = draw_image(meta_grid)
        
        # Save the image
        image_path = f'data/arc_data/{data_id}.png'
        image.save(image_path)

        questions, answers = generate_questions(meta_grid)
        
        # Prepare data for JSON
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": f"<image>{questions}"
                },
                {
                    "role": "assistant",
                    "content": answers
                }
            ],
            "images": [
                image_path
            ]
        }

        all_data.append(data)

        print(f"Image saved to: {image_path}")
        print("Questions and answers generated successfully.")
        print("---")

    # Save all data to a single JSON file
    json_path = 'data/arc.json'
    with open(json_path, 'w') as f:
        json.dump(all_data, f, indent=2)

    print(f"All data saved to: {json_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate grid images and questions.')
    parser.add_argument('-n', type=int, default=100, help='Number of datapoints to generate (default: 100)')
    args = parser.parse_args()
    main(args.n)

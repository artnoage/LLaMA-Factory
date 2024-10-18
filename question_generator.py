import random

def get_position_description(row, col):
    positions = {
        (0, 0): "top left", (0, 1): "top center", (0, 2): "top right",
        (1, 0): "middle left", (1, 1): "center", (1, 2): "middle right",
        (2, 0): "bottom left", (2, 1): "bottom center", (2, 2): "bottom right"
    }
    return positions.get((row, col), f"row {row + 1}, column {col + 1}")

def find_grid_with_most_tiles(meta_grid):
    max_tiles = 0
    max_tile_position = None
    for i, row in enumerate(meta_grid):
        for j, tile in enumerate(row):
            if tile:
                tile_count = tile['width'] * tile['height']
                if tile_count > max_tiles:
                    max_tiles = tile_count
                    max_tile_position = (i, j)
    return max_tile_position, max_tiles

def find_grid_with_most_colors(meta_grid):
    max_colors = 0
    max_color_position = None
    for i, row in enumerate(meta_grid):
        for j, tile in enumerate(row):
            if tile:
                unique_colors = set(cell for row in tile['grid'] for cell in row if cell != 'Empty')
                if len(unique_colors) > max_colors:
                    max_colors = len(unique_colors)
                    max_color_position = (i, j)
    return max_color_position, max_colors

import random

def generate_questions(meta_grid):
    all_questions = [
        "How many grids do you see?",
        "How many of each color are there in total?",
        "What are the dimensions of each grid?",
        "Which grid has the most tiles?",
        "Which grid has the most unique colors?",
        "How many empty grids are there?",
        "What is the most common color across all grids?",
        "Are there any completely empty grids (all tiles are 'Empty')?",
        "What is the total number of colored tiles across all grids?",
        "What is the ratio of colored tiles to empty tiles?",
        "What is the average number of tiles per non-empty grid?",
        "How many grids have more colored tiles than empty tiles?",
        "What is the total perimeter of all grids combined?",
        "What is the most common grid size?",
        "How many grids are square (equal width and height)?",
        "What is the total area of all grids combined?",
        "What percentage of the total area is colored?",
        "How many grids have at least one tile of every color?",
        "What is the color diversity index (number of colors used / total number of colors)?",
        "How many grids have a majority (>50%) of a single color?",
        "What is the largest difference in tile count between any two colors?",
        "How many grids have a perfect color balance (equal number of tiles for each color used)?",
        "What is the average number of colors per grid?",
        "How many grids have a color pattern (any repeating sequence of colors)?",
        "What is the most common color in the corners of all grids?",
        "How many grids have a diagonal symmetry?",
        "What is the total number of unique color combinations across all grids?",
        "How many grids have a 'checkerboard' pattern (alternating colors in a regular pattern)?",
        "What is the 'color entropy' (measure of color disorder) across all grids?",
        "Are there any interesting patterns or observations you can make about the grids?"
    ]

    # Choose 5 random questions
    selected_questions = random.sample(all_questions, 5)
    
    questions = "Please analyze the image and answer the following questions:\n\n" + "\n".join(f"{i+1}. {q}" for i, q in enumerate(selected_questions))

    # Calculate all the answers
    grid_count = sum(1 for row in meta_grid for tile in row if tile)
    non_empty_grids = [(i, j, tile) for i, row in enumerate(meta_grid) for j, tile in enumerate(row) if tile]
    color_names = ['Magenta', 'Dark Red', 'Red', 'Orange', 'Yellow', 'Green', 'Light Blue', 'Blue', 'Gray', 'Black', 'Empty']
    total_counts = {color: sum(sum(1 for cell in row if cell == color) for tile in row if tile for row in tile['grid']) for color in color_names for row in meta_grid}
    max_tile_position, max_tiles = find_grid_with_most_tiles(meta_grid)
    max_color_position, max_colors = find_grid_with_most_colors(meta_grid)
    empty_grid_count = sum(1 for row in meta_grid for tile in row if tile is None)
    most_common_color = max(total_counts, key=total_counts.get) if sum(total_counts.values()) > 0 else None
    completely_empty_grids = sum(1 for row in meta_grid for tile in row if tile and all(cell == 'Empty' for row in tile['grid'] for cell in row))
    total_colored_tiles = sum(count for color, count in total_counts.items() if color != 'Empty')
    empty_tiles = total_counts['Empty']
    ratio = total_colored_tiles / empty_tiles if empty_tiles > 0 else "undefined"
    non_empty_grid_count = sum(1 for row in meta_grid for tile in row if tile)
    avg_tiles = sum(tile['width'] * tile['height'] for row in meta_grid for tile in row if tile) / non_empty_grid_count if non_empty_grid_count > 0 else 0
    grids_more_colored = sum(1 for row in meta_grid for tile in row if tile and sum(1 for r in tile['grid'] for c in r if c != 'Empty') > sum(1 for r in tile['grid'] for c in r if c == 'Empty'))
    total_perimeter = sum(2 * (tile['width'] + tile['height']) for row in meta_grid for tile in row if tile)
    grid_sizes = [(tile['width'], tile['height']) for row in meta_grid for tile in row if tile]
    most_common_size = max(set(grid_sizes), key=grid_sizes.count) if grid_sizes else None
    square_grids = sum(1 for row in meta_grid for tile in row if tile and tile['width'] == tile['height'])
    total_area = sum(tile['width'] * tile['height'] for row in meta_grid for tile in row if tile)
    percent_colored = (total_colored_tiles / total_area * 100) if total_area > 0 else 0
    grids_all_colors = sum(1 for row in meta_grid for tile in row if tile and all(any(c == color for r in tile['grid'] for c in r) for color in color_names if color != 'Empty'))
    colors_used = sum(1 for color, count in total_counts.items() if count > 0 and color != 'Empty')
    diversity_index = colors_used / len(color_names[:-1])  # Excluding 'Empty'
    grids_majority_color = sum(1 for row in meta_grid for tile in row if tile and any(sum(1 for r in tile['grid'] for c in r if c == color) > (tile['width'] * tile['height'] / 2) for color in color_names))
    color_counts = [count for color, count in total_counts.items() if color != 'Empty']
    max_diff = max(color_counts) - min(color_counts) if color_counts else 0
    balanced_grids = sum(1 for row in meta_grid for tile in row if tile and len(set(sum(1 for r in tile['grid'] for c in r if c == color) for color in color_names if color != 'Empty')) == 1)
    avg_colors_per_grid = sum(len(set(c for r in tile['grid'] for c in r if c != 'Empty')) for row in meta_grid for tile in row if tile) / non_empty_grid_count if non_empty_grid_count > 0 else 0
    
    def has_pattern(grid):
        for row in grid:
            if len(set(row)) < len(row):
                return True
        for col in zip(*grid):
            if len(set(col)) < len(col):
                return True
        return False
    
    grids_with_pattern = sum(1 for row in meta_grid for tile in row if tile and has_pattern(tile['grid']))
    corner_colors = [tile['grid'][0][0] for row in meta_grid for tile in row if tile] + \
                    [tile['grid'][0][-1] for row in meta_grid for tile in row if tile] + \
                    [tile['grid'][-1][0] for row in meta_grid for tile in row if tile] + \
                    [tile['grid'][-1][-1] for row in meta_grid for tile in row if tile]
    most_common_corner = max(set(corner_colors), key=corner_colors.count) if corner_colors else None
    
    def has_diagonal_symmetry(grid):
        height = len(grid)
        width = len(grid[0]) if grid else 0
        if height != width:
            return False  # Non-square grids can't have diagonal symmetry
        return all(grid[i][j] == grid[j][i] for i in range(height) for j in range(i+1, width))
    
    diagonal_symmetric_grids = sum(1 for row in meta_grid for tile in row if tile and has_diagonal_symmetry(tile['grid']))
    unique_combinations = set(tuple(sorted(set(c for r in tile['grid'] for c in r if c != 'Empty'))) for row in meta_grid for tile in row if tile)
    
    def is_checkerboard(grid):
        colors = list(set(c for row in grid for c in row if c != 'Empty'))
        if len(colors) != 2:
            return False
        return all((i + j) % 2 == grid[i][j] == colors[0] or (i + j) % 2 != grid[i][j] == colors[1] for i in range(len(grid)) for j in range(len(grid[0])))
    
    checkerboard_grids = sum(1 for row in meta_grid for tile in row if tile and is_checkerboard(tile['grid']))
    
    from math import log2
    
    def color_entropy(grid):
        flat_grid = [c for row in grid for c in row if c != 'Empty']
        total = len(flat_grid)
        probabilities = [flat_grid.count(c) / total for c in set(flat_grid)]
        return -sum(p * log2(p) for p in probabilities) if probabilities else 0
    
    total_entropy = sum(color_entropy(tile['grid']) for row in meta_grid for tile in row if tile)

    all_answers = [
        f"There are {grid_count} grids visible in the image.",
        f"The total count for each color is: {', '.join(f'{color}: {count}' for color, count in total_counts.items())}.",
        f"The dimensions of each grid are: {', '.join(f'{get_position_description(*tile[0:2])}: {tile[2]['width']}x{tile[2]['height']}' for tile in non_empty_grids)}.",
        f"The {get_position_description(*max_tile_position)} grid has the most tiles with {max_tiles} tiles.",
        f"The {get_position_description(*max_color_position)} grid has the most unique colors with {max_colors} different colors.",
        f"There are {empty_grid_count} empty grids in the image.",
        f"The most common color across all grids is {most_common_color} with {total_counts[most_common_color]} occurrences.",
        f"{'Yes, there are ' + str(completely_empty_grids) + ' completely empty grid(s).' if completely_empty_grids > 0 else 'No, there are no completely empty grids.'}",
        f"The total number of colored tiles across all grids is {total_colored_tiles}.",
        "The ratio of colored tiles to empty tiles is approximately {:.2f} to 1.".format(ratio),
        f"The average number of tiles per non-empty grid is approximately {avg_tiles:.2f}.",
        f"{grids_more_colored} grids have more colored tiles than empty tiles.",
        f"The total perimeter of all grids combined is {total_perimeter} units.",
        f"The most common grid size is {f'{most_common_size[0]}x{most_common_size[1]}' if most_common_size else 'No grids present'}.",
        f"There are {square_grids} square grids (equal width and height).",
        f"The total area of all grids combined is {total_area} units.",
        f"{percent_colored:.2f}% of the total area is colored.",
        f"{grids_all_colors} grids have at least one tile of every color.",
        f"The color diversity index is {diversity_index:.2f}.",
        f"{grids_majority_color} grids have a majority (>50%) of a single color.",
        f"The largest difference in tile count between any two colors is {max_diff}.",
        f"{balanced_grids} grids have a perfect color balance (equal number of tiles for each color used).",
        f"The average number of colors per grid is {avg_colors_per_grid:.2f}.",
        f"{grids_with_pattern} grids have a color pattern (any repeating sequence of colors).",
        f"The most common color in the corners of all grids is {most_common_corner if most_common_corner else 'No grids present'}.",
        f"{diagonal_symmetric_grids} grids have a diagonal symmetry.",
        f"The total number of unique color combinations across all grids is {len(unique_combinations)}.",
        f"{checkerboard_grids} grids have a 'checkerboard' pattern (alternating colors in a regular pattern).",
        f"The 'color entropy' (measure of color disorder) across all grids is {total_entropy:.2f}.",
        f"Some interesting observations about the grids:\n"
        f"   - The image contains a diverse set of {grid_count} grids with varying sizes and color distributions.\n"
        f"   - The most common color ({most_common_color}) appears {total_counts[most_common_color]} times, while the rarest non-empty color appears {min(count for color, count in total_counts.items() if color != 'Empty' and count > 0)} times.\n"
        f"   - {grids_more_colored} out of {grid_count} grids have more colored tiles than empty tiles, suggesting a tendency towards colorful designs.\n"
        f"   - The presence of {diagonal_symmetric_grids} grids with diagonal symmetry and {checkerboard_grids} grids with a checkerboard pattern indicates some level of structured design in the image.\n"
        f"   - The color entropy of {total_entropy:.2f} suggests a moderate level of color disorder across the grids, balancing between uniformity and randomness.\n"
        f"   - With {len(unique_combinations)} unique color combinations, the image showcases a wide variety of color arrangements across the grids."
    ]

    # Select answers corresponding to the selected questions
    selected_answers = [all_answers[all_questions.index(q)] for q in selected_questions]
    
    answers = "Certainly! I'll analyze the image and answer your questions:\n\n" + "\n".join(f"{i+1}. {a}" for i, a in enumerate(selected_answers))

    return questions, answers

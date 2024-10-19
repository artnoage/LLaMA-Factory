import numpy as np
import random
from color_map import COLOR_MAP

def rotate_grid_90_clockwise(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rotated_array = np.rot90(grid['array'], k=-1).tolist()
        stringified_array = str([[str(color) for color in row] for row in rotated_array])
        question = f"What is the 90-degree clockwise rotation of {grid_name}?"
        answer = f"The 90-degree clockwise rotation of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def rotate_grid_180(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rotated_array = np.rot90(grid['array'], k=2).tolist()
        stringified_array = str([[str(color) for color in row] for row in rotated_array])
        question = f"What is the 180-degree rotation of {grid_name}?"
        answer = f"The 180-degree rotation of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def rotate_grid_270_clockwise(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rotated_array = np.rot90(grid['array'], k=-3).tolist()
        stringified_array = str([[str(color) for color in row] for row in rotated_array])
        question = f"What is the 270-degree clockwise rotation of {grid_name}?"
        answer = f"The 270-degree clockwise rotation of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def reflect_grid_horizontally(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        reflected_array = np.fliplr(grid['array']).tolist()
        stringified_array = str([[str(color) for color in row] for row in reflected_array])
        question = f"What is the horizontal reflection of {grid_name}?"
        answer = f"The horizontal reflection of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def reflect_grid_vertically(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        reflected_array = np.flipud(grid['array']).tolist()
        stringified_array = str([[str(color) for color in row] for row in reflected_array])
        question = f"What is the vertical reflection of {grid_name}?"
        answer = f"The vertical reflection of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def count_color_patterns(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        color1, color2 = random.sample(list(COLOR_MAP.keys()), 2)
        array = grid['array']
        count = 0
        for i in range(array.shape[0]):
            for j in range(array.shape[1] - 1):
                if array[i][j] == color1 and array[i][j+1] == color2:
                    count += 1
        question = f"How many times does the pattern '{color1} followed by {color2}' appear horizontally in {grid_name}?"
        answer = f"The pattern '{color1} followed by {color2}' appears {count} times horizontally in {grid_name}."
        return question, answer
    return None, None

def find_largest_single_color_area(grids, COLOR_MAP):
    def dfs(i, j, color, visited):
        if i < 0 or i >= height or j < 0 or j >= width or visited[i][j] or array[i][j] != color:
            return 0
        visited[i][j] = True
        area = 1
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            area += dfs(i + di, j + dj, color, visited)
        return area

    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array']
        height, width = array.shape
        visited = [[False for _ in range(width)] for _ in range(height)]
        max_area = 0
        max_color = None

        for i in range(height):
            for j in range(width):
                if not visited[i][j]:
                    color = array[i][j]
                    area = dfs(i, j, color, visited)
                    if area > max_area:
                        max_area = area
                        max_color = color

        if max_color == 'Empty':
            question = f"What is the largest contiguous area of empty tiles in {grid_name}?"
            answer = f"The largest contiguous area of empty tiles in {grid_name} is {max_area} tiles."
        else:
            question = f"What is the largest contiguous area of a single color in {grid_name}, and what color is it?"
            answer = f"The largest contiguous area in {grid_name} is {max_area} tiles of {max_color}."
        return question, answer
    return None, None

def generate_grid_code(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array'].tolist()
        code = f"import numpy as np\n\n"
        code += f"def generate_{grid_name.lower()}():\n"
        code += f"    return np.array({array})\n"
        stringified_code = code.replace('\n', '\\n')
        question = f"What is the code to reproduce the grid {grid_name}?"
        answer = f"The code to reproduce the grid {grid_name} is: {stringified_code}"
        return question, answer
    return None, None

def create_complex_meta_question_and_answer(question_answer_pairs):
    meta_question = "Answer the following questions about the grids: " + " ".join(q for q, a in question_answer_pairs if q)
    meta_answer = " ".join(a for q, a in question_answer_pairs if a)
    return meta_question, meta_answer

def count_diagonal_color_pattern(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        color1, color2 = random.sample(list(COLOR_MAP.keys()), 2)
        array = grid['array']
        height, width = array.shape
        count = 0
        for i in range(height - 1):
            for j in range(width - 1):
                if array[i][j] == color1 and array[i+1][j+1] == color2:
                    count += 1
        question = f"How many times does the diagonal pattern '{color1} followed by {color2}' appear in {grid_name}?"
        answer = f"The diagonal pattern '{color1} followed by {color2}' appears {count} times in {grid_name}."
        return question, answer
    return None, None

def calculate_color_density(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    color = random.choice(list(COLOR_MAP.keys()))
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array']
        total_tiles = array.size
        color_count = np.sum(array == color)
        density = (color_count / total_tiles) * 100
        question = f"What is the density of {color} tiles in {grid_name}?"
        answer = f"The density of {color} tiles in {grid_name} is {density:.2f}%."
        return question, answer
    return None, None

def find_color_islands(grids, COLOR_MAP):
    def dfs(i, j, visited):
        if i < 0 or i >= height or j < 0 or j >= width or visited[i][j] or array[i][j] != color:
            return
        visited[i][j] = True
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(i + di, j + dj, visited)

    grid_name = random.choice([g['name'] for g in grids])
    color = random.choice(list(COLOR_MAP.keys()))
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array']
        height, width = array.shape
        visited = np.zeros((height, width), dtype=bool)
        islands = 0

        for i in range(height):
            for j in range(width):
                if array[i][j] == color and not visited[i][j]:
                    dfs(i, j, visited)
                    islands += 1

        question = f"How many isolated 'islands' of {color} exist in {grid_name}?"
        answer = f"There are {islands} isolated 'islands' of {color} in {grid_name}."
        return question, answer
    return None, None

def analyze_color_distribution(grids, COLOR_MAP):
    grid_name = random.choice([g['name'] for g in grids])
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array']
        unique, counts = np.unique(array, return_counts=True)
        total_tiles = array.size
        distribution = {color: count/total_tiles for color, count in zip(unique, counts)}
        
        # Calculate the entropy of the distribution
        entropy = -sum(p * np.log2(p) for p in distribution.values() if p > 0)
        max_entropy = np.log2(len(unique))
        normalized_entropy = entropy / max_entropy

        if normalized_entropy > 0.9:
            distribution_type = "highly uniform"
        elif normalized_entropy > 0.7:
            distribution_type = "moderately uniform"
        elif normalized_entropy > 0.5:
            distribution_type = "slightly clustered"
        else:
            distribution_type = "highly clustered"

        question = f"Is the distribution of colors in {grid_name} uniform or clustered?"
        answer = f"The distribution of colors in {grid_name} is {distribution_type}."
        return question, answer
    return None, None

def compare_grid_complexity(grids, COLOR_MAP):
    def count_transitions(grid):
        array = grid['array']
        horizontal = np.sum(array[:, :-1] != array[:, 1:])
        vertical = np.sum(array[:-1, :] != array[1:, :])
        return horizontal + vertical

    if len(grids) < 2:
        return None, None
    grid_name1, grid_name2 = random.sample([g['name'] for g in grids], 2)
    grid1 = next((g for g in grids if g['name'] == grid_name1), None)
    grid2 = next((g for g in grids if g['name'] == grid_name2), None)
    if grid1 and grid2:
        transitions1 = count_transitions(grid1)
        transitions2 = count_transitions(grid2)
        question = f"Which grid has more color transitions: {grid_name1} or {grid_name2}?"
        if transitions1 > transitions2:
            answer = f"{grid_name1} has more color transitions ({transitions1}) compared to {grid_name2} ({transitions2})."
        elif transitions2 > transitions1:
            answer = f"{grid_name2} has more color transitions ({transitions2}) compared to {grid_name1} ({transitions1})."
        else:
            answer = f"Both {grid_name1} and {grid_name2} have the same number of color transitions ({transitions1})."
        return question, answer
    return None, None

def find_color_path(grids, COLOR_MAP):
    def dfs(i, j, visited, target):
        if i < 0 or i >= height or j < 0 or j >= width or visited[i][j] or array[i][j] != color:
            return False
        if (j == width - 1 and target == 'right') or (i == height - 1 and target == 'bottom'):
            return True
        visited[i][j] = True
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if dfs(i + di, j + dj, visited, target):
                return True
        return False

    grid_name = random.choice([g['name'] for g in grids])
    color = random.choice(list(COLOR_MAP.keys()))
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array']
        height, width = array.shape
        
        # Check for left to right path
        visited_lr = np.zeros((height, width), dtype=bool)
        lr_path_exists = any(dfs(i, 0, visited_lr, 'right') for i in range(height) if array[i][0] == color)
        
        # Check for top to bottom path
        visited_tb = np.zeros((height, width), dtype=bool)
        tb_path_exists = any(dfs(0, j, visited_tb, 'bottom') for j in range(width) if array[0][j] == color)

        question = f"Is there a continuous path of {color} from left to right or top to bottom in {grid_name}?"
        if lr_path_exists and tb_path_exists:
            answer = f"Yes, there is a continuous path of {color} from both left to right and top to bottom in {grid_name}."
        elif lr_path_exists:
            answer = f"Yes, there is a continuous path of {color} from left to right in {grid_name}, but not from top to bottom."
        elif tb_path_exists:
            answer = f"Yes, there is a continuous path of {color} from top to bottom in {grid_name}, but not from left to right."
        else:
            answer = f"No, there is no continuous path of {color} from left to right or top to bottom in {grid_name}."
        return question, answer
    return None, None

complex_question_functions = [
    rotate_grid_90_clockwise,
    rotate_grid_180,
    rotate_grid_270_clockwise,
    reflect_grid_horizontally,
    reflect_grid_vertically,
    count_color_patterns,
    find_largest_single_color_area,
    generate_grid_code,
    count_diagonal_color_pattern,
    calculate_color_density,
    find_color_islands,
    analyze_color_distribution,
    compare_grid_complexity,
    find_color_path
]

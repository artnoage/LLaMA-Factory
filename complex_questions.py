import numpy as np

def rotate_grid_90_clockwise(grids, grid_name):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rotated_array = np.rot90(grid['array'], k=-1).tolist()
        stringified_array = str([[str(color) for color in row] for row in rotated_array])
        question = f"What is the 90-degree clockwise rotation of {grid_name}?"
        answer = f"The 90-degree clockwise rotation of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def rotate_grid_180(grids, grid_name):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rotated_array = np.rot90(grid['array'], k=2).tolist()
        stringified_array = str([[str(color) for color in row] for row in rotated_array])
        question = f"What is the 180-degree rotation of {grid_name}?"
        answer = f"The 180-degree rotation of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def rotate_grid_270_clockwise(grids, grid_name):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rotated_array = np.rot90(grid['array'], k=-3).tolist()
        stringified_array = str([[str(color) for color in row] for row in rotated_array])
        question = f"What is the 270-degree clockwise rotation of {grid_name}?"
        answer = f"The 270-degree clockwise rotation of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def reflect_grid_horizontally(grids, grid_name):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        reflected_array = np.fliplr(grid['array']).tolist()
        stringified_array = str([[str(color) for color in row] for row in reflected_array])
        question = f"What is the horizontal reflection of {grid_name}?"
        answer = f"The horizontal reflection of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def reflect_grid_vertically(grids, grid_name):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        reflected_array = np.flipud(grid['array']).tolist()
        stringified_array = str([[str(color) for color in row] for row in reflected_array])
        question = f"What is the vertical reflection of {grid_name}?"
        answer = f"The vertical reflection of {grid_name} is: {stringified_array}"
        return question, answer
    return None, None

def count_color_patterns(grids, grid_name, color1, color2):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
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

def find_largest_single_color_area(grids, grid_name):
    def dfs(i, j, color, visited):
        if i < 0 or i >= height or j < 0 or j >= width or visited[i][j] or array[i][j] != color:
            return 0
        visited[i][j] = True
        area = 1
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            area += dfs(i + di, j + dj, color, visited)
        return area

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

        question = f"What is the largest contiguous area of a single color in {grid_name}, and what color is it?"
        answer = f"The largest contiguous area in {grid_name} is {max_area} tiles of {max_color}."
        return question, answer
    return None, None

def generate_grid_code(grids, grid_name):
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

def count_diagonal_color_pattern(grids, grid_name, color1, color2):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
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

def calculate_color_density(grids, grid_name, color):
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

def compare_grid_perimeter_colors(grids, grid_name1, grid_name2):
    def get_perimeter_colors(grid):
        array = grid['array']
        perimeter = np.concatenate([array[0], array[-1], array[1:-1, 0], array[1:-1, -1]])
        return perimeter

    grid1 = next((g for g in grids if g['name'] == grid_name1), None)
    grid2 = next((g for g in grids if g['name'] == grid_name2), None)
    if grid1 and grid2:
        perimeter1 = get_perimeter_colors(grid1)
        perimeter2 = get_perimeter_colors(grid2)
        common_color1 = np.bincount(perimeter1).argmax()
        common_color2 = np.bincount(perimeter2).argmax()
        question = f"What is the most common color on the perimeter of {grid_name1} and {grid_name2}?"
        answer = f"The most common color on the perimeter of {grid_name1} is {common_color1}, and for {grid_name2} it is {common_color2}."
        return question, answer
    return None, None

def find_color_islands(grids, grid_name, color):
    def dfs(i, j, visited):
        if i < 0 or i >= height or j < 0 or j >= width or visited[i][j] or array[i][j] != color:
            return
        visited[i][j] = True
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(i + di, j + dj, visited)

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

def analyze_color_distribution(grids, grid_name):
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

def compare_grid_complexity(grids, grid_name1, grid_name2):
    def count_transitions(grid):
        array = grid['array']
        horizontal = np.sum(array[:, :-1] != array[:, 1:])
        vertical = np.sum(array[:-1, :] != array[1:, :])
        return horizontal + vertical

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

def find_color_path(grids, grid_name, color):
    def dfs(i, j, visited):
        if i < 0 or i >= height or j < 0 or j >= width or visited[i][j] or array[i][j] != color:
            return False
        if j == width - 1:
            return True
        visited[i][j] = True
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if dfs(i + di, j + dj, visited):
                return True
        return False

    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        array = grid['array']
        height, width = array.shape
        visited = np.zeros((height, width), dtype=bool)

        path_exists = any(dfs(i, 0, visited) for i in range(height) if array[i][0] == color)

        question = f"Is there a continuous path of {color} from left to right in {grid_name}?"
        answer = f"{'Yes' if path_exists else 'No'}, there {'is' if path_exists else 'is not'} a continuous path of {color} from left to right in {grid_name}."
        return question, answer
    return None, None

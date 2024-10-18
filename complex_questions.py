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

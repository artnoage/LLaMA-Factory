import numpy as np

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

import numpy as np

def count_color_in_grid(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        count = np.sum(grid['array'] == color)
        question = f"How many {color} tiles are in {grid_name}?"
        answer = f"There are {count} {color} tiles in {grid_name}."
        return question, answer
    return None, None

def total_color_in_all_grids(grids, color):
    total_count = sum(np.sum(grid['array'] == color) for grid in grids)
    question = f"How many {color} tiles are there in all grids?"
    answer = f"There are a total of {total_count} {color} tiles across all grids."
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
            comparison = "fewer"
        else:
            comparison = "the same number of"
        question = f"Does {grid_name1} have more {color} tiles than {grid_name2}?"
        answer = f"{grid_name1} has {comparison} {color} tiles compared to {grid_name2}. Specifically, {grid_name1} has {count1} {color} tiles, while {grid_name2} has {count2} {color} tiles."
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
        answer = f"{max_grid} has the most {color} tiles with a total of {max_count} {color} tiles."
        return question, answer
    else:
        question = f"Which grid has the most {color} tiles?"
        answer = f"No grid has any {color} tiles. The color {color} is not present in any of the grids."
        return question, answer

def is_color_present_in_grid(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        present = np.any(grid['array'] == color)
        question = f"Is there any {color} tile in {grid_name}?"
        if present:
            count = np.sum(grid['array'] == color)
            answer = f"Yes, there are {color} tiles in {grid_name}. Specifically, there are {count} {color} tiles in this grid."
        else:
            answer = f"No, there are no {color} tiles in {grid_name}."
        return question, answer
    return None, None

def compare_grid_sizes(grids, grid_name1, grid_name2):
    grid1 = next((g for g in grids if g['name'] == grid_name1), None)
    grid2 = next((g for g in grids if g['name'] == grid_name2), None)
    if grid1 and grid2:
        size1 = grid1['width'] * grid1['height']
        size2 = grid2['width'] * grid2['height']
        question = f"Which grid is larger in terms of total tiles: {grid_name1} or {grid_name2}?"
        if size1 > size2:
            answer = f"{grid_name1} is larger with {size1} tiles, compared to {grid_name2} with {size2} tiles."
        elif size2 > size1:
            answer = f"{grid_name2} is larger with {size2} tiles, compared to {grid_name1} with {size1} tiles."
        else:
            answer = f"Both {grid_name1} and {grid_name2} have the same number of tiles: {size1}."
        return question, answer
    return None, None

def compare_total_tiles(grids):
    total_tiles = sum(grid['width'] * grid['height'] for grid in grids)
    largest_grid = max(grids, key=lambda g: g['width'] * g['height'])
    largest_grid_tiles = largest_grid['width'] * largest_grid['height']
    question = "How many total tiles are there across all grids, and which grid has the most tiles?"
    answer = f"There are {total_tiles} tiles in total across all grids. The grid with the most tiles is {largest_grid['name']} with {largest_grid_tiles} tiles."
    return question, answer

def count_color_in_row(grids, grid_name, row_index, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid and 0 <= row_index < grid['height']:
        count = np.sum(grid['array'][row_index] == color)
        question = f"How many {color} tiles are in row {row_index + 1} of {grid_name}?"
        answer = f"There are {count} {color} tiles in row {row_index + 1} of {grid_name}."
        return question, answer
    return None, None

def count_color_in_column(grids, grid_name, column_index, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid and 0 <= column_index < grid['width']:
        count = np.sum(grid['array'][:, column_index] == color)
        question = f"How many {color} tiles are in column {column_index + 1} of {grid_name}?"
        answer = f"There are {count} {color} tiles in column {column_index + 1} of {grid_name}."
        return question, answer
    return None, None

def count_rows_with_color(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        rows_with_color = np.sum(np.any(grid['array'] == color, axis=1))
        question = f"In how many rows of {grid_name} does the color {color} appear?"
        answer = f"The color {color} appears in {rows_with_color} rows of {grid_name}."
        return question, answer
    return None, None

def count_columns_with_color(grids, grid_name, color):
    grid = next((g for g in grids if g['name'] == grid_name), None)
    if grid:
        columns_with_color = np.sum(np.any(grid['array'] == color, axis=0))
        question = f"In how many columns of {grid_name} does the color {color} appear?"
        answer = f"The color {color} appears in {columns_with_color} columns of {grid_name}."
        return question, answer
    return None, None

def create_meta_question_and_answer(question_answer_pairs):
    meta_question = " ".join(q for q, a in question_answer_pairs if q)
    meta_answer = " ".join(a for q, a in question_answer_pairs if a)
    return meta_question, meta_answer

assignments = []
cols = '123456789'
rows = 'ABCDEFGHI'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# Diagonal
diagonal1 = [[rows[i]+cols[i] for i in range(9)]]
#diagonal2 = [[rows[-(i+1)]+cols[-(i+1)] for i in range(9)]]
diagonal2 = [[rows[i]+cols[::-1][i] for i in range(9)]]
unitlist += diagonal1 + diagonal2


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    two_digit_boxes = [box for box in values.keys() if len(values[box]) == 2]
    naked_twins = []
    for box1 in two_digit_boxes:
        for box2 in peers[box1]:
            if len(values[box2]) == 2 and set(values[box1]) == set(values[box2]):
                naked_twins.append([box1, box2])

    for naked_twin in naked_twins:
        box1 = naked_twin[0]
        box2 = naked_twin[1]

        box1_peers = peers[box1]
        box2_peers = peers[box2]

        intersection_boxes = set(box1_peers).intersection(box2_peers)

        for box in intersection_boxes:
            for val in values[box1]:
                if len(values[box]) > 2:
                    assign_value(values, box, values[box].replace(val, ''))
    return values



    # Eliminate the naked twins as possibilities for their peers

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    grid_list = []
    for ch in grid:
        if ch == '.':
            grid_list.append(cols)
        else:
            grid_list.append(ch)

    grid_boxes_value = dict(zip(boxes, grid_list))

    return grid_boxes_value

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    single_value_box = [box for box in values if len(values[box]) == 1]
    for svb in single_value_box:
        svb_value = values[svb]
        for peer in peers[svb]:
            assign_value(values, peer, values[peer].replace(svb_value, ''))
            #values[peer] = values[peer].replace(svb_value, '')
    return values


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for num in cols:
            boxes_has_num = [box for box in unit if num in values[box]]
            if len(boxes_has_num) == 1:
                assign_value(values, boxes_has_num[0], num)
                #values[boxes_has_num[0]] = num
    return values

def reduce_puzzle(values):
    halted = False
    while not halted:
        # Solved boxes count
        solved_boxes = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate
        values = eliminate(values)

        # Only Choice
        values = only_choice(values)

        # Compute the solved boxes after running eliminate and only choice
        solved_boxes_after = len([box for box in values.keys() if len(values[box]) == 1])

        # Check if no boxes hase been solved
        halted = solved_boxes == solved_boxes_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

    # Reduce
    values = reduce_puzzle(values)

    if not values:
        return False

    # Check if already solved
    unsolved_boxes = [box for box in values.keys() if len(values[box]) > 1]
    if len(unsolved_boxes) == 0:
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, box = min((len(values[s]), s) for s in unsolved_boxes)

    for num in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = num
        attemp = search(new_sudoku)
        if attemp:
            return attemp


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """Cross product of elements in A and elements in B."""

    return [a+b for a in A for b in B]

def inner(A,B):
    """
    "Inner" product of elements in A and elements in B.

    :param A:
    :param B:
    :return:
    """
    return [a+b for a, b in zip(A,B)]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units= [inner('ABCDEFGHI','123456789'),inner('ABCDEFGHI','987654321')]
unitlist = row_units + column_units + square_units +diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def find_twins(unit,values):
    """
    Find all twins in a unit
    :param unit: the unit list
    :return: a list of naked twins in a unit, e.g. [(box1,box2),(box3,box4)]
    """

    all_twins=[box for box in unit if len(values[box])==2]
    visited=[False for t in all_twins]

    # a dictionary to bookeep whether a potential candidate has been visited or not
    all_twins=dict(zip(all_twins,visited))

    if len(all_twins)<2:
        return None

    pair=[]
    for twin in all_twins.keys():
        if all_twins[twin]==True:
            # pass this node if it is already visited
            continue
        else:
            all_twins[twin]=True
            for twin2 in all_twins:
                if all_twins[twin2]==False:
                    if values[twin]==values[twin2]:
                        # Add the twin into the final result when a twin is found
                        all_twins[twin2]=True
                        pair.append((twin,twin2))

    return pair



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


    for unit in unitlist:
        pair=find_twins(unit,values)
        if pair is None:
            continue

        # Delete the digits in every cell in a unit if these digits occur in naked twins
        for p in pair:
            for digit in values[p[0]]:
                for box in unit:
                    if box not in p and len(values[box])>1:
                        values[box]=values[box].replace(digit,'')


    return values





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
    values = []
    for g in grid:
        if g == '.':
            values.append('123456789')
        else:
            values.append(g)

    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]

        # eliminate every digit shows up in peers
        for b in peers[box]:
            if len(values[b]) > 1:
                values[b] = values[b].replace(digit, '')
    return values

def only_choice(values):

    all_digits = '123456789'
    for unit in unitlist:
        for a in all_digits:
            dplaces = []
            for box in unit:
                if a in values[box]:
                    dplaces.append(box)
            if len(dplaces) == 1:
                values[dplaces[0]] = a

    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values=eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values=only_choice(values)

        # Apply naked twins

        naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):

    values = reduce_puzzle(values)

    if values is False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    min_val = 9
    min_box = None
    for b in boxes:
        if len(values[b]) > 1:
            if len(values[b]) < min_val:
                min_val = len(values[b])
                min_box = b

    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[min_box]:
        p_values = values.copy()
        p_values[min_box] = digit
        result = search(p_values)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values=grid_values(grid)

    values=reduce_puzzle(values)

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

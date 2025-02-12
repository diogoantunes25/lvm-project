from z3 import *
import time

OFFICIAL_EXAMPLE = ([[2,1],[2,1,3],[7],[1,3],[2,1]], [[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]])
OFFICIAL_SOLUTION = [[False, True, True, False, False], [False, True, True, False, True], [False, False, True, False, True], [False, True, True, True, False], [True, False, True, False, False], [True, False, True, False, False], [False, False, True, True, False], [False, True, False, True, False], [False, True, False, True, True], [True, True, False, False, False]]

TEST_1 = ([[1, 1], [1, 1], [1, 1], [2, 1], [1, 1, 2], [1]], [[1], [1], [5], [1], [2, 2], [1, 1]])
TEST_1_SOL = [[False, False, False, False, True, False], [False, False, False, True, False, False], [True, True, True, True, True, False], [False, False, False, False, False, True], [True, True, False, True, True, False], [False, False, True, False, True, False]]

def all_possible(gaps, size):
    """
    Returns all possible start configurations given the gaps and the line size.
    """

    if len(gaps) == 0:
        return []

    g = gaps[0]
    min_start = 0
    max_start = (size-g) - (sum(gaps[1:]) + (len(gaps)-1))

    if len(gaps) == 1:
        return list(map(lambda x: [x], range(min_start, max_start+1)))

    ans = []
    for start in range(min_start, max_start+1):
        offset = start + g + 1
        for relative_positions in all_possible(gaps[1:], size - offset):
            positions = [start] + list(map(lambda p: p + offset, relative_positions))
            ans += [positions]

    return ans

def constraints_for_line_brute(gaps, size, s, x, id = 0):
    """
    Adds to the model s all constraints for the provided line using the brute-force approach
    """

    valid_starts = []
    for starts in all_possible(gaps, size):
        ends = list(map(lambda p: p[1] + gaps[p[0]], enumerate(starts)))
        bounds = list(zip(starts, ends))

        start, end = bounds.pop(0)

        i = 0
        values = []
        while i < size:
            if i < start:
                values += [Not(x[i])]
                i += 1
            elif i < end:
                values += [x[i]]
                i += 1
            else:
                if len(bounds) > 0:
                    start, end = bounds.pop(0)
                else:
                    start = size
                    end = size

        valid_starts += [And(values)]

    s.add(Or(valid_starts))

def constraints_for_line_poly(gaps, size, s, x, id = 0):
    """
    Adds to the model s all constraints for the provided line using the polynomial approach
    """

    c = [[Bool(f"c_{id}_{j}_{i}") for i in range(size+1)] for j in range(len(gaps))]

    for i, gap in enumerate(gaps):
        min_start = sum(gaps[:i]) + len(gaps[:i])
        max_start = size - (sum(gaps[i:]) + len(gaps[i+1:]))

        # Ensure gaps are filled with the appropriate sizes
        for start in range(min_start, max_start + 1):

            if i == 0:
                # We're the first gap.
                # To start completing the gap at `start`, we need to ensure:
                #   - we haven't started completing the gap (not c[i][start+gap-1])
                #   - the current cell is filled (x[start])
                left = And(Not(c[i][start+gap-1]), x[start]) if start > 0 else x[start]
            else:
                # We're past the first gap.
                # To start completing the gap at `start`, we need to ensure:
                #   - we haven't started completing the gap (not c[i][start+gap-1])
                #   - the current cell is filled (x[start])
                #   - previous gap has finished (c[i-1][start])
                left = And(c[i-1][start-1], Not(c[i][start+gap-1]), x[start]) if start > 0 else x[start]

            # Fill the rest of the gap
            remaining = And(list(map(lambda i: x[i], range(start+1, start+gap))))

            # The slack are the cells that must necessarily be empty after the current gap
            if i < len(gaps) - 1:
                # If not last gap, the slack is just the cell after the gap
                slack = Not(x[start+gap])
            else:
                # If last gap, the slack are all the remaining cells (starting from the end of the gap)
                slack = And(list(map(lambda i: Not(x[i]), range(start+gap, size))))

            right = And([remaining, slack, c[i][start+gap]])

            s.add(Implies(left, right))

        # If gap was placed by position start, then it was placed by position start+1
        for start in range(min_start, size):
            s.add(Implies(c[i][start], c[i][start+1]))

        # Ensure that c[i][j] is only set to true for valid reason
        # for j in range(min_start+1, size+1):
        for j in range(min_start, size+1):
            # j is the empty cell
            # corresponding start is j - gap
            start = j - gap

            if start <= max_start:
                # If the position is within the allowed starts, then it can be filled:
                #   - the previous was filled
                #   - we just placed the gap
                gap_cells = And(list(map(lambda i: x[i], range(start, start+gap))))
                s.add(Implies(c[i][j], Or(c[i][j-1], gap_cells)))
            else:
                # If the position is not within the allowed starts, then the previous
                # cell should the be reason why it was filled
                s.add(Implies(c[i][j], c[i][j-1]))

        # Ensure all gaps are placed by the end
        s.add(c[i][size])

        # Ensure the gap is not completed before start position
        s.add(And(list(map(lambda j: Not(c[i][j]), range(0, min_start+gap)))))

        # Ensure orderly completion
        for k in range(0, max_start):
            if i < len(gaps) - 1:
                next_gap = gaps[i+1]
                cooldown = And(list(map(lambda j: Not(c[i+1][j+next_gap]), range(k, k+gap+1))))
                s.add(Implies(Not(c[i][k+gap]), cooldown))


def gen_z3(width, height):
    """
    Creates z3 solver and cell variables
    """

    s = Solver()
    xs = [[Bool(f"x_{i}_{j}") for i in range(width)] for j in range(height)]

    return (s, xs)

def transpose(x):
    """
    Transposes matrix
    """
    return [[row[i] for row in x] for i in range(len(x[0]))]

def model_to_bitmap(model, width, height):
    """
    Converts the z3 provided model into a array of bits
    """

    bits = [[False for _ in range(width)] for _ in range(height)]

    for v in model:
        if v.name()[0] == "x":
            x, y = list(map(int, v.name().split("_")[1:]))
            bits[y][x] = model[v]

    return bits

def show_all(H, V, bits):
    """
    Auxiliary function to pretty print the puzzle
    """
    max_h = max(len(h) for h in H)  # Maximum length of horizontal clues
    max_v = max(len(v) for v in V)  # Maximum length of vertical clues
    cell_width = 4  # Adjust cell width to match the grid width

    # Prepare vertical clues by transposing and padding them to align with the grid
    vertical_clues = []
    for i in range(max_v):
        row = []
        for v in V:
            if len(v) > i:
                row.append(f'{v[i]:2}')  # Format to align
            else:
                row.append('  ')  # Padding for shorter vertical clues
        vertical_clues.append(row)

    # Print the vertical clues at the top
    for i in range(max_v):
        print(' ' + ' ' * (max_h * cell_width), end='')  # Padding for horizontal clues
        for clue in vertical_clues[i]:
            print(clue.center(cell_width), end=' ')
        print()

    # Print horizontal clues and the solution grid
    for h, row in zip(H, bits):
        # Print the horizontal clue
        print(' '.join(f'{x:2}' for x in h).rjust(max_h * cell_width), end='  ')

        # Print the grid row
        for value in row:
            if value:
                print('[T]'.center(cell_width), end=' ')
            else:
                print('[ ]'.center(cell_width), end=' ')
        print()  # Newline after each row

def show_bits(bits):
    """
    Auxiliary function to pretty print a solution
    """
    for row in bits:
        for value in row:
            if value:
                print('[T]', end=' ')  # Print 'T' for True
            else:
                print('[ ]', end=' ')  # Leave a space for False
        print()  # Newline after each row

def nonogram(V, H, show = True, return_stats = False, constraints_for_line = constraints_for_line_poly):
    """
    Function that givven two lists V and H of lists of positive integers, finds the solution for the corresponding
    nonogram.
    Can optionally print the solution or return statistics about execution.
    """

    width = len(V)
    height = len(H)

    s, x = gen_z3(width, height)

    if return_stats:
        bits, stats = _nonogram(V, H, s, x, return_stats = True, constraints_for_line = constraints_for_line)
    else:
        bits = _nonogram(V, H, s, x, return_stats = False, constraints_for_line = constraints_for_line)

    if show:
        if len(bits) > 0:
            print("")
            # show_bits(bits)
            show_all(H, V, bits)
        else:
            print("unsat")

    return (bits, stats) if return_stats else bits

def _nonogram(V, H, s, x, return_stats = False, constraints_for_line = constraints_for_line_poly):
    """
    Function that given two lists V and H of lists of positive integers, determines a solution
    for the nonogram, if there is one.
    Inputs:
    - V: vertical constraints
    - H: horizontal constraints
    - s: the z3 solver
    - x: the set of variables
    """

    start = time.time()

    width = len(V)
    height = len(H)

    x_t = transpose(x)

    j = 0
    for i, line in enumerate(H):
        constraints_for_line(line, width, s, x[i], id = j)
        j += 1

    for i, line in enumerate(V):
        constraints_for_line(line, height, s, x_t[i], id = j)
        j += 1

    middle = time.time()

    ans = s.check()

    end = time.time()


    stats = {"init": middle-start, "solving": end-middle}

    bits = model_to_bitmap(s.model(), width, height) if ans == sat else []

    return (bits, stats) if return_stats else bits

def well_posed(V, H, constraints_for_line = constraints_for_line_poly):
    """
    Function that given two lists V and H of lists of positive integers, determines if the given
    constraints define a well posed puzzle.
    Inputs:
    - V: vertical constraints
    - H: horizontal constraints
    """

    width = len(V)
    height = len(H)

    s, x = gen_z3(width, height)
    bits = _nonogram(V, H, s, x, constraints_for_line = constraints_for_line)

    # Add negation of bits as constraints
    flat = []
    for i in range(len(bits)):
        for j in range(len(bits[0])):
            if bits[i][j]:
                flat += [x[i][j]]
            else:
                flat += [Not(x[i][j])]

    s.add(Not(And(flat)))

    # For the puzzle to be well-posed, this should now be unsat
    return s.check() != sat

def all_solutions(V, H, constraints_for_line = constraints_for_line_poly):
    """
    Function that given two lists V and H of lists of positive integers, returns all solutions for the nonogram.
    Inputs:
    - V: vertical constraints
    - H: horizontal constraints
    """

    width = len(V)
    height = len(H)

    s, x = gen_z3(width, height)
    bits = _nonogram(V, H, s, x, constraints_for_line = constraints_for_line)

    solutions = []
    while len(bits) > 0:
        solutions += [bits]
        # Add negation of bits as constraints
        flat = []
        for i in range(len(bits)):
            for j in range(len(bits[0])):
                if bits[i][j]:
                    flat += [x[i][j]]
                else:
                    flat += [Not(x[i][j])]

        s.add(Not(And(flat)))

        bits = model_to_bitmap(s.model(), width, height) if s.check() == sat else []

    return solutions

def main():
    nonogram(*OFFICIAL_EXAMPLE, show = True, constraints_for_line = constraints_for_line_brute)

if __name__ == "__main__":
    main()

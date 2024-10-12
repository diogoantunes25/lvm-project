from z3 import *
import time

TEST_1 = ([[1, 1, 2, 1], [2, 1], [1, 1, 1, 2], [1, 1, 3], [1]], [[1], [3], [1], [1, 2], [1], [1], [1, 2], [1], [3], [1, 1]])
TEST_1_SOL = [[False, False, False, True, False], [True, True, True, False, False], [False, True, False, False, False], [True, False, True, True, False], [False, False, False, False, True], [True, False, False, False, False], [True, False, True, True, False], [False, False, False, True, False], [False, True, True, True, False], [True, False, True, False, False]]

def all_possible(gaps, size):
    """
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

def constraints_for_line_2(gaps, size, s, x):
    """
    TBA
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

def constraints_for_line(gaps, size, s, x):
    """
    TBA
    """

    c = [[Bool(f"c_{j}_{i}") for i in range(size+1)] for j in range(len(gaps))]

    for i, gap in enumerate(gaps):
        min_start = sum(gaps[:i]) + len(gaps[:i])
        max_start = size - (sum(gaps[i:]) + len(gaps[i+1:]))

        # Ensure proper gaps
        for start in range(min_start, max_start + 1):

            # Previous did not start completing and I want to start
            left = And(Not(c[i][start+gap-1]), x[start]) if start > 0 else x[start]

            remaining = And(list(map(lambda i: x[i], range(start+1, start+gap))))

            if i < len(gaps) - 1:
                # not last gap
                slack = Not(x[start+gap])
            else:
                slack = And(list(map(lambda i: Not(x[i]), range(start+gap, size))))

            right = And([remaining, slack, c[i][start+gap]])

            s.add(Implies(left, right))

        # add constraints implications
        for start in range(min_start, size):
            s.add(Implies(c[i][start], c[i][start+1]))

        # add backpropagation
        for j in range(min_start+1, size+1):
            # j is the empty cell
            # corresponding start is j - gap
            start = j - gap
            if start <= max_start:
                remaining = And(list(map(lambda i: x[i], range(start, start+gap))))
                s.add(Implies(c[i][j], Or(c[i][j-1], remaining)))
            else:
                s.add(Implies(c[i][j], c[i][j-1]))

        # ensure completion
        s.add(c[i][size])

        # all starts false
        s.add(And(list(map(lambda j: Not(c[i][j]), range(0, min_start+gap)))))

        # ensure orderly completion
        for k in range(0, max_start):
            if i < len(gaps) - 1:
                cooldown = And(list(map(lambda j: Not(c[i+1][j+gap]), range(k, k+gap))))
                s.add(Implies(Not(c[i][k+gap]), cooldown))


def gen_z3(width, height):
    """
    TBA
    """

    s = Solver()
    xs = [[Bool(f"x_{i}_{j}") for i in range(width)] for j in range(height)]

    return (s, xs)

def transpose(x):
    """
    TBA
    """
    return [[row[i] for row in x] for i in range(len(x[0]))]

def model_to_bitmap(model, width, height):
    """
    TBA
    """

    bits = [[False for _ in range(width)] for _ in range(height)]

    for v in model:
        x, y = list(map(int, v.name().split("_")[1:]))
        bits[y][x] = model[v]

    return bits

def show_bits(bits):
    for row in bits:
        for value in row:
            if value:
                print('[T]', end=' ')  # Print 'T' for True
            else:
                print('[ ]', end=' ')  # Leave a space for False
        print()  # Newline after each row

def nonogram(V, H, show = True, return_stats = False):
    """
    TBA
    """

    width = len(V)
    height = len(H)

    s, x = gen_z3(width, height)

    if return_stats:
        bits, stats = _nonogram(V, H, s, x, return_stats = True)
    else:
        bits = _nonogram(V, H, s, x, return_stats = False)

    if len(bits) > 0 and show:
        print("")
        show_bits(bits)

    return (bits, stats) if return_stats else bits

def _nonogram(V, H, s, x, return_stats = False):
    """
    Function that given two lists V and H of lists of positive integers, determines a solution
    for the nonogram, if there is one.
    Inputs:
    - V: vertical constraints
    - H: horizontal constraints
    """

    start = time.time()

    width = len(V)
    height = len(H)

    x_t = transpose(x)

    for i, line in enumerate(H):
        constraints_for_line(line, width, s, x[i])

    for i, line in enumerate(V):
        constraints_for_line(line, height, s, x_t[i])

    middle = time.time()

    ans = s.check()

    end = time.time()

    stats = {"init": middle-start, "solving": end-middle}

    bits = model_to_bitmap(s.model(), width, height) if ans == sat else []

    return (bits, stats) if return_stats else bits

# Less eficient version
def well_posed_2(V, H):
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
    bits = _nonogram(V, H, s, x)

    # Add negation of bits as constraints
    flat = []
    for i in range(len(bits)):
        for j in range(len(bits[0])):
            if bits[i][j]:
                flat += [x[i][j]]
            else:
                flat += [Not(x[i][j])]

    s.add(Not(And(flat)))

    return len(_nonogram(V, H, s, x)) == 0

def well_posed(V, H):
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
    bits = _nonogram(V, H, s, x)

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

# Less eficient version
def all_solutions_2(V, H):
    """
    """

    width = len(V)
    height = len(H)

    s, x = gen_z3(width, height)
    bits = _nonogram(V, H, s, x)

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

        bits = _nonogram(V, H, s, x)

    return solutions

def all_solutions(V, H):
    """
    """

    width = len(V)
    height = len(H)

    s, x = gen_z3(width, height)
    bits = _nonogram(V, H, s, x)

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
    s, xs = gen_z3(10, 10)
    constraints_for_line([3, 2], 10, s, xs[0])
    s.add(Not(And([xs[0][1], xs[0][2], xs[0][3], xs[0][8], xs[0][9]])))
    s.add(Not(And([xs[0][0], xs[0][1], xs[0][2], xs[0][8], xs[0][9]])))
    s.add(Not(And([xs[0][0], xs[0][1], xs[0][2], xs[0][7], xs[0][8]])))
    s.add(Not(And([xs[0][0], xs[0][1], xs[0][2], xs[0][6], xs[0][7]])))
    s.add(Not(And([xs[0][0], xs[0][1], xs[0][2], xs[0][4], xs[0][5]])))
    s.add(Not(And([xs[0][0], xs[0][1], xs[0][2], xs[0][5], xs[0][6]])))
    # print(s)

    s.check()
    m = s.model()
    res = []
    for t in m.decls():
        if is_true(m[t]):
            res += [str(t)]
    print('\n'.join(sorted(res)))

if __name__ == "__main__":
    main()

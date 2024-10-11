from z3 import *

def all_possible(gaps, size):
    """
    """

    g = gaps[0]
    min_start = 0
    max_start = (size-g) - (sum(gaps[1:]) + (len(gaps)-1))

    # print(f"called with size = {size}")

    if len(gaps) == 1:
        return list(map(lambda x: [x], range(min_start, max_start+1)))

    ans = []
    for start in range(min_start, max_start+1):
        # print(f"Checking start from {start}")
        offset = start + g + 1
        for relative_positions in all_possible(gaps[1:], size - offset):
            positions = [start] + list(map(lambda p: p + offset, relative_positions))
            ans += [positions]

    return ans

def constraints_for_line(gaps, size, s, x):
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

def nonogram(V, H):
    """
    Function that given two lists V and H of lists of positive integers, determines a solution
    for the nonogram, if there is one.
    Inputs:
    - V: vertical constraints
    - H: horizontal constraints
    """

    width = len(V)
    height = len(H)

    print(f"solving problem with width={width}, height={height}")

    s, x = gen_z3(width, height)
    x_t = transpose(x)

    for i, line in enumerate(H):
        constraints_for_line(line, width, s, x[i])

    for i, line in enumerate(V):
        constraints_for_line(line, height, s, x_t[i])

    ans = s.check()
    print(ans)

    if ans == sat:
        model = s.model()
        bits = model_to_bitmap(model, width, height)
        print("")
        show_bits(bits)
    else:
        print("No solution found")

def well_posed(V, H):
    """
    Function that given two lists V and H of lists of positive integers, determines if the given
    constraints define a well posed puzzle.
    Inputs:
    - V: vertical constraints
    - H: horizontal constraints
    """

    pass

def main():
    nonogram([[2,1],[2,1,3],[7],[1,3],[2,1]],[[2],[2,1],[1,1],[3],[1,1],[1,1],[2],[1,1],[1,2],[2]])
    # print(all_possible([1, 1], 5))


if __name__ == "__main__":
    main()

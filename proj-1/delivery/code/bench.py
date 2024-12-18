from nonoguru import *
import random, sys

def gaps(bits):
    gaps = []
    for row in bits:
        g = []
        c = 0
        for b in row:
            if b == 0 and c > 0:
                g += [c]
                c = 0

            c += b

        if c > 0:
            g += [c]

        gaps += [g]

    return gaps

def int_to_bool(bits):
    return [list(map(bool, row)) for row in bits]

def random_test(width, height):
    """
    Returns test and solution
    """
    bits = [[random.getrandbits(1) for _ in range(width)] for _ in range(height)]

    V = gaps(bits)
    H = gaps(transpose(bits))

    if [] in V or [] in H:
        return random_test(width, height)
    else:
        return ((H, V), int_to_bool(bits))

def main():
    if len(sys.argv) < 2:
        print("Please provide a filename.")
    else:
        filename = sys.argv[1]

    count = 10
    stats = []

    values = []
    for size in range(4, 40, 2):
        # Split size into two parts. You can adjust how they are divided if needed.
        part1 = size // 2
        part2 = size - part1
        values.append((part1, part2))

    print(f"The values are  {values}")

    # print to csv
    with open(filename, 'w') as fh:
        fh.write("width, height, init, solving, mode\n")

        for (width, height) in values:
            for method in ["brute", "poly"]:
                i = 0
                while i < count:
                    i += 1
                    stat = bench_single(width, height, method)
                    stat["width"] = width
                    stat["height"] = height
                    stat["method"] = method

                    fh.write(f"{stat['width']}, {stat['height']}, {stat['init']}, {stat['solving']}, {stat['method']}\n")


def bench_single(width, height, method):
    myoutputs = []
    while len(myoutputs) != 1:
        input, output = random_test(width, height)
        myoutputs = all_solutions(*input)

    if method == "brute":
        myoutput, stats = nonogram(*input, return_stats = True, show = False, constraints_for_line = constraints_for_line_brute)
    else:
        myoutput, stats = nonogram(*input, return_stats = True, show = False, constraints_for_line = constraints_for_line_poly)

    print(stats)

    match = (myoutput == output)
    if match:
        return stats
    else:
        print("Failed")

        print("Input")
        print(input)

        print("Output")
        print(output)

        raise Exception("Bad answer")

if __name__ == "__main__":
    main()

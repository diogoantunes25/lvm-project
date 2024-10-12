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

    values = [(5, 10), (2, 4)]

    for (width, height) in values:
        this_stats = []
        while len(this_stats) < count:
            stat = bench_single(width, height)
            stat["width"] = width
            stat["height"] = height

            this_stats += [stat]

        stats += this_stats

    # print to csv
    with open(filename, 'w') as fh:
        fh.write("width, height, init, solving\n")
        for stat in stats:
            fh.write(f"{stat['width']}, {stat['height']}, {stat['init']}, {stat['solving']}\n")


def bench_single(width, height):
    myoutputs = []
    while len(myoutputs) != 1:
        input, output = random_test(width, height)
        myoutputs = all_solutions(*input)

    myoutput, stats = nonogram(*input, return_stats = True, show = False)

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

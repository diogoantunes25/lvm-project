from nonoguru import *
import random

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

    return ((H, V), int_to_bool(bits))

def main():
    i = 0
    count = 1000
    while i < count:
        if solve_one():
            i += 1

def solve_one():
    input, output = random_test(5, 10)
    myoutputs = all_solutions(*input)
    if len(myoutputs) != 1:
        print("I wasn't able to find a single solution")
        return False

    myoutput = myoutputs[0]
    match = (myoutput == output)
    if match:
        print("Correct")
        return True
    else:
        print("Failed")

        print("Input")
        print(input)

        print("Output")
        print(output)

        raise Exception("Bad answer")

if __name__ == "__main__":
    main()

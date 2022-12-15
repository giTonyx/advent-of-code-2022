#!/usr/bin/env python3
import sys
import importlib
import os.path


def main():
    day = 1 if len(sys.argv) == 1 else int(sys.argv[-1])
    day_name = "day%02d" % day
    solution = importlib.import_module("solutions." + day_name)
    input_filename = os.path.join(os.path.dirname(__file__), "..", "input", day_name)
    solver = solution.Solver()
    solver.solve(input_filename)

    return 0


if __name__ == "__main__":
    sys.exit(main())

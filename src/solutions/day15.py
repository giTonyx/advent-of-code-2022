import solution


def extract_coords(input):
    sensor_part, beacon_part = input.split(":")
    sx_part, sy_part = sensor_part.split(",")
    sx = int(sx_part.strip().split("=")[1])
    sy = int(sy_part.strip().split("=")[1])
    bx_part, by_part = beacon_part.split(",")
    bx = int(bx_part.strip().split("=")[1])
    by = int(by_part.strip().split("=")[1])
    return sx, sy, bx, by


def closest_positions(sx, sy, bx, by, yfilter):
    cells = set()
    max_distance = abs(sx - bx) + abs(sy - by)
    ydistance = abs(sy - yfilter)
    remaining_distance = max_distance - ydistance
    if remaining_distance < 0:
        return cells
    for dx in range(-remaining_distance, remaining_distance + 1):
        px = sx + dx
        if px == bx and yfilter == by: continue
        cells.add((px, yfilter))
    return cells


def find_hole_in_row(inputs, bounds, row):
    ranges = []

    for sx, sy, distance in inputs:
        remaining = distance - abs(row - sy)
        if remaining < 1: continue
        lx = max(0, sx - remaining)
        rx = min(bounds + 1, sx + remaining)
        ranges.append((lx, rx))

    ranges.sort()
    current_x = ranges[0][1]
    for i in range(1, len(ranges)):
        if ranges[i][0] > (current_x + 1):
            return ranges[i][0] - 1
        current_x = max(current_x, ranges[i][1])


def find_hole(inputs, bounds):
    for y in range(bounds + 1):
        res = find_hole_in_row(inputs, bounds, y)
        if res is not None:
            return res, y


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        empty_cells = set()
        for line in input_data:
            sx, sy, bx, by = extract_coords(line)
            empty = closest_positions(sx, sy, bx, by, 2000000)
            empty_cells = empty_cells.union(empty)
        return len(empty_cells)

    def solve_second(self, input_data):
        inputs = []
        for line in input_data:
            sx, sy, bx, by = extract_coords(line)
            inputs.append((sx, sy, abs(sx - bx) + abs(sy - by)))
        (x, y) = find_hole(inputs, 4000000)
        return x * 4000000 + y

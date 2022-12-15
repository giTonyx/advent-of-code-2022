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


def find_row_len(inputs, beacons, row):
    beacons = set([x for x, y in beacons if y == row])
    ranges = []
    for sx, sy, distance in inputs:
        remaining = distance - abs(row - sy)
        if remaining < 1: continue
        lx = sx - remaining
        rx = sx + remaining
        ranges.append((lx, rx))
    ranges.sort()

    total = 0
    clx, crx = ranges[0]
    for lx, rx in ranges[1:]:
        if lx <= crx:
            crx = max(crx, rx)
        else:
            total += crx - clx + 1
            for b in beacons:
                if clx <= b <= crx:
                    total -= 1
            clx = lx
            crx = rx
    total += crx - clx + 1
    for b in beacons:
        if clx <= b <= crx:
            total -= 1
    return total


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
        inputs = []
        beacons = []
        for line in input_data:
            sx, sy, bx, by = extract_coords(line)
            inputs.append((sx, sy, abs(sx - bx) + abs(sy - by)))
            beacons.append((bx, by))
        return find_row_len(inputs, beacons, 2000000)

    def solve_second(self, input_data):
        inputs = []
        for line in input_data:
            sx, sy, bx, by = extract_coords(line)
            inputs.append((sx, sy, abs(sx - bx) + abs(sy - by)))
        (x, y) = find_hole(inputs, 4000000)
        return x * 4000000 + y

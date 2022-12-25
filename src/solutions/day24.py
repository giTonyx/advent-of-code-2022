import solution
from collections import deque


class Blizzards(object):
    def __init__(self, blizzards, width, height):
        self.blizzards = blizzards
        self.positions = {}
        self.width = width
        self.height = height

    def get_positions_at(self, step):
        if step not in self.positions:
            positions = []
            for ((x, y), d) in self.blizzards:
                if d == "^": y = ((y - 1 - step) % (self.height - 2)) + 1
                if d == "v": y = ((y - 1 + step) % (self.height - 2)) + 1
                if d == "<": x = ((x - 1 - step) % (self.width - 2)) + 1
                if d == ">": x = ((x - 1 + step) % (self.width - 2)) + 1
                positions.append((x, y))
            self.positions[step] = set(positions)
        return self.positions[step]


def possible_moves(x, y, width, height, start_x, end_x):
    moves = []
    moves.append((x, y))

    if x < (width - 2) and 0 < y < height: moves.append((x + 1, y))
    if x > 1 and 0 < y < (height-1): moves.append((x - 1, y))
    if y < (height - 2) or (y == height - 2 and x == end_x): moves.append((x, y + 1))
    if y > 1 or (y == 1 and x == start_x): moves.append((x, y - 1))

    return moves


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        width = len(input_data[0])
        height = len(input_data)
        start_x = [x for x in range(width) if input_data[0][x] == "."][0]
        end_x = [x for x in range(width) if input_data[-1][x] == "."][0]

        blizzards = []
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                cell = input_data[y][x]
                if cell != ".":
                    blizzards.append(((x, y), cell))
        b = Blizzards(blizzards, width, height)

        initial_state = (0, start_x, 0)
        seen = set()
        seen.add(initial_state)
        to_visit = deque()
        to_visit.append(initial_state)

        while len(to_visit):
            steps, x, y = to_visit.popleft()
            if x == end_x and y == (height - 1):
                return steps
            blizzard_positions = b.get_positions_at(steps + 1)
            moves = possible_moves(x, y, width, height, start_x, end_x)
            for mx, my in moves:
                if (mx, my) not in blizzard_positions:
                    state = (steps + 1, mx, my)
                    if state not in seen:
                        seen.add(state)
                        to_visit.append(state)

    def solve_second(self, input_data):
        width = len(input_data[0])
        height = len(input_data)
        start_x = [x for x in range(width) if input_data[0][x] == "."][0]
        end_x = [x for x in range(width) if input_data[-1][x] == "."][0]

        blizzards = []
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                cell = input_data[y][x]
                if cell != ".":
                    blizzards.append(((x, y), cell))
        b = Blizzards(blizzards, width, height)

        initial_state = (0, start_x, 0, 0)
        seen = set()
        seen.add(initial_state)
        to_visit = deque()
        to_visit.append(initial_state)

        while len(to_visit):
            steps, x, y, travel = to_visit.popleft()
            if x == start_x and y == 0 and travel == 1:
                to_visit.clear()
                travel = 2
            if x == end_x and y == (height - 1):
                if travel == 0:
                    to_visit.clear()
                    travel = 1
                if travel == 2:
                    return steps
            blizzard_positions = b.get_positions_at(steps + 1)
            moves = possible_moves(x, y, width, height, start_x, end_x)
            for mx, my in moves:
                if (mx, my) not in blizzard_positions:
                    state = (steps + 1, mx, my, travel)
                    if state not in seen:
                        seen.add(state)
                        to_visit.append(state)

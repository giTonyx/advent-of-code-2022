import solution


class Cave(object):
    def __init__(self):
        self.blocks = set()
        self.sand = set()
        self.bottom = -1
        self.drop = set()

    def is_free(self, x, y):
        if y >= (self.bottom + 2): return False
        return (x, y) not in self.blocks and (x, y) not in self.sand

    def add_line(self, line):
        points = line.split("->")
        for i in range(len(points) - 1):
            x1, y1 = [int(x) for x in points[i].strip().split(",")]
            x2, y2 = [int(x) for x in points[i + 1].strip().split(",")]

            if y1 > self.bottom: self.bottom = y1
            if y2 > self.bottom: self.bottom = y2

            if x1 > x2: x1, x2 = x2, x1
            if y1 > y2: y1, y2 = y2, y1

            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    self.blocks.add((x, y))
        return

    def print(self):
        out = ""
        left = min(x for x, y in self.blocks)
        right = max(x for x, y in self.blocks)
        for y in range(self.bottom + 1):
            for x in range(left, right + 1):
                if x == 500 and y == 0:
                    out += "+"
                    continue
                if (x, y) in self.blocks:
                    out += "#"
                    continue
                if (x, y) in self.sand:
                    out += "o"
                    continue
                if (x, y) in self.drop:
                    out += "X"
                    continue
                out += "."
            out += "\n"
        print(out)

    def drop_sand(self, has_bottom):
        x = 500
        y = 0
        if not self.is_free(x, y):
            return False
        drop = set()
        while True:
            drop.add((x, y))
            if y > self.bottom and not has_bottom:
                self.drop = drop
                return False
            if self.is_free(x, y + 1):
                y += 1
                continue
            if self.is_free(x - 1, y + 1):
                x -= 1
                y += 1
                continue
            if self.is_free(x + 1, y + 1):
                x += 1
                y += 1
                continue
            self.sand.add((x, y))
            return True


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        cave = Cave()
        for l in input_data:
            cave.add_line(l)
        while cave.drop_sand(has_bottom=False):
            pass
        return len(cave.sand)

    def solve_second(self, input_data):
        cave = Cave()
        for l in input_data:
            cave.add_line(l)
        while cave.drop_sand(has_bottom=True):
            pass
        return len(cave.sand)

        return 0

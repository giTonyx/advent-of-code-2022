import solution


class Heightmap(object):
    def __init__(self, input_data):
        self.width = len(input_data[0])
        self.height = len(input_data)
        self.cells = []
        for row in input_data:
            for cell in row:
                self.cells.append(Cell(cell))
        return

    def start_position(self):
        for i in range(len(self.cells)):
            if self.cells[i].is_start:
                return i

    def end_position(self):
        for i in range(len(self.cells)):
            if self.cells[i].is_end:
                return i

    def lowest_positions(self):
        result = []
        for i in range(len(self.cells)):
            if self.cells[i].elevation == 0:
                result.append(i)
        return result

    def adjacent(self, position):
        results = []
        height = self.cells[position].elevation
        x = position % self.width
        y = position // self.width
        if x > 0 and self.cells[position - 1].elevation <= (height + 1):
            results.append(position - 1)
        if x < (self.width - 1) and self.cells[position + 1].elevation <= (height + 1):
            results.append(position + 1)
        if y > 0 and self.cells[position - self.width].elevation <= (height + 1):
            results.append(position - self.width)
        if y < (self.height - 1) and self.cells[position + self.width].elevation <= (height + 1):
            results.append(position + self.width)
        return results


class Cell(object):
    def __init__(self, mark):
        self.is_start = mark == 'S'
        self.is_end = mark == 'E'
        self.elevation = ord(mark) - ord('a')
        if self.is_start:
            self.elevation = 0
        if self.is_end:
            self.elevation = 26
        return


class VisitMap(object):
    def __init__(self):
        self.m = {}

    def add(self, value, weight):
        self.m[value] = weight

    def pop(self):
        min_weight = min(self.m.values())
        for k, v in self.m.items():
            if v == min_weight:
                min_value = v
                break
        del self.m[k]
        return (k, v)

    def have_already(self, value, weight):
        if value in self.m and self.m[value] <= weight: return True
        return False


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        heightmap = Heightmap(input_data)

        start_position = heightmap.start_position()
        end_position = heightmap.end_position()
        to_visit = VisitMap()
        to_visit.add(start_position, 1)

        while True:
            position, steps = to_visit.pop()

            for p in heightmap.adjacent(position):
                if p == end_position:
                    return steps
                if not to_visit.have_already(p, steps + 1):
                    to_visit.add(p, steps + 1)

    def solve_second(self, input_data):
        heightmap = Heightmap(input_data)

        start_positions = heightmap.lowest_positions()

        end_position = heightmap.end_position()
        to_visit = VisitMap()
        for start_position in start_positions:
            to_visit.add(start_position, 1)

        while True:
            position, steps = to_visit.pop()

            for p in heightmap.adjacent(position):
                if p == end_position:
                    return steps
                if not to_visit.have_already(p, steps + 1):
                    to_visit.add(p, steps + 1)

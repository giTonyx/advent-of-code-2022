import solution


class TreeGrid(object):
    def __init__(self, input):
        self.width = len(input[0])
        self.height = len(input)
        self.values = [0] * (self.width * self.height)
        for y in range(self.height):
            for x in range(self.width):
                self.set(x, y, int(input[y][x]))

    def coordToIndex(self, x, y):
        return y * self.width + x

    def set(self, x, y, value):
        idx = self.coordToIndex(x, y)
        self.values[idx] = value

    def get(self, x, y):
        idx = self.coordToIndex(x, y)
        return self.values[idx]

    def visibleInDirection(self, x, y, dx, dy):
        base_value = self.get(x, y)
        cx = x + dx
        cy = y + dy
        while (cx >= 0 and cx < self.width and cy >= 0 and cy < self.height):
            if self.get(cx, cy) >= base_value:
                return False
            cx += dx
            cy += dy
        return True

    def visible(self, x, y):
        return self.visibleInDirection(x, y, -1, 0) or self.visibleInDirection(x, y, 1, 0) or \
               self.visibleInDirection(x, y, 0, -1) or self.visibleInDirection(x, y, 0, 1)

    def scoreInDirection(self, x, y, dx, dy):
        base_value = self.get(x, y)
        cx = x + dx
        cy = y + dy
        score = 0
        while (cx >= 0 and cx < self.width and cy >= 0 and cy < self.height):
            score += 1
            if self.get(cx, cy) >= base_value:
                return score
            cx += dx
            cy += dy
        return score

    def score(self, x, y):
        return self.scoreInDirection(x, y, -1, 0) * self.scoreInDirection(x, y, 1, 0) * \
               self.scoreInDirection(x, y, 0, -1) * self.scoreInDirection(x, y, 0, 1)


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        forest = TreeGrid(input_data)
        total = 0
        for x in range(forest.width):
            for y in range(forest.height):
                if forest.visible(x, y):
                    total += 1
        return total

    def solve_second(self, input_data):
        forest = TreeGrid(input_data)
        max_score = 0
        for x in range(1, forest.width - 1):
            for y in range(1, forest.height - 1):
                score = forest.score(x, y)
                if score > max_score:
                    max_score = score
        return max_score

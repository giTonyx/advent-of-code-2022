import solution


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    def __str__(self):
        return f"{self.x}#{self.y}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__repr__())

    def eq(self, other):
        return self.__repr__() == other.__repr__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def adjacent(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def move_to(self, other):
        if other.x > self.x:
            self.x += 1
            if other.y > self.y: self.y += 1
            if other.y < self.y: self.y -= 1
            return
        if other.x < self.x:
            self.x -= 1
            if other.y > self.y: self.y += 1
            if other.y < self.y: self.y -= 1
            return
        if other.y > self.y: self.y += 1
        if other.y < self.y: self.y -= 1
        return


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        head = Position(0, 0)
        tail = Position(0, 0)
        visited = set()
        visited.add(tail.__repr__())

        for command in input_data:
            direction, steps = command.split(" ")
            steps = int(steps)

            for _ in range(steps):
                if direction == "R":
                    head.x += 1
                if direction == "L":
                    head.x -= 1
                if direction == "U":
                    head.y += 1
                if direction == "D":
                    head.y -= 1

                if not tail.adjacent(head):
                    tail.move_to(head)
                    visited.add(tail.__repr__())
        return len(visited)

    def solve_second(self, input_data):
        head = Position(0, 0)
        t1 = Position(0, 0)
        t2 = Position(0, 0)
        t3 = Position(0, 0)
        t4 = Position(0, 0)
        t5 = Position(0, 0)
        t6 = Position(0, 0)
        t7 = Position(0, 0)
        t8 = Position(0, 0)
        t9 = Position(0, 0)
        visited = set()
        visited.add(t9.__repr__())

        ropes = [head, t1, t2, t3, t4, t5, t6, t7, t8, t9]

        for command in input_data:
            direction, steps = command.split(" ")
            steps = int(steps)

            for _ in range(steps):
                if direction == "R":
                    head.x += 1
                if direction == "L":
                    head.x -= 1
                if direction == "U":
                    head.y += 1
                if direction == "D":
                    head.y -= 1

                for i in range(1, len(ropes)):
                    if not ropes[i].adjacent(ropes[i - 1]):
                        ropes[i].move_to(ropes[i - 1])

                visited.add(t9.__repr__())
        return len(visited)
        return 0

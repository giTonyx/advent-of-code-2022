import solution

rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # h line
    [(1, 0), (0, 1), (1, 1), (1, 2), (2, 1)],  # cross
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # L
    [(0, 0), (0, 1), (0, 2), (0, 3)],  # v line
    [(0, 0), (0, 1), (1, 0), (1, 1)]  # square
]


class Rock(object):
    def __init__(self, pattern, dx, dy):
        self.points = [(x + dx, y + dy) for x, y in pattern]

    def try_move(self, dx, dy, board):
        candidate_points = [(x + dx, y + dy) for x, y in self.points]
        for x, y in candidate_points:
            if x < 1 or x > 7: return False
            if y < 1: return False
            if (x, y) in board: return False
        self.points = candidate_points
        return True


class Tetris(object):
    def __init__(self, commands):
        self.commands = commands
        self.next_command = 0
        self.next_rock = 0
        self.board = set()
        self.height = 0

    def serialize(self):
        return tuple([self.next_rock, self.next_command] + [self.height - self.max_at_pos(x) for x in range(1, 8)])

    def max_at_pos(self, pos):
        return max([y for x, y in self.board if x == pos] + [0])

    def fall(self):
        entry_point_height = self.height + 4
        rock = Rock(rocks[self.next_rock], 3, entry_point_height)
        self.next_rock = (self.next_rock + 1) % len(rocks)

        while True:
            command = self.commands[self.next_command]
            self.next_command = (self.next_command + 1) % len(self.commands)

            dx = 1 if command == ">" else -1
            rock.try_move(dx, 0, self.board)
            if not rock.try_move(0, -1, self.board):
                self.settle(rock)
                break
        return

    def settle(self, rock):
        for x, y in rock.points:
            self.board.add((x, y))
            self.height = max(self.height, y)
        return


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        commands = input_data[0]
        tetris = Tetris(commands)
        for i in range(2022):
            tetris.fall()
        return tetris.height

    def solve_second(self, input_data):
        commands = input_data[0]
        tetris = Tetris(commands)
        seen = {}
        for i in range(1000000000000):
            tetris.fall()
            ser = tetris.serialize()
            if ser in seen:
                rep_start = seen[ser]
                period = i - seen[ser]
                break
            seen[ser] = i

        tetris = Tetris(commands)
        for _ in range(rep_start): tetris.fall()
        base_height = tetris.height
        for _ in range(period): tetris.fall()
        period_height = tetris.height - base_height
        num_periods = (1000000000000 - rep_start) // period
        remaining = (1000000000000 - rep_start) % period
        for _ in range(remaining): tetris.fall()
        remaining_height = tetris.height - (base_height + period_height)

        total_height = base_height + remaining_height + period_height * num_periods

        return total_height

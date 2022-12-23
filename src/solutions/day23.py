import solution


# For debug purposes
def print_grid(grid):
    min_x = min([x for x, y in grid])
    max_x = max([x for x, y in grid])
    min_y = min([y for x, y in grid])
    max_y = max([y for x, y in grid])

    result = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                result += "#"
            else:
                result += "."
        result += "\n"
    result += "\n"
    print(result)


class Direction(object):
    def __init__(self, destination, checks):
        self.destination = destination
        self.checks = checks


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        elfs = set()
        for y in range(len(input_data)):
            for x in range(len(input_data[0])):
                if input_data[y][x] == "#":
                    elfs.add((x, y))

        directions = (Direction((0, -1), ((-1, -1), (0, -1), (1, -1))),
                      Direction((0, 1), ((-1, 1), (0, 1), (1, 1))),
                      Direction((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),
                      Direction((1, 0), ((1, -1), (1, 0), (1, 1))))

        curr_direction = 0

        for i in range(10):
            proposed_moves = {}
            proposed_destination_counts = {}

            for x, y in elfs:
                # considering adjacent positions
                found = False
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if (dx != 0 or dy != 0) and (x + dx, y + dy) in elfs:
                            found = True
                if not found: continue

                # looking at directions
                for i in range(len(directions)):
                    dir = directions[(curr_direction + i) % len(directions)]
                    seen_anyone = False
                    for dx, dy in dir.checks:
                        if (x + dx, y + dy) in elfs:
                            seen_anyone = True
                    if not seen_anyone:
                        destination = (x + dir.destination[0], y + dir.destination[1])
                        proposed_moves[(x, y)] = destination
                        proposed_destination_counts[destination] = proposed_destination_counts.get(destination, 0) + 1
                        break

            # Actually move the elves
            new_elves = set()
            for x, y in elfs:
                if (x, y) in proposed_moves and proposed_destination_counts[proposed_moves[(x, y)]] == 1:
                    new_elves.add(proposed_moves[(x, y)])
                else:
                    new_elves.add((x, y))
            elfs = new_elves

            curr_direction = (curr_direction + 1) % len(directions)

        min_x = min([x for x, y in elfs])
        max_x = max([x for x, y in elfs])
        min_y = min([y for x, y in elfs])
        max_y = max([y for x, y in elfs])
        ground = ((max_x - min_x + 1) * (max_y - min_y + 1)) - len(elfs)

        return ground

    def solve_second(self, input_data):
        elfs = set()
        for y in range(len(input_data)):
            for x in range(len(input_data[0])):
                if input_data[y][x] == "#":
                    elfs.add((x, y))

        directions = (Direction((0, -1), ((-1, -1), (0, -1), (1, -1))),
                      Direction((0, 1), ((-1, 1), (0, 1), (1, 1))),
                      Direction((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),
                      Direction((1, 0), ((1, -1), (1, 0), (1, 1))))

        curr_direction = 0

        round = 0
        while True:
            round += 1
            proposed_moves = {}
            proposed_destination_counts = {}

            for x, y in elfs:
                # considering adjacent positions
                found = False
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if (dx != 0 or dy != 0) and (x + dx, y + dy) in elfs:
                            found = True
                if not found: continue

                # looking at directions
                for i in range(len(directions)):
                    dir = directions[(curr_direction + i) % len(directions)]
                    seen_anyone = False
                    for dx, dy in dir.checks:
                        if (x + dx, y + dy) in elfs:
                            seen_anyone = True
                    if not seen_anyone:
                        destination = (x + dir.destination[0], y + dir.destination[1])
                        proposed_moves[(x, y)] = destination
                        proposed_destination_counts[destination] = proposed_destination_counts.get(destination, 0) + 1
                        break

            # Actually move the elves
            new_elves = set()
            for x, y in elfs:
                if (x, y) in proposed_moves and proposed_destination_counts[proposed_moves[(x, y)]] == 1:
                    new_elves.add(proposed_moves[(x, y)])
                else:
                    new_elves.add((x, y))
            if elfs == new_elves:
                break
            elfs = new_elves

            curr_direction = (curr_direction + 1) % len(directions)


        return round

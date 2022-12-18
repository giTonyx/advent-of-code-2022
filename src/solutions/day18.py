import solution


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        faces = 0
        cubes = set()

        for line in input_data:
            x, y, z = [int(a) for a in line.split(",")]
            cubes.add((x, y, z))
            faces += 6
            if ((x - 1, y, z)) in cubes: faces -= 2
            if ((x + 1, y, z)) in cubes: faces -= 2
            if ((x, y - 1, z)) in cubes: faces -= 2
            if ((x, y + 1, z)) in cubes: faces -= 2
            if ((x, y, z - 1)) in cubes: faces -= 2
            if ((x, y, z + 1)) in cubes: faces -= 2

        return faces

    def solve_second(self, input_data):
        cubes = set()
        for line in input_data:
            x, y, z = [int(a) for a in line.split(",")]
            cubes.add((x, y, z))

        faces = 0
        # for each side, we calculate the projections, i.e. how many cubes do we see
        min_coordinate = min([min(x, y, z) for x, y, z in cubes]) - 1
        max_coordinate = max([max(x, y, z) for x, y, z in cubes]) + 1

        filled = set()
        fill_queue = [(min_coordinate, min_coordinate, min_coordinate)]
        filled.add((min_coordinate, min_coordinate, min_coordinate))

        while len(fill_queue) > 0:
            fx, fy, fz = fill_queue.pop()

            left = (fx - 1, fy, fz)
            right = (fx + 1, fy, fz)
            down = (fx, fy - 1, fz)
            up = (fx, fy + 1, fz)
            behind = (fx, fy, fz - 1)
            ahead = (fx, fy, fz + 1)

            for neighbour in (left, right, up, down, behind, ahead):
                x, y, z = neighbour
                if x < min_coordinate or y < min_coordinate or z < min_coordinate or x > max_coordinate or y > max_coordinate or z > max_coordinate:
                    continue
                if neighbour in cubes:
                    faces += 1
                    continue
                if neighbour in filled: continue
                filled.add(neighbour)
                fill_queue.append(neighbour)

        return faces

import solution

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        total = 0
        for data in input_data:
            first, second = data.split(",")
            start_a, end_a = [int(x) for x in first.split("-")]
            start_b, end_b = [int(x) for x in second.split("-")]
            if start_a <= start_b and end_a >= end_b:
                total += 1
            else:
                if start_b <= start_a and end_b >= end_a:
                    total += 1
        return total

    def solve_second(self, input_data):
        total = 0
        for data in input_data:
            first, second = data.split(",")
            start_a, end_a = [int(x) for x in first.split("-")]
            start_b, end_b = [int(x) for x in second.split("-")]

            for i in range(start_a, end_a + 1):
                if start_b <= i <= end_b:
                    total += 1
                    break

        return total
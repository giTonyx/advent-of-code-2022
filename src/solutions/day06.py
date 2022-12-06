import solution

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return open(input_filename).read().strip()

    def solve_first(self, input_data):
        for i in range(4, len(input_data)):
            if len(set(input_data[i-4:i])) == 4:
                return i
        return 0

    def solve_second(self, input_data):
        for i in range(14, len(input_data)):
            if len(set(input_data[i - 14:i])) == 14:
                return i
        return 0
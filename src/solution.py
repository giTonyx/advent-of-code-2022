class Solution:

    def __init__(self):
        return

    def parse_input(self, input_filename):
        return open(input_filename).read()

    def solve_first(self, input_data):
        return "Not Implemented Yet"

    def solve_second(self, input_data):
        return "Not Implemented Yet"

    def solve(self, input_filename):
        input_data = self.parse_input(input_filename)
        s1 = self.solve_first(input_data)
        s2 = self.solve_second(input_data)
        print(f"Solution 1: {s1}")
        print(f"Solution 2: {s2}")
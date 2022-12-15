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
        print("Solution 1: " + str(s1))
        print("Solution 2: " + str(s2))
import time
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
        pre_time = time.time()
        s1 = self.solve_first(input_data)
        post_time = time.time()
        print("Solution 1: %s (%.03fs)" % (str(s1), post_time - pre_time))

        pre_time = time.time()
        s2 = self.solve_second(input_data)
        post_time = time.time()
        print("Solution 2: %s (%.03fs)" % (str(s2), post_time - pre_time))

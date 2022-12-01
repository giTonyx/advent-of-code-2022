import solution
import heapq

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        current = max_value = 0
        for value in input_data:
            if len(value) == 0:
                current = 0
            else:
                current += int(value)
                if current > max_value:
                    max_value = current
        return max_value

    def solve_second(self, input_data):
        calories = []
        current = 0

        for value in input_data:
            if len(value) == 0:
                if len(calories) < 3:
                    heapq.heappush(calories, current)
                else:
                    heapq.heappushpop(calories, current)
                current = 0
            else:
                current += int(value)
        if len(calories) < 3:
            heapq.heappush(calories, current)
        else:
            heapq.heappushpop(calories, current)
        return sum(calories)
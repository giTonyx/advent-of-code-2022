import solution
import functools
import json

# return 0 if equal, 1 if left is bigger, -1 if left is smaller
def compare(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return -1
        if left > right:
            return 1
        return 0
    if type(left) == list and type(right) == list:
        for i in range(len(left)):
            if i >= len(right):
                return 1
            cmp = compare(left[i], right[i])
            if cmp != 0:
                return cmp
        if len(right) > len(left):
            return -1
        return 0
    if type(left) == int and type(right) == list:
        return compare([left], right)
    if type(left) == list and type(right) == int:
        return compare(left, [right])
    return

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        total = 0
        current_idx = 0
        while (current_idx * 3) < len(input_data):
            left = json.loads(input_data[current_idx * 3])
            right = json.loads(input_data[(current_idx * 3) + 1])
            current_idx += 1

            if compare(left, right) == -1:
                total += current_idx
        return total

    def solve_second(self, input_data):
        input_array = [[[2]], [[6]]]
        current_idx = 0
        while (current_idx * 3) < len(input_data):
            left = json.loads(input_data[current_idx * 3])
            right = json.loads(input_data[(current_idx * 3) + 1])
            input_array.append(left)
            input_array.append(right)
            current_idx += 1

        distress = 1
        sorted_input = sorted(input_array, key=functools.cmp_to_key(compare))
        for i in range(len(sorted_input)):
            if sorted_input[i] == [[2]] or sorted_input[i] == [[6]]:
                distress *= (i+1)
        return distress
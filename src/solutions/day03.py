import solution


def priority(letter):
    if letter.lower() == letter:
        return ord(letter) - ord('a') + 1
    return ord(letter) - ord('A') + 27


def split_half(string):
    half = len(string) // 2
    first = string[:half]
    second = string[half:]
    return (first, second)


def common_letter(first, second):
    for letter in first:
        if letter in second:
            return letter


def common_in_three(first, second, third):
    for letter in first:
        if letter in second and letter in third:
            return letter


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        total = 0
        for line in input_data:
            first, second = split_half(line)
            common = common_letter(first, second)
            p = priority(common)
            total += p
        return total

    def solve_second(self, input_data):
        total = 0
        i = 0
        while i < len(input_data):
            first = input_data[i]
            second = input_data[i + 1]
            third = input_data[i + 2]
            common = common_in_three(first, second, third)
            p = priority(common)
            total += p
            i += 3
        return total

import solution


class Janken:
    def outcome(self, other):
        if self.shape_score == other.shape_score: return 3
        if (self.shape_score - other.shape_score) % 3 == 1: return 6
        return 0


class Rock(Janken):
    shape_score = 1


class Paper(Janken):
    shape_score = 2


class Scissor(Janken):
    shape_score = 3


def from_letter(letter):
    if letter == 'A' or letter == 'X':
        return Rock()
    if letter == 'B' or letter == 'Y':
        return Paper()
    return Scissor()


def from_number(number):
    if number == 1:
        return Rock()
    if number == 2:
        return Paper()
    return Scissor()


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip().split() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        score = 0
        for first, second in input_data:
            elf = from_letter(first)
            player = from_letter(second)
            score += player.shape_score
            score += player.outcome(elf)
        return score

    def solve_second(self, input_data):
        score = 0
        for first, second in input_data:
            elf = from_letter(first)
            if second == 'X':
                player = from_number((elf.shape_score - 1) % 3)
            if second == 'Y':
                player = from_number(elf.shape_score)
            if second == 'Z':
                player = from_number((elf.shape_score + 1) % 3)
            score += player.shape_score
            score += player.outcome(elf)
        return score

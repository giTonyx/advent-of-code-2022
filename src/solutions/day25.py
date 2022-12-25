import solution

def from_snafu(snafu):
    total = 0
    for i in range(len(snafu)):
        if snafu[i] == "=": coex = -2
        elif snafu[i] == "-": coex = -1
        else: coex = int(snafu[i])
        power = len(snafu) - (i + 1)
        total += coex * (5 ** power)
    return total

def to_snafu(number):
    base5 = {}
    remaining = number
    power = 0
    while True:
        base5[power] = remaining % 5
        remaining = remaining // 5
        if remaining == 0: break
        power += 1

    power = 0
    snafu = ""
    while True:
        if power not in base5: break
        if base5[power] == 3:
            base5[power+1] = base5.get(power + 1, 0) + 1
            snafu += "="
        elif base5[power] == 4:
            base5[power+1] = base5.get(power + 1, 0) + 1
            snafu += "-"
        elif base5[power] == 5:
            base5[power + 1] = base5.get(power + 1, 0) + 1
            snafu += "0"
        else:
            snafu += str(base5[power])
        power += 1

    return snafu[::-1]

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        total = 0
        for line in input_data:
            total += from_snafu(line)
        return to_snafu(total)

    def solve_second(self, input_data):
        return 0

import solution


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip('\n') for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        num_stacks = (len(input_data[0]) + 1) // 4
        stacks = []
        for _ in range(num_stacks):
            stacks.append([])

        initial_drawing = True
        for data in input_data:
            if len(data) == 0:
                initial_drawing = False
                continue

            if initial_drawing:
                for i in range(num_stacks):
                    crate = data[4 * i + 1]
                    if crate == " ": continue
                    stacks[i].insert(0, crate)
            else:
                _, quantity, _, source, _, destination = data.split()
                quantity = int(quantity)
                source = int(source)
                destination = int(destination)

                for _ in range(quantity):
                    elem = stacks[source - 1].pop()
                    stacks[destination - 1].append(elem)

        answer = ""
        for s in stacks:
            if len(s) > 0:
                answer += s[-1]
        return answer

    def solve_second(self, input_data):
        num_stacks = (len(input_data[0]) + 1) // 4
        stacks = []
        for _ in range(num_stacks):
            stacks.append([])

        initial_drawing = True
        for data in input_data:
            if len(data) == 0:
                initial_drawing = False
                continue

            if initial_drawing:
                for i in range(num_stacks):
                    crate = data[4 * i + 1]
                    if crate == " ": continue
                    stacks[i].insert(0, crate)
            else:
                _, quantity, _, source, _, destination = data.split()
                quantity = int(quantity)
                source = int(source)
                destination = int(destination)

                to_move = stacks[source - 1][-quantity:]
                for _ in range(quantity): stacks[source - 1].pop()
                stacks[destination - 1] += to_move

        answer = ""
        for s in stacks:
            if len(s) > 0:
                answer += s[-1]
        return answer

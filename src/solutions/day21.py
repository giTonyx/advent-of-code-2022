import solution


class MonkeyOp(object):
    def __init__(self, monkey1, monkey2, operation):
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operation = operation

    def calculate(self, value1, value2):
        if self.operation == "+": return value1 + value2
        if self.operation == "-": return value1 - value2
        if self.operation == "*": return value1 * value2
        if self.operation == "/": return value1 / value2

    def reverse1(self, result, value2):
        if self.operation == "+": return result - value2
        if self.operation == "-": return result + value2
        if self.operation == "*": return result / value2
        if self.operation == "/": return result * value2

    def reverse2(self, result, value1):
        if self.operation == "+": return result - value1
        if self.operation == "-": return value1 - result
        if self.operation == "*": return result / value1
        if self.operation == "/": return value1 / result

    def __repr__(self):
        return "%s %s %s" % (self.monkey1, self.operation, self.monkey2)


class Troop(object):
    def __init__(self):
        self.monkey_values = {}
        self.monkey_ops = {}
        self.dependendants = {}
        return

    def add_monkey(self, name, value):
        if " " in value:
            m1, op, m2 = value.strip().split(" ")
            self.monkey_ops[name] = MonkeyOp(m1, m2, op)
            if m1 not in self.dependendants: self.dependendants[m1] = []
            self.dependendants[m1].append(name)
            if m2 not in self.dependendants: self.dependendants[m2] = []
            self.dependendants[m2].append(name)
        else:
            self.monkey_values[name] = int(value)
        return

    # Here we assume that a monkey is used to calculate at most another monkey, which is correct for my input
    def get_path(self, name):
        if name not in self.dependendants: return []
        if len(self.dependendants[name]) > 1: print("Assumption broke, result might be incorrect")
        parent = self.dependendants[name][0]
        return [parent] + self.get_path(parent)

    def balance(self):
        human_path = ["humn"] + self.get_path("humn")
        root_op = self.monkey_ops["root"]
        if root_op.monkey1 in human_path:
            value = self.get(root_op.monkey2)
        else:
            value = self.get(root_op.monkey1)

        human_path.reverse()
        for i in range(1, len(human_path) - 1):
            op_monkey = human_path[i]
            child_monkey = human_path[i + 1]
            op = self.monkey_ops[op_monkey]
            if child_monkey == op.monkey1:
                value = op.reverse1(value, self.get(op.monkey2))
            else:
                value = op.reverse2(value, self.get(op.monkey1))
        return value

    def get(self, name):
        while name not in self.monkey_values:
            for monkey, op in self.monkey_ops.items():
                if monkey in self.monkey_values: continue
                if op.monkey1 in self.monkey_values and op.monkey2 in self.monkey_values:
                    value = op.calculate(self.monkey_values[op.monkey1], self.monkey_values[op.monkey2])
                    self.monkey_values[monkey] = value
        return self.monkey_values[name]


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        troop = Troop()
        for line in input_data:
            name, value = line.split(":")
            troop.add_monkey(name, value.strip())

        return troop.get("root")

    def solve_second(self, input_data):
        troop = Troop()
        for line in input_data:
            name, value = line.split(":")
            troop.add_monkey(name, value.strip())

        return troop.balance()

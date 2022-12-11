import solution
import heapq
from math import lcm

class Troop(object):
    def __init__(self):
        self.monkeys = {}
        return

    def add(self, input):
        name = int(input[0].split(" ")[1].strip(":"))
        starting_items = [int(x) for x in input[1].split(":")[1].split(",")]
        operation = input[2].split(" ")[-2]
        operation_value = input[2].split(" ")[-1]
        mod_test = int(input[3].split(" ")[-1])
        true_target = int(input[4].split(" ")[-1])
        false_target = int(input[5].split(" ")[-1])
        self.monkeys[name] = Monkey(name, starting_items, operation, operation_value, mod_test, true_target, false_target)
        return

    def do_round(self, divide_worry):
        idx = 0
        least_common_multiplier = lcm(*[x.mod_test for x in self.monkeys.values()])
        while idx in self.monkeys:
            for (item, monkey) in self.monkeys[idx].throw(divide_worry):
                if not divide_worry:
                    item = item % least_common_multiplier
                self.monkeys[monkey].items.append(item)
            idx += 1
        return

    def inspections(self):
        return [x.inspected for x in self.monkeys.values()]

class Monkey(object):
    def __init__(self, name, starting_items, operation, operation_value, mod_test, true_target, false_target):
        self.name = name # not needed, really. just for debug
        self.items = starting_items[:]
        self.operation = operation
        self.operation_value = operation_value
        self.mod_test = mod_test
        self.true_target = true_target
        self.false_target = false_target
        self.inspected = 0

    def throw(self, divide_worry):
        result = []

        for item in self.items:
            self.inspected += 1
            value = item if self.operation_value == "old" else int(self.operation_value)
            new_value = item * value if self.operation == "*" else item + value
            if divide_worry: new_value = new_value // 3
            target = self.true_target if (new_value % self.mod_test) == 0 else self.false_target
            result.append((new_value, target))

        self.items = []
        return result

def load_troop(lines):
    idx = 0
    troop = Troop()
    while idx < len(lines):
        monkey_definition = lines[idx:idx + 6]
        troop.add(monkey_definition)
        idx += 7
    return troop


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        troop = load_troop(input_data)
        for _ in range(20):
            troop.do_round(True)
        all_inspections = troop.inspections()
        top_inspections = []
        heapq.heappush(top_inspections, all_inspections[0])
        heapq.heappush(top_inspections, all_inspections[1])
        for i in all_inspections[2:]:
            heapq.heappushpop(top_inspections, i)
        return top_inspections[0] * top_inspections[1]

    def solve_second(self, input_data):
        troop = load_troop(input_data)
        for i in range(10000):
            troop.do_round(False)
        all_inspections = troop.inspections()
        top_inspections = []
        heapq.heappush(top_inspections, all_inspections[0])
        heapq.heappush(top_inspections, all_inspections[1])
        for i in all_inspections[2:]:
            heapq.heappushpop(top_inspections, i)
        return top_inspections[0] * top_inspections[1]

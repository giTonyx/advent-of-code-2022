import solution
import re
from collections import deque


class Valve(object):
    def __init__(self, name, rate, exits):
        self.name = name
        self.rate = rate
        self.exits = exits

    def __repr__(self):
        return "%s r%d -> %s" % (self.name, self.rate, self.exits)


class State(object):
    def __init__(self, minute, position, opened, rate, total):
        self.minute = minute
        self.position = position
        self.opened = opened
        self.rate = rate
        self.total = total

    def __repr__(self):
        return "T%s @%s OP:%s r%d total: %d flow: %d" % (
        self.minute, self.position, self.opened, self.rate, self.total, self.flow())

    def flow(self, end=30):
        return self.total + (end - self.minute + 1) * self.rate


def valve_distance(valves, start, end):
    if start == end: return 0
    seen = set()
    seen.add(start)
    to_visit = deque()
    for exit in valves[start].exits:
        seen.add(exit)
        to_visit.append((exit, 1))
    while len(to_visit) > 0:
        valve, steps = to_visit.popleft()
        if valve == end: return steps
        for exit in valves[valve].exits:
            if exit not in seen:
                seen.add(exit)
                to_visit.append((exit, steps + 1))
    print("No path found")
    return None  # couldn't find


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        valves = {}
        input_exp = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
        for line in input_data:
            name, rate, exit_part = input_exp.search(line).groups()
            rate = int(rate)
            exits = [x.strip(",") for x in exit_part.split(" ")]
            valves[name] = Valve(name, rate, exits)

        good_valves = [x.name for x in valves.values() if x.rate > 0]

        distances = {}
        for valve in valves.keys():
            distances[valve] = {}
            for target in good_valves:
                distances[valve][target] = valve_distance(valves, valve, target)

        initial_state = State(1, "AA", [], 0, 0)
        max_flow = 0
        states = [initial_state]
        while len(states):
            state = states.pop()
            max_flow = max(max_flow, state.flow())
            valve = valves[state.position]
            if state.minute == 30:
                continue
            if state.position not in state.opened and valve.rate > 0:
                states.append(
                    State(state.minute + 1, state.position, state.opened[:] + [state.position], state.rate + valve.rate,
                          state.total + state.rate))
                continue
            for dest_valve in good_valves:
                if dest_valve in state.opened:
                    continue
                distance = distances[state.position][dest_valve]
                if (state.minute + distance) > 29:
                    continue
                states.append(State(state.minute + distance, dest_valve, state.opened, state.rate,
                                    state.total + (state.rate * distance)))

        return max_flow

    def solve_second(self, input_data):
        valves = {}
        input_exp = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to (.+)")
        for line in input_data:
            name, rate, exit_part = input_exp.search(line).groups()
            rate = int(rate)
            exits = [x.strip(",") for x in exit_part.split(" ")[1:]]
            valves[name] = Valve(name, rate, exits)

        good_valves = [x.name for x in valves.values() if x.rate > 0]

        distances = {}
        for valve in valves.keys():
            distances[valve] = {}
            for target in good_valves:
                distances[valve][target] = valve_distance(valves, valve, target)

        best_states = {}
        all_states = {}
        initial_state = State(1, "AA", [], 0, 0)
        states = [initial_state]
        while len(states):
            state = states.pop()
            valve = valves[state.position]
            if state.minute == 26:
                continue
            if state.position not in state.opened and valve.rate > 0:
                state = State(state.minute + 1, state.position, state.opened[:] + [state.position],
                              state.rate + valve.rate, state.total + state.rate)
                states.append(state)
                opened = state.opened
                opened.sort()
                opened = tuple(opened)
                if best_states.get(opened, 0) < state.flow(26):
                    best_states[opened] = state.flow(26)
                    all_states[opened] = state
                continue
            for dest_valve in good_valves:
                if dest_valve in state.opened:
                    continue
                distance = distances[state.position][dest_valve]
                if (state.minute + distance) > 29:
                    continue
                states.append(State(state.minute + distance, dest_valve, state.opened, state.rate,
                                    state.total + (state.rate * distance)))

        max_flow = 0
        for human in all_states.values():
            for elephant in all_states.values():
                good_state = True
                for v in human.opened:
                    if v in elephant.opened:
                        good_state = False
                        break
                if good_state:
                    max_flow = max(max_flow, human.flow(26) + elephant.flow(26))

        return max_flow

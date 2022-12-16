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
        return "T%s @%s OP:%s r%d total: %d flow: %d" % (self.minute, self.position, self.opened, self.rate, self.total, self.flow())

    def flow(self):
        return self.total + (30 - self.minute + 1) * self.rate

class DualState(object):
    def __init__(self, minute, h_target, h_distance, e_target, e_distance, opened, rate, total):
        self.minute = minute
        self.h_target = h_target
        self.h_distance = h_distance
        self.e_target = e_target
        self.e_distance = e_distance
        self.opened = opened
        self.rate = rate
        self.total = total

    def flow(self):
        return self.total + (26 - self.minute + 1) * self.rate

    def __repr__(self):
        return "T%d H%s-(%d) E%s-(%d) opened: %s rate: %d so far: %d flow: %d" % (self.minute, self.h_target, self.h_distance, self.e_target, self.e_distance, self.opened, self.rate, self.total, self.flow())

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
    return None # couldn't find

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
                states.append(State(state.minute + 1, state.position, state.opened[:] + [state.position], state.rate + valve.rate, state.total + state.rate))
                continue
            for dest_valve in good_valves:
                if dest_valve in state.opened:
                    continue
                distance = distances[state.position][dest_valve]
                if (state.minute + distance) > 29:
                    continue
                states.append(State(state.minute + distance, dest_valve, state.opened, state.rate, state.total + (state.rate * distance)))

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

        initial_state = DualState(1, "AA", 0, "AA", 0, [], 0, 0)
        max_flow = 0
        states = [initial_state]

        while len(states):
            state = states.pop()
            max_flow = max(max_flow, state.flow())

            # Out of time
            if state.minute >= 26: continue

            human_valve = valves[state.h_target]
            elephant_valve = valves[state.e_target]

            # Can the human open?
            if state.h_distance == 0 and state.h_target not in state.opened and human_valve.rate > 0:
                # Is the elephant moving?
                if state.e_distance > 0:
                    states.append(DualState(state.minute + 1, state.h_target, 0, state.e_target, state.e_distance - 1, state.opened[:] + [state.h_target], state.rate + human_valve.rate, state.total + state.rate))
                    continue
                # Can the elephant open as well?
                if state.e_target not in state.opened and elephant_valve.rate > 0:
                    states.append(DualState(state.minute + 1, state.h_target, 0, state.e_target, 0, state.opened[:] + [state.h_target, state.e_target], state.rate + human_valve.rate + elephant_valve.rate, state.total + state.rate))
                    continue
                # Find a target for the elephant
                elephant_target_found = False
                for dest_valve in good_valves:
                    if dest_valve in state.opened or dest_valve == state.h_target: continue
                    distance = distances[state.e_target][dest_valve]
                    if (state.minute + distance) > 25: continue
                    states.append(DualState(state.minute + 1, state.h_target, 0, dest_valve, distance - 1, state.opened[:] + [state.h_target], state.rate + human_valve.rate, state.total + state.rate))
                    elephant_target_found = True

                # Elephant stays still
                if not elephant_target_found:
                    states.append(DualState(state.minute + 1, state.h_target, 0, state.e_target, 0, state.opened[:] + [state.h_target], state.rate + human_valve.rate, state.total + state.rate))
                continue

            # Can the elephant (but not the human) open?
            if state.e_distance == 0 and state.e_target not in state.opened and elephant_valve.rate > 0:
                # is the human moving?
                if state.h_distance > 0:
                    states.append(DualState(state.minute + 1, state.h_target, state.h_distance - 1, state.e_target, 0, state.opened[:] + [state.e_target], state.rate + elephant_valve.rate, state.total + state.rate))
                    continue
                # find a target for the human
                human_target_found = False
                for dest_valve in good_valves:
                    if dest_valve in state.opened or dest_valve == state.e_target or dest_valve == state.h_target: continue
                    distance = distances[state.h_target][dest_valve]
                    if (state.minute + distance) > 25: continue
                    states.append(DualState(state.minute + 1, dest_valve, distance - 1, state.e_target, 0, state.opened[:] + [state.e_target], state.rate + elephant_valve.rate, state.total + state.rate))
                    human_target_found = True
                # human stays still
                if not human_target_found:
                    states.append(DualState(state.minute + 1, state.h_target, 0, state.e_target, 0, state.opened[:] + [state.e_target], state.rate + elephant_valve.rate, state.total + state.rate))
                continue

            # Human moving but elephant done
            if state.h_distance > 0 and state.e_distance == 0:
                # Find a target for the elephant
                elephant_target_found = False
                for dest_valve in good_valves:
                    if dest_valve in state.opened or dest_valve == state.h_target: continue
                    distance = distances[state.e_target][dest_valve]
                    if (state.minute + distance) > 25: continue
                    min_distance = min(distance, state.h_distance)
                    states.append(DualState(state.minute + min_distance, state.h_target, state.h_distance - min_distance, dest_valve, distance - min_distance, state.opened, state.rate, state.total + (state.rate * min_distance)))
                    elephant_target_found = True

                # Elephant stays still
                if not elephant_target_found:
                    states.append(DualState(state.minute + state.h_distance, state.h_target, 0, state.e_target, 0, state.opened, state.rate, state.total + (state.rate * state.h_distance)))
                continue

            # Elephant moving but human done
            if state.e_distance > 0 and state.h_distance == 0:
                # Find a target for the human
                human_target_found = False
                for dest_valve in good_valves:
                    if dest_valve in state.opened or dest_valve == state.e_target: continue
                    distance = distances[state.h_target][dest_valve]
                    if (state.minute + distance) > 25: continue
                    min_distance = min(distance, state.e_distance)
                    states.append(DualState(state.minute + min_distance, dest_valve, distance - min_distance, state.e_target, state.e_distance - min_distance, state.opened, state.rate, state.total + (state.rate * min_distance)))
                    human_target_found = True

                # Elephant stays still
                if not human_target_found:
                    states.append(DualState(state.minute + state.e_distance, state.h_target, 0, state.e_target, 0, state.opened, state.rate, state.total + (state.rate * state.e_distance)))
                continue

            # Find a target for both
            human_target_found = False
            for h_dest in good_valves:
                if h_dest in state.opened or h_dest == state.e_target: continue
                h_distance = distances[state.h_target][h_dest]
                if h_distance + state.minute > 25: continue
                human_target_found = True

                elephant_target_found = False
                for e_dest in good_valves:
                    if e_dest in state.opened or e_dest == h_dest: continue
                    e_distance = distances[state.e_target][e_dest]
                    if e_distance + state.minute > 25: continue

                    min_distance = min(h_distance, e_distance)
                    states.append(DualState(state.minute + min_distance, h_dest, h_distance - min_distance, e_dest, e_distance - min_distance, state.opened, state.rate, state.total + (state.rate * min_distance)))
                    elephant_target_found = True

                # Only the human move
                if not elephant_target_found:
                    states.append(DualState(state.minute + h_distance, h_dest, 0, state.e_target, 0, state.opened, state.rate, state.total + (state.rate * h_distance)))
            if not human_target_found:
                # Maybe the elephant can move
                for e_dest in good_valves:
                    if e_dest in state.opened : continue
                    e_distance = distances[state.e_target][e_dest]
                    if e_distance + state.minute > 25: continue

                    states.append(DualState(state.minute + e_distance, state.h_target, 0, e_dest, 0, state.opened, state.rate, state.total + (state.rate * e_distance)))


        return max_flow
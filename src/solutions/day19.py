import solution
import re
from collections import deque

class Blueprint(object):
    def __init__(self, name, ore, clay, obbsidian_ore, obsidian_clay, geode_ore, geode_obsidian):
        self.name = int(name)
        self.ore = int(ore)
        self.clay = int(clay)
        self.obsidian_ore = int(obbsidian_ore)
        self.obsidian_clay = int(obsidian_clay)
        self.geode_ore = int(geode_ore)
        self.geode_obsidian = int(geode_obsidian)

    def __repr__(self):
        return "Blueprint %d: ore: %d clay: %d obsidian %d-%d geode %d-%d" % (self.name, self.ore, self.clay, self.obsidian_ore, self.obsidian_clay, self.geode_ore, self.geode_obsidian)

    def max_geodes_at(self, max_minute):
        max_geode = 0
        states = deque()
        states.append((1,(0,0,0,0,1,0,0,0)))
        seen = set()
        seen.add((0,0,0,0,1,0,0,0))

        max_obsidian_robots = self.geode_obsidian
        max_ore_robots = max(self.ore, self.clay, self. obsidian_ore, self.geode_ore)
        max_clay_robots = self.obsidian_clay

        while len(states) > 0:
            minute, state = states.popleft()
            ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots = state
            max_geode = max(max_geode, geode + geode_robots)
            if minute >= max_minute: continue

            if ore >= self.geode_ore and obsidian >= self.geode_obsidian:
                new_state = (ore - self.geode_ore + ore_robots, clay + clay_robots, obsidian - self.geode_obsidian + obsidian_robots, geode + geode_robots, ore_robots, clay_robots, obsidian_robots, geode_robots + 1 )
                if new_state in seen: continue
                seen.add(new_state)
                states.append((minute + 1, new_state))
                continue

            new_states = []
            if ore >= self.obsidian_ore and clay >= self.obsidian_clay and obsidian_robots < max_obsidian_robots:
                new_state = (ore - self.obsidian_ore + ore_robots, clay - self.obsidian_clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots,
                             ore_robots, clay_robots, obsidian_robots +1 , geode_robots)
                new_states.append(new_state)

            if ore >= self.clay and clay_robots < max_clay_robots:
                new_state = (ore - self.clay + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots,
                             ore_robots, clay_robots + 1, obsidian_robots, geode_robots)
                new_states.append(new_state)

            if ore >= self.ore and ore_robots < max_ore_robots:
                new_state = (ore - self.ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots,
                             ore_robots + 1, clay_robots, obsidian_robots, geode_robots)
                new_states.append(new_state)

            if len(new_states) == 0:
                new_state = (ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geode + geode_robots,
                             ore_robots, clay_robots, obsidian_robots, geode_robots)
                new_states.append(new_state)

            for state in new_states:
                if state in seen: continue
                seen.add(state)
                states.append((minute + 1, state))

        return max_geode

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        input_lines = open(input_filename).readlines()
        blueprints = []
        blue_exp = re.compile("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
        for line in input_lines:
            blueprint = Blueprint(*blue_exp.search(line.strip()).groups())
            blueprints.append(blueprint)
        return blueprints

    def solve_first(self, blueprints):
        total = 0
        for b in blueprints:
            total += b.name * b.max_geodes_at(24)
        return total

    def solve_second(self, blueprints):
        total = 1
        for b in blueprints[:3]:
            total *= b.max_geodes_at(32)
        return total

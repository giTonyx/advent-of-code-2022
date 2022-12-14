import solution
from advent_of_code_ocr import convert_6

class CPU(object):
    def __init__(self):
        self.cycle = 0
        self.X = 1
        self.signals = {}
        return

    def execute(self, commands):
        for c in commands:
            if c == "noop":
                self.cycle += 1
                self.signals[self.cycle] = self.X
            if c.startswith("addx"):
                value = int(c.split(" ")[1])
                self.cycle += 1
                self.signals[self.cycle] = self.X
                self.cycle += 1
                self.signals[self.cycle] = self.X
                self.X += value
        return

    def signal(self, clock):
        return self.signals[clock] * clock

class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        cpu = CPU()
        cpu.execute(input_data)
        total = cpu.signal(20) + cpu.signal(60) + cpu.signal(100) + cpu.signal(140) + cpu.signal(180) + cpu.signal(220)
        return total

    def solve_second(self, input_data):
        cpu = CPU()
        cpu.execute(input_data)
        crt = ""
        for i in range(40*6):
            p = i % 40
            if abs(cpu.signals[i+1] - p) <= 1:
                crt += "#"
            else:
                crt += "."
            if p == 39:
                crt += "\n"
        return convert_6(crt.strip())

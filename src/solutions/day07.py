import solution

class File(object):
    def __init__(self, name, size):
        self.name = name
        self.size = int(size)

class Directory(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.directories = []

    def full_name(self):
        fullname = self.name
        if self.parent is not None:
            fullname = self.parent.full_name() + "." + fullname
        return fullname

    def find_directory(self, name):
        for d in self.directories:
            if d.name == name:
                return d

    def get_size(self, sizes):
        total = 0
        for f in self.files:
            total += f.size
        for d in self.directories:
            total += d.get_size(sizes)
        sizes[self.full_name()] = total
        return total

def read_commands(commands):
    root = Directory("/", None)
    current = root
    for command in commands:
        if command.startswith("$ "):
            util = command[2:]
            if util.startswith("cd"):
                target = util.split(" ")[1]
                if target == "/":
                    current = root
                    continue
                if target == "..":
                    current = current.parent
                    continue
                current = current.find_directory(target)
        else:
            if command.startswith("dir "):
                name = command.split(" " )[1]
                current.directories.append(Directory(name, current))
            else:
                size, name = command.split(" ")
                current.files.append(File(name, size))
    return root


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [x.strip() for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        root = read_commands(input_data)
        sizes = {}
        root.get_size(sizes)
        total = 0
        for folder, size in sizes.items():
            if size <= 100000:
                total += size
        return total

    def solve_second(self, input_data):
        root = read_commands(input_data)
        sizes = {}
        root.get_size(sizes)
        total = 70000000
        target = 30000000
        unused = total - sizes['/']
        if target > unused:
            needed = target - unused
        else:
            needed = 0
        min_delete = total
        for size in sizes.values():
            if size >= needed and size < min_delete:
                min_delete = size
        return min_delete

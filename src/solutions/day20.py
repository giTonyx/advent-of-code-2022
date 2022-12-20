import solution


class Solver(solution.Solution):

    def parse_input(self, input_filename):
        return [int(x.strip()) for x in open(input_filename).readlines()]

    def solve_first(self, input_data):
        mixing_array = []
        for n in input_data:
            mixing_array.append((n, False))

        for _ in range(len(input_data)):
            for old_index in range(len(input_data)):
                if mixing_array[old_index][1] == False:
                    break
            value = mixing_array[old_index][0]
            del (mixing_array[old_index])
            new_index = (old_index + value) % len(mixing_array)
            mixing_array.insert(new_index, (value, True))

        mixed_array = [x for x, y in mixing_array]

        idx1 = (mixed_array.index(0) + 1000) % len(mixed_array)
        idx2 = (mixed_array.index(0) + 2000) % len(mixed_array)
        idx3 = (mixed_array.index(0) + 3000) % len(mixed_array)
        coords = mixed_array[idx1] + mixed_array[idx2] + mixed_array[idx3]
        return coords

    def solve_second(self, input_data):
        key = 811589153
        mixing_array = []
        for i in range(len(input_data)):
            mixing_array.append(((input_data[i] * key, i, 10)))

        for iteration in range(10):
            iterations_left = 10 - iteration

            for i in range(len(input_data)):
                for old_index in range(len(input_data)):
                    if mixing_array[old_index][2] == iterations_left and mixing_array[old_index][1] == i:
                        break
                value = mixing_array[old_index][0]
                del (mixing_array[old_index])
                new_index = (old_index + value) % len(mixing_array)
                mixing_array.insert(new_index, (value, i, iterations_left - 1))

        mixed_array = [x for x, y, z in mixing_array]

        idx1 = (mixed_array.index(0) + 1000) % len(mixed_array)
        idx2 = (mixed_array.index(0) + 2000) % len(mixed_array)
        idx3 = (mixed_array.index(0) + 3000) % len(mixed_array)
        coords = mixed_array[idx1] + mixed_array[idx2] + mixed_array[idx3]
        return coords

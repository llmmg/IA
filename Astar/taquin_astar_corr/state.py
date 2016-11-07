from copy import deepcopy


class State(object):

    def __init__(self, values, parent=None):
        self.values = values
        self.parent = parent
        self.dist = None
        self.g = 0
        current_parent = self.parent
        while(current_parent is not None):
            self.g += 1
            current_parent = current_parent.parent

    def legal(self):
        return True

    def final(self, final_values):
        return self.values == final_values

    def lazy_distance(self, final_values):
        if self.dist == None:
            self.dist = self.distance(final_values)
        return self.dist

    def distance(self, final_values):
        dist = 0
        for x, line in enumerate(final_values):
            for y, elem in enumerate(line):
                x2, y2 = self.where_is_x(self.values, elem)
                dist += abs(x - x2) + abs(y - y2)
        return dist + self.g

    @staticmethod
    def where_is_x(values, number):
        for x, line in enumerate(values):
            for y, elem in enumerate(line):
                if elem == number:
                    return x, y


    def __hash__(self):
        return str(self).__hash__()

    def __str__(self):
        return str(self.values)

    def __eq__(self, other):
        return self.values == other.values

    @classmethod
    def swap(cls, values, x1, y1, x2, y2):
        new_values = deepcopy(values)
        new_values[x1][y1], new_values[x2][y2] = new_values[x2][y2], new_values[x1][y1]
        return new_values

    def applicable_operators(self):
        ops = []
        #  print(self.values)
        for i, line in enumerate(self.values):
            for j, e in enumerate(line):
                if self.values[i][j] == 0:
                    if i > 0:
                        ops.append(self.swap(self.values, i, j, i-1, j))
                    if i < len(self.values) - 1:
                        ops.append(self.swap(self.values, i, j, i+1, j))
                    if j > 0:
                        ops.append(self.swap(self.values, i, j, i, j-1))
                    if j < len(line) - 1:
                        ops.append(self.swap(self.values, i, j, i, j+1))
                    return ops  # optimization

        return ops

    def apply(self, op):
        return State(op, self)

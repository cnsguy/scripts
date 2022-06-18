from itertools import product

class Or:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, values):
        return self.lhs.eval(values) or self.rhs.eval(values)

class And:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def eval(self, values):
        return self.lhs.eval(values) and self.rhs.eval(values)

class Not:
    def __init__(self, subexpr):
        self.subexpr = subexpr

    def eval(self, values):
        return not self.subexpr.eval(values)

class ValueRef:
    def __init__(self, value_idx):
        self.value_idx = value_idx

    def eval(self, values):
        return values[self.value_idx]

def sat(expr, num_values):
    results = []

    for value in product([True, False], repeat = num_values):
        print(value)

        if expr.eval(value):
            results.append(value)

    return results

def main():
    expr = Or(ValueRef(0), ValueRef(1))
    results = sat(expr, 2)

    for result in results:
        print("Satisfies expression:", result)

main()
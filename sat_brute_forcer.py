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

def next_value(values):
    idx = len(values) - 1

    while True:
        if idx == -1: # 0 is obviously a valid index, hence this is the termination condition
            return None

        if values[idx] != True:
            break

        values[idx] = False
        idx -= 1

    values[idx] = True
    return values

def sat(expr, values):
    results = []

    while values is not None:
        if expr.eval(values):
            results.append([x for x in values])

        values = next_value(values)

    return results

def main():
    start_values = [False] * 2
    expr = Or(ValueRef(0), Not(ValueRef(1)))
    results = sat(expr, start_values)

    for result in results:
        print("Satisfies expression:", result)

main()
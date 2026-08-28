def is_variable(x):
    return isinstance(x, str) and x.startswith("?")


def substitute(term, bindings):
    if is_variable(term) and term in bindings:
        return bindings[term]
    return term


def unify(pattern, goal, bindings=None):
    if bindings is None:
        bindings = {}

    if len(pattern) != len(goal):
        return None

    bindings = bindings.copy()

    for p, g in zip(pattern, goal):
        p = substitute(p, bindings)
        g = substitute(g, bindings)

        if p == g:
            continue

        if is_variable(p):
            bindings[p] = g
        elif is_variable(g):
            bindings[g] = p
        else:
            return None

    return bindings


def apply_bindings(statement, bindings):
    return tuple(substitute(x, bindings) for x in statement)


class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, conclusion, premises):
        self.rules.append((conclusion, premises))

    def prove(self, goal, visited=None):
        if visited is None:
            visited = set()

        if goal in visited:
            return False

        visited = visited | {goal}

        for fact in self.facts:
            if unify(fact, goal) is not None:
                return True

        for conclusion, premises in self.rules:
            bindings = unify(conclusion, goal)

            if bindings is None:
                continue

            success = True

            for premise in premises:
                new_premise = apply_bindings(premise, bindings)

                if not self.prove(new_premise, visited):
                    success = False
                    break

            if success:
                return True

        return False
def parse_grammar(rules):
    grammar = {}
    for rule in rules:
        head, productions = rule.split("->")
        head = head.strip()
        grammar[head] = [' '.join(p.strip()).split() for p in productions.split("|")]

    print(grammar)
    print(grammar)
    return grammar


def is_complete(state):
    _, rule, dot, _ = state
    return dot >= len(rule)


def next_symbol(state):
    _, rule, dot, _ = state
    return rule[dot] if dot < len(rule) else None


class EarleyParser:
    def __init__(self, grammar):
        self.grammar = parse_grammar(grammar)
        self.states = []
        self.final_state = ("S1", [next(iter(self.grammar))], 1, 0)
        self.result = False

    def parse(self, word):
        self.states = [[] for _ in range(len(word) + 1)]
        print([next(iter(self.grammar))])
        self.states[0].append(("S1", [next(iter(self.grammar))], 0, 0))  # Start state

        for i in range(len(word) + 1):
            for state in self.states[i]:
                if is_complete(state):
                    self.completer(state, i)
                elif next_symbol(state) in self.grammar:
                    self.predictor(state, i)
                elif next_symbol(state) is not None:
                    self.scanner(state, i, word)


        self.result = self.final_state in self.states[len(word)]

        return self.result

    def predictor(self, state, i):
        _, rule, dot, _ = state
        symbol = next_symbol(state)
        for production in self.grammar[symbol]:
            new_state = (symbol, production, 0, i)
            if new_state not in self.states[i]:
                self.states[i].append(new_state)

    def scanner(self, state, i, word):
        if i < len(word):
            _, rule, dot, origin = state
            symbol = next_symbol(state)
            if symbol == word[i]:
                new_state = (state[0], rule, dot + 1, origin)
                if new_state not in self.states[i + 1]:
                    self.states[i + 1].append(new_state)
            elif symbol in ["(", ")"] and word[i] == symbol:  # Special case for parentheses
                new_state = (state[0], rule, dot + 1, origin)
                if new_state not in self.states[i + 1]:
                    self.states[i + 1].append(new_state)

    def completer(self, state, i):
        head, rule, dot, origin = state
        for s in self.states[origin]:
            if not is_complete(s) and next_symbol(s) == head:
                new_state = (s[0], s[1], s[2] + 1, s[3])
                if new_state not in self.states[i]:
                    self.states[i].append(new_state)

    def print_states(self, parsed_word):
        j: int
        flag: bool = False

        parsed_word = parsed_word.replace(" ", "")
        for i, state_set in enumerate(self.states):
            parsed_word_situation = parsed_word[:i] + "•" + parsed_word[i:]
            print(f"State {i}: {parsed_word_situation}")
            j = 0
            while j < len(state_set) and state_set[j] != self.final_state:
                flag = state_set[j] != self.final_state
                head, rule, dot, origin = state_set[j]
                dotted_rule = rule[:dot] + ["•"] + rule[dot:]
                print(f"[{head} -> {' '.join(dotted_rule).replace(" ", "")}, {origin}]")
                j += 1

        if flag and self.result:
            head, rule, dot, origin = self.final_state
            dotted_rule = rule[:dot] + ["•"] + rule[dot:]
            print(f"[{head} -> {' '.join(dotted_rule).replace(" ", "")}, {origin}]")

if __name__ == "__main__":

    print("Enter grammar rules (empty line to finish) in grouped form (S -> AB | c):")
    input_grammar = []
    while True:
        line = input().strip()
        if not line:
            break
        input_grammar.append(line)

    input_word = input("Enter word to parse: ").replace(" ", "")
    input_word = " ".join(input_word)

    parser = EarleyParser(input_grammar)
    result = parser.parse(input_word.split())
    parser.print_states(input_word)
    print("Result:", result)

    input("Press ENTER to exit...")

# S -> T + S | T
# T -> F * T | F
# F -> (S) | a
# (a)

# S -> CD
# C -> BE
# D -> AB
# A -> x | EA
# E -> y
# B -> y
# yyxy

# S -> A + S | b
# A -> S - A | a
# a + b
# a - b

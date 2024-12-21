import copy


def parse_grammar(rules) -> dict[str, list]:
    grammar = {}
    for rule in rules:
        head, productions = rule.split("->")
        head = head.strip()
        grammar[head] = [' '.join(p.strip()).split() for p in productions.split("|")]

    return grammar


def sort_grammar(grammar):
    ordered = []
    visited = set()

    def add_non_terminal(non_terminal):
        if non_terminal not in visited:
            visited.add(non_terminal)
            ordered.append(non_terminal)
            for production in grammar[non_terminal]:
                for symbol in production:
                    if symbol.isupper() and symbol not in visited:
                        add_non_terminal(symbol)

    add_non_terminal('S')
    sorted_grammar = {key: grammar[key] for key in ordered}

    return sorted_grammar


def has_left_recursion(rules: dict) -> bool:
    for key, productions in rules.items():
        for production in productions:
            if production[0] == key:
                return True
    return False


def remove_nesting(ordered_grammar: dict, N: str, N_rules: list):
    un_nested_grammar: dict = {}

    for N1 in ordered_grammar:
        current_set: list = ordered_grammar[N1]
        nested_rules: list = [sublist for sublist in current_set if N in sublist]
        current_set: list = [item for item in current_set if item not in nested_rules]

        non_nested_rules: list = []

        for sublist in nested_rules:
            s_index = sublist.index(N) if N in sublist else -1

            if s_index != -1:
                for numbers in N_rules:
                    new_sublist = sublist[:s_index] + numbers + sublist[s_index + 1:]
                    non_nested_rules.append(new_sublist)

        for non_nested_rule in non_nested_rules:
            current_set.append(non_nested_rule)

        un_nested_grammar[N1] = current_set

    return un_nested_grammar


def split_and_attach(d, N, new_dict):
    keys = list(d.keys())
    idx = keys.index(N)
    dict_part_1 = {key: d[key] for key in keys[:idx + 1]}
    dict_part_2 = {key: d[key] for key in keys[idx + 1:]}
    dict_part_2.update(new_dict)

    return dict_part_1, dict_part_2


def delete_left_recursion(grammar: dict) -> dict:
    grammar_without_left_recursion: dict = {}
    ordered_grammar: dict = sort_grammar(grammar)

    for N in ordered_grammar:
        current_rules = ordered_grammar[N]
        if not has_left_recursion({N: current_rules}):
            grammar_without_left_recursion[N] = current_rules
        else:
            N1 = N + "1"
            alphas: list = [lst[1:] for lst in current_rules if lst[0] == N]
            betas: list = [lst for lst in current_rules if lst[0] != N]
            alphasN1: list = copy.deepcopy(alphas)
            betasN1: list = copy.deepcopy(betas)
            for a in alphasN1:
                a.append(N1)
            for b in betasN1:
                b.append(N1)

            N_rules: list = copy.deepcopy(betas) + betasN1
            N1_rules = copy.deepcopy(alphas) + alphasN1

            grammar_without_left_recursion[N] = N_rules
            grammar_without_left_recursion[N1] = N1_rules

        keys = list(ordered_grammar.keys())
        idx = keys.index(N)
        dict_part_1 = {key: ordered_grammar[key] for key in keys[:idx + 1]}
        dict_part_2 = {key: ordered_grammar[key] for key in keys[idx + 1:]}
        dict_part_2 = remove_nesting(dict_part_2, N, current_rules)

        dict_part_1.update(dict_part_2)
        ordered_grammar = dict_part_1.copy()

    return grammar_without_left_recursion


def get_alpha_prefix(rules: list) -> list:
    alpha_prefixes: list = []
    rule_lengths: list = []
    for rule in rules:
        rule_lengths.append(len(rule))

    rule_lengths.remove(max(rule_lengths))
    second_max_rule_length: int = max(rule_lengths) # take second biggest
                                            # (in case if there are multiple max values max value will be taken)

    for j in range(second_max_rule_length):
        for i in range(len(rules)-1):
            if rules[i][j] == rules[i+1][j]:
                print(rules[i][j], rules[i+1][j])
                if not alpha_prefixes.__contains__(rules[i][j]):
                    alpha_prefixes.append(rules[i][j])

        if len(rules) > 2:
            min_len_index = min(range(len(rules)), key=lambda i: len(rules[i]))
            del rules[min_len_index]


    return alpha_prefixes

def left_factorize(grammar: dict) -> dict:
    factorized_grammar: dict = {}
    new_rules_added: bool = True

    while new_rules_added:
        new_rules_added = False
        for N in grammar:
            alpha_prefixes: list = get_alpha_prefix(grammar[N])
            if len(alpha_prefixes) > 0:
                new_rules_added = True
                N1 = N + "1"
                pass # do factorisation
            else:
                factorized_grammar[N] = grammar[N]

        grammar = factorized_grammar

    return factorized_grammar

def print_grammar(grammar):
    for non_terminal, rules in grammar.items():
        print(f"{non_terminal} -> " + " | ".join([" ".join(rule).replace(" ", "") for rule in rules]))


grammarEx = {
    'S': [['S', '+', 'A'], ['S', '-', 'A'], ['A']],
    'A': [['a'], ['b']]
}

grammarEx2 = {
    'S': [['A', 'a']],
    'B': [['C', 'c'], ['d']],
    'C': [['C', 'c', 'b', 'z'], ['d', 'b', 'z']],
    'A': [['B', 'b'], ['S', 'b']]
}

grammarEx3 = {
    'B': [['C', 'c'], ['d']],
    'C': [['C', 'c', 'b', 'z'], ['d', 'b', 'z']],
    'A': [['B', 'b'], ['S', 'b']]
}

grammarEx4 = {
    'S': [['A', 'B']],
    'A': [['C']],
    'B': [['D']],
    'C': [['b']],
    'D': [['a']]
}

grammarEx5 = {
    'S': [['A'], ['A', 'S1']],
    'S1': [['+', 'A'], ['-', 'A'], ['+', 'A', 'S1'], ['-', 'A', 'S1']],
    'A': [['a'], ['b']]
}

grammarEx6 = {
    'R': [['p', 'X'], ['p', 'a', 'R', 'T'], ['p', 'a', 'T', 'k'], ['x']]
}

grammarEx61 = {
    'R': [['p', 'X'], ['p', 'a', 'R', 'T'], ['p', 'a', 'T', 'k']]
}

grammarEx7 = {
    'R': [['a', 'b', 'C'], ['a', 'b', 'T'], ['a', 'b', 'K']]
}

grammarEx8 = {
    'R': [['a', 'b', 'C'], ['a', 'b', 'T'], ['a', 'b', 'K'], ['x']]
}


if __name__ == "__main__":

    print("Данная программа выполнена только до этапа удаления левой рекурсии.")
    print("Введите грамматику с левой рекурсией (для завершения введите пустую строку):")
    input_grammar = []
    while True:
        line = input().strip()
        if not line:
            break
        input_grammar.append(line)

    parsed_grammar = parse_grammar(input_grammar)

    without_left_rec = delete_left_recursion(parsed_grammar)
    print("Грамматика без левой рекурсии:")
    print_grammar(without_left_rec)
    input("Нажмите ENTER для завершения...")

# S -> S + A | S - A | A
# A -> a | b

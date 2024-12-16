# Заготовка для вычисления FIRST/FOLLOW
from collections import defaultdict

class LL1Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = defaultdict(set)
        self.follow = defaultdict(set)

    def compute_first(self):
        # Реализация вычисления FIRST
        for non_terminal in self.grammar:
            self.first[non_terminal] = self._compute_first(non_terminal)

    def _compute_first(self, symbol):
        if symbol not in self.grammar:  # Терминал
            return {symbol}
        first_set = set()
        for production in self.grammar[symbol]:
            for s in production:
                first_set.update(self._compute_first(s))
                if 'ε' not in self._compute_first(s):  # Если нет epsilons
                    break
        return first_set

    def compute_follow(self):
        # Реализация FOLLOW
        self.follow['S'].add('$')  # Добавляем $ к стартовому символу
        # Повторяем до сходимости
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.grammar.items():
                for production in productions:
                    follow_temp = self.follow[non_terminal]
                    for symbol in reversed(production):
                        if symbol in self.grammar:  # Если нетерминал
                            if follow_temp - self.follow[symbol]:
                                self.follow[symbol].update(follow_temp)
                                changed = True
                            if 'ε' in self.first[symbol]:
                                follow_temp = follow_temp.union(self.first[symbol] - {'ε'})
                            else:
                                follow_temp = self.first[symbol]

    def build_parse_table(self):
        # Реализация таблицы предсказаний
        parse_table = defaultdict(dict)
        for non_terminal, productions in self.grammar.items():
            for production in productions:
                for terminal in self.first[production[0]]:
                    parse_table[non_terminal][terminal] = production
                if 'ε' in self.first[production[0]]:
                    for terminal in self.follow[non_terminal]:
                        parse_table[non_terminal][terminal] = production
        return parse_table

if __name__ == '__main__':
    # Пример использования
    grammar = {
        'S': [['A', 'S1']],
        'S1': [['+', 'A', 'S1'], ['ε']],
        'A': [['a'], ['b']]
    }
    parser = LL1Parser(grammar)
    parser.compute_first()
    parser.compute_follow()
    parse_table = parser.build_parse_table()

    print("FIRST:", dict(parser.first))
    print("FOLLOW:", dict(parser.follow))
    print("Таблица предсказаний:")
    for non_terminal, row in parse_table.items():
        print(non_terminal, row)
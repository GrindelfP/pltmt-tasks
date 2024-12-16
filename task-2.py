class EarleyParser:
    def __init__(self, grammar):
        self.grammar = grammar  # Словарь вида {'S': ['A + S', 'b'], 'A': ['S - A', 'a']}
        self.chart = []

    def parse(self, word):
        self.chart = [[] for _ in range(len(word) + 1)]
        self.chart[0].append(('S1', ['•', 'S'], 0))  # Добавляем начальное правило

        for i in range(len(word) + 1):
            self.scanner(word, i)
            self.predictor(i)
            self.completer(i)

        # Проверяем финальное состояние
        final_state = ('S1', ['S', '•'], 0)
        return final_state in self.chart[-1], self.chart

    def scanner(self, word, i):
        if i < len(word):
            for rule in self.chart[i]:
                if '•' in rule[1] and rule[1][-1] != '•':  # Проверяем текущий символ
                    next_symbol = rule[1][rule[1].index('•') + 1]
                    if next_symbol == word[i]:
                        self.chart[i + 1].append((rule[0], rule[1][:-1] + [next_symbol, '•'], rule[2]))

    def predictor(self, i):
        for rule in self.chart[i]:
            if '•' in rule[1] and rule[1][-1] != '•':  # Если есть символ после "•"
                next_symbol = rule[1][rule[1].index('•') + 1]
                if next_symbol in self.grammar:  # Если это нетерминал
                    for production in self.grammar[next_symbol]:
                        self.chart[i].append((next_symbol, ['•'] + production.split(), i))

    def completer(self, i):
        for rule in self.chart[i]:
            if rule[1][-1] == '•':  # Если точка в конце
                for prev_rule in self.chart[rule[2]]:
                    if '•' in prev_rule[1] and prev_rule[1][-1] != '•':
                        next_symbol = prev_rule[1][prev_rule[1].index('•') + 1]
                        if next_symbol == rule[0]:
                            self.chart[i].append((prev_rule[0], prev_rule[1][:-1] + [next_symbol, '•'], prev_rule[2]))


if __name__ == "__main__":
    # Пример использования
    grammar = {
        'S': ['A + S', 'b'],
        'A': ['S - A', 'a']
    }
    parser = EarleyParser(grammar)
    word = input("Введите слово: ").strip()
    result, chart = parser.parse(word)
    print("Результат:", result)
    for i, state in enumerate(chart):
        print(f"Состояние {i}: {state}")
import re
from collections import defaultdict

class CYKParser:
    def __init__(self, grammar):
        """
        Инициализация парсера. Грамматика должна быть в НФХ.
        Формат грамматики: {'A': [['B', 'C'], ['a']]}
        """
        self.grammar = grammar
        self.cnf = self._prepare_cnf()

    def _prepare_cnf(self):
        """
        Подготовка грамматики в виде словаря для быстрого поиска.
        """
        cnf = defaultdict(list)
        for non_terminal, rules in self.grammar.items():
            for rule in rules:
                cnf[tuple(rule)].append(non_terminal)
        return cnf

    def parse(self, word):
        """
        Применение алгоритма CYK к заданному слову.
        """
        n = len(word)
        table = [[set() for _ in range(n)] for _ in range(n)]

        # Заполняем первую строку таблицы
        for j, symbol in enumerate(word):
            for rule in self.cnf.get((symbol,), []):
                table[0][j].add(rule)

        # Заполняем оставшуюся таблицу
        for length in range(2, n + 1):  # Длина подпоследовательности
            for start in range(n - length + 1):  # Начало подпоследовательности
                for split in range(1, length):  # Позиция разделения
                    left = table[split - 1][start]
                    right = table[length - split - 1][start + split]
                    for A in left:
                        for B in right:
                            for rule in self.cnf.get((A, B), []):
                                table[length - 1][start].add(rule)

        # Проверяем, выводится ли стартовый символ в верхнем правом углу таблицы
        start_symbol = 'S'
        return start_symbol in table[-1][0], table

def tokenize_input(input_str):
    """
    Разбивает входную строку на токены: числа, символы и операторы.
    """
    return re.findall(r'[a-zA-Z]+|[\+\-]', input_str)

# Пример использования
if __name__ == "__main__":
    # Грамматика в НФХ
    grammar = {
        'S': [['S', 'S1'], ['S', 'S2'], ['A']],
        'S1': [['O1', 'A']],
        'S2': [['O2', 'A']],
        'O1': [['+']],
        'O2': [['-']],
        'A': [['a'], ['b']]
    }

    parser = CYKParser(grammar)

    # Чтение входного слова и токенизация
    input_word = input("Введите слово: ").strip()
    tokens = tokenize_input(input_word)

    result, table = parser.parse(tokens)
    print("Результат:", result)

    # Вывод таблицы T[i][j]
    print("\nТаблица T[i][j]:")
    n = len(tokens)
    for i in range(n):
        for j in range(n - i):
            #if table[i][j] != set():
            print(f"T[{i+1},{j+1}]: {table[i][j]}")
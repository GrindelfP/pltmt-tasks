import re


def process_code(string: str) -> tuple[str, set]:

    without_comments: str = re.sub(r'/\*.*?\*/', '', string, flags=re.DOTALL)

    without_extra_spaces: str = re.sub(r'\s+', ' ', without_comments).strip()

    lexemes: set = set(re.findall(r'[a-zA-Zа-яА-ЯёЁ0-9]+|[^\s\w]', without_extra_spaces))

    return without_extra_spaces, lexemes


if __name__ == "__main__":
    input_str = input("Input you code: ")
    cleaned_code, lexemes_set = process_code(input_str)

    print("processed code:", cleaned_code)
    print("Lexemes:")
    for lexeme in lexemes_set:
        print(lexeme)
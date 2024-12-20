import re


def process_code(string: str) -> tuple[str, str, set]:

    without_comments: str = re.sub(r'/\*.*?\*/', '', string, flags=re.DOTALL)
    without_extra_spaces: str = re.sub(r'\s+', ' ', without_comments).strip()
    without_spaces_in_numbers: str = re.sub(r'(?<=\d)\s+(?=\d)', '', without_extra_spaces)
    cleaned_code: str = re.sub(r'\(\s+', '(', without_spaces_in_numbers)
    cleaned_code = re.sub(r'\s+\)', ')', cleaned_code)
    cleaned_code = re.sub(r'\s+;', ';', cleaned_code)

    lexemes: set = set(re.findall(r'[a-zA-Zа-яА-ЯёЁ0-9]+|[^\s\w]', cleaned_code))

    return without_comments, cleaned_code, lexemes


if __name__ == "__main__":
    input_str = input("Input you code: ")
    no_comments_code, correct_code, lexemes_set = process_code(input_str)

    print("Processed code without comments:", no_comments_code)
    print("Processed code without spaces:", correct_code)
    print("Lexemes:")
    for lexeme in lexemes_set:
        print(lexeme)

    input("Press ENTER key to exit...")

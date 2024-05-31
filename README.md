# bench_codes
Bench Mark some codes
with one is faster?

## codes
def count_letters_junior(text: str) -> int:
    count = 0
    for letter in text:
        if letter.isalpha():
            count += 1
    return count


def count_letters_intermediate(text: str) -> int:
    return sum(1 for letter in text if letter.isalpha())


def count_letters_confirmed(text: str) -> int:
    return sum(letter.isalpha() for letter in text)


def count_letters_senior(text: str) -> int:
    return sum(map(str.isalpha, text))


def count_letters_senior_petr_ocelik(text: str) -> int:
    return sum(map(string.ascii_letters.__contains__, text))


def count_letters_staff(text: str) -> int:
    return sum("A" <= letter <= "Z" or "a" <= letter <= "z" for letter in text)


def count_letters_expert(text: str) -> int:
    return sum(letter in string.ascii_letters for letter in text)


def count_letters_counter_v1(text: str) -> int:
    return len([True for letter in text if letter.isalpha()])


def count_letters_sum_anthony(text: str) -> int:
    return sum(97 <= ord(i.lower()) <= 122 for i in text)


def count_letters_sum_count(text: str) -> int:
    return sum(text.count(char) for char in string.ascii_letters)


alpha_chars = string.ascii_letters
table_alpha = str.maketrans('', '', alpha_chars)


def count_letters_translate_alpha(text: str) -> int:
    return len(text) - len(text.translate(table_alpha))


table_non_alpha = str.maketrans('', '', ''.join(set(string.printable) - set(alpha_chars)))
print(table_non_alpha)


def count_letters_translate_non_alpha(text: str) -> int:
    return len(text.translate(table_non_alpha))


compiled_pattern = regex.compile(r'[a-zA-Z]', regex.MULTILINE)
compiled_pattern_v2 = regex.compile(r'[a-zA-Z]+', regex.MULTILINE)
compiled_pattern_v3 = regex.compile(r'[^a-zA-Z]+', regex.MULTILINE)


def count_letters_regex_findall(text: str) -> int:
    return len(compiled_pattern.findall(text))


def count_letters_regex_split(text: str) -> int:
    return sum(len(x) for x in compiled_pattern_v3.split(text))


def count_letters_regex_sub(text: str) -> int:
    return len(text) - len(compiled_pattern.sub('', text))


def count_letters_regex_sub_v2(text: str) -> int:
    return len(text) - len(compiled_pattern_v2.sub('', text))


def count_letters_regex_sub_v3(text: str) -> int:
    return len(compiled_pattern_v3.sub('', text))


def count_letters_regex_iter(text: str) -> int:
    return sum(True for x in compiled_pattern.finditer(text))


def count_letters_regex_iter_v2(text: str) -> int:
    return sum(i.end() - i.start() for i in compiled_pattern_v2.finditer(text))

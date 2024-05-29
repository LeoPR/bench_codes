import string
#from memory_profiler import profile
import timeit
import random
import statistics
from collections import defaultdict, Counter
import regex
#####################
text_size: int = 100000
alpha_ratios = [0.1, 0.33, 0.66, 1] # 0 - no alpha, 1 - all alpha
alpha_threshold = True # vary size threshold over alpha_ratios
run_tests = 100


##########
# this code runs in ASCII text

#@profile
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

compiled_pattern = regex.compile(r'[a-zA-Z]')
def count_letters_regex(text: str) -> int:
    return len(compiled_pattern.findall(text))

def count_letters_dummy(text: str) -> int:
    return True

# Functions to test
functions =[#count_letters_dummy, # only to very if result exists
            count_letters_translate_non_alpha, # fastest
            count_letters_translate_alpha, # second fast
            count_letters_senior,
            count_letters_sum_count,
            count_letters_counter_v1,
            count_letters_junior,
            count_letters_intermediate,
            count_letters_confirmed,
            #count_letters_regex, # unstable, very unbalanced, with no alpha, its faster than any other, but with all alpha its worst 
            #count_letters_expert, #ultra slow
            #count_letters_staff, # very slow
            ]


def benchmark(func, text, runs=100):
    times = []
    in_res = 0
    total_time = 0
    for _ in range(runs):
        start_time = timeit.default_timer()
        in_res = func(text)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        times.append(execution_time)
        total_time += execution_time
    best_time = min(times)
    worst_time = max(times)
    avg_time = statistics.mean(times)
    return best_time, avg_time, worst_time, total_time, in_res


def generate_text(length: int, in_alpha_ratio: float, seed: int, alpha_threshold: bool) -> str:
    random.seed(seed)
    # generate a printable and non-printable characters
    alpha = string.ascii_letters
    non_alpha = ''.join(set(string.printable) - set(alpha))
    in_text = []
    alpha_length = int(length * in_alpha_ratio)
    if alpha_threshold:
        alpha_length *= 1 - random.uniform(0.01, 0.03)
    alpha_length = int(min(max(alpha_length,1),length))
    non_alpha_length = length - alpha_length
    for _ in range(alpha_length):
        in_text.append(random.choice(alpha))
    for _ in range(non_alpha_length):
        in_text.append(random.choice(non_alpha))
    random.shuffle(in_text)
    return ''.join(in_text)


best_times = defaultdict(list)
avg_times = defaultdict(list)
worst_times = defaultdict(list)
total_times = defaultdict(list)

best_funcs = []
avg_funcs = []
worst_funcs = []
total_funcs = []

for alpha_ratio in alpha_ratios:
    print(f"\nAlpha ratio: {alpha_ratio}")
    text = generate_text(text_size, alpha_ratio, 0, alpha_threshold)
    print(f'text size: {len(text)} ...')  # show text size
    print(f'text sample: {text[:100]} ...')  # show sample
    results = []
    for func in functions:
        best, avg, worst, total, res = benchmark(func, text, run_tests)
        print(
            f"{func.__name__}: Best: {best} seconds, Average: {avg} seconds, Worst: {worst} seconds, Total: {total} seconds, Result: {res}")
        results.append((func.__name__, best, avg, worst, total, res))
        best_times[func.__name__].append(best)
        avg_times[func.__name__].append(avg)
        worst_times[func.__name__].append(worst)
        total_times[func.__name__].append(total)

    results.sort(key=lambda x: x[1])  # Sort by best time
    print(f"Best: {results[0][0]}, Second Best: {results[1][0]}")
    best_funcs.append(results[0][0])
    results.sort(key=lambda x: x[2])  # Sort by average time
    print(f"Best Average: {results[0][0]}, Second Best Average: {results[1][0]}")
    avg_funcs.append(results[0][0])
    results.sort(key=lambda x: x[3], reverse=True)
    print(f"Worst: {results[0][0]}, Second Worst: {results[1][0]}")
    worst_funcs.append(results[0][0])
    results.sort(key=lambda x: x[4], reverse=False)
    total_funcs.append(results[0][0])

best_func_counter = Counter(best_funcs)
best_func_overall = best_func_counter.most_common(1)[0][0]
avg_funcs_counter = Counter(avg_funcs)
avg_funcs_overall = avg_funcs_counter.most_common(1)[0][0]
worst_funcs_counter = Counter(worst_funcs)
worst_funcs_overall = worst_funcs_counter.most_common(1)[0][0]
total_funcs_counter = Counter(total_funcs)
total_funcs_overall = total_funcs_counter.most_common(1)[0][0]

print("\nBest function over all alpha ratios:")
print(best_func_overall)
print("\nAVG function over all alpha ratios:")
print(avg_funcs_overall)
print("\nWorst function over all alpha ratios:")
print(worst_funcs_overall)
print("\nTotal time faster function over all alpha ratios:")
print(total_funcs_overall)

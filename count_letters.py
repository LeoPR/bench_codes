import string
#from memory_profiler import profile
import timeit
import random
import statistics
from collections import defaultdict, Counter

#####################
text_size:int = 100000
alpha_ratios = [0, 0.3, 0.6, 1] # 0 - no alpha, 1 - all aplha
run_tests = 100
##########


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
    return sum(97 <= ord(i.lower()) <=122 for i in text)

def count_letters_sum_count(text: str) -> int:
    return sum(text.count(char) for char in string.ascii_letters)

table_alpha = str.maketrans('','',string.ascii_letters)
def count_letters_translate_alpha(text: str) -> int:
    return len(text) - len(text.translate(table_alpha))

table_non_alpha = str.maketrans('','',string.punctuation + string.digits + string.whitespace)

def count_letters_translate_nonaplha(text: str) -> int:
    return len(text.translate(table_non_alpha))

functions = [count_letters_junior, count_letters_intermediate, count_letters_confirmed, count_letters_senior, count_letters_staff,
             count_letters_expert, count_letters_counter_v1, count_letters_sum_count,
             count_letters_translate_alpha, count_letters_translate_nonaplha]


def benchmark(func, text, runs=100):
    times = []
    res = 0
    total_time = 0
    for _ in range(runs):
        start_time = timeit.default_timer()
        res = func(text)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        times.append(execution_time)
        total_time += execution_time
    best_time = min(times)
    worst_time = max(times)
    avg_time = statistics.mean(times)
    return best_time, avg_time, worst_time, total_time, res

def generate_text(length: int, alpha_ratio: float, seed: int) -> str:
    random.seed(seed)
    alpha = string.ascii_letters
    non_alpha = ''.join(set(string.printable) - set(alpha))
    text = []
    alpha_length = int(length * alpha_ratio)
    non_alpha_length = length - alpha_length
    for _ in range(alpha_length):
        text.append(random.choice(alpha))
    for _ in range(non_alpha_length):
        text.append(random.choice(non_alpha))
    random.shuffle(text)
    return ''.join(text)



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
    text = generate_text(text_size, alpha_ratio, 0)
    print(text[:100]) # show sample
    results = []
    for func in functions:
        best, avg, worst, total, res = benchmark(func, text, run_tests)
        print(f"{func.__name__}: Best: {best} seconds, Average: {avg} seconds, Worst: {worst} seconds, Total: {total} seconds, Result: {res}")
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

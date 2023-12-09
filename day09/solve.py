def complete_sequence(numbers: list[int]) -> int:
    if not any(numbers):
        return 0
    diffs=list(map(lambda a,b:a-b, numbers[1:], numbers[:-1]))
    return numbers[-1]+complete_sequence(diffs)

def extrapolate(line: str) -> int:
    numbers=[int(el) for el in line.split(' ') if el]
    return complete_sequence(numbers)

def extrapolate_backwards(line: str) -> int:
    numbers=[int(el) for el in line.split(' ') if el]
    numbers.reverse()
    return complete_sequence(numbers)

def solve_1(data: list[str]) -> int:
    return sum(perform(data, extrapolate))

def solve_2(data: list[str]) -> int:
    return sum(perform(data, extrapolate_backwards))

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    with Pool() as pool:
        results = pool.map(func, data)
    return results


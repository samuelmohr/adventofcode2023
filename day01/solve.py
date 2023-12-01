import re
regex_start = re.compile(r"^[a-z]*(\d).*")
regex_end = re.compile(".*(\d)[a-z]*$")


def calibrate(input: str) -> int:
    match=regex_start.match(input)
    if match is None:
        return 0
    digit1=int(match.group(1))
    match=regex_end.match(input)
    if match is None:
        return 0
    digit2=int(match.group(1))
    return digit1*10+digit2

def prepare_words(input: str) -> str:
    input=input.replace("zero","zero0zero")
    input=input.replace("one","one1one")
    input=input.replace("two","two2two")
    input=input.replace("three","three3three")
    input=input.replace("four","four4four")
    input=input.replace("five","five5five")
    input=input.replace("six","six6six")
    input=input.replace("seven","seven7seven")
    input=input.replace("eight","eight8eight")
    input=input.replace("nine","nine9nine")
    return calibrate(input)
    
def solve_1(data: list[str]) -> int:
    return perform(data, calibrate)

def solve_2(data: list[str]) -> int:
    return perform(data, prepare_words)

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    pool= Pool()
    results=[pool.apply_async(func,[line]) for line in data]
    pool.close()
    pool.join()
    from functools import reduce
    return reduce(lambda value,result : value + result.get(), results, 0)

import re

def winning_numbers(line: str) -> int:
    game=line.split(':')[1]
    draw_string=game.split('|')[0]
    my_string=game.split('|')[1]
    draw_numbers=set([int(number) for number in draw_string.split(' ') if number])
    my_numbers=set([int(number) for number in my_string.split(' ') if number])
    good=len(draw_numbers.intersection(my_numbers))
    return good

def winning_score(line: str) -> int:
    good = winning_numbers(line)
    return int((good>0) * 2**(good-1))

def solve_1(data: list[str]) -> int:
    return sum(perform(data, winning_score))

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    with Pool() as pool:
        results = pool.map(func, data)
    return results

def play_card(card_list: list[list[int]]) -> int:
    if len(card_list)==0:
        return 0
    card=card_list.pop(0)
    count=card[1]
    score=card[0]
    for i in range(score):
        card_list[i][1]+=count
    ret=count+play_card(card_list)
    return ret

def solve_2(data: list[str]) -> int:
    numbers=[[number,1] for number in perform(data, winning_numbers)]
    return play_card(numbers)


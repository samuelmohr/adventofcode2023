import re
regex_number = re.compile(r"\d+")

engine: list[str] = []
vert_length : int = 0
horiz_length: int = 0

def set_engine(data: list[str]):
    global engine, vert_length, horiz_length
    engine = data
    vert_length = len(engine)
    horiz_length = len(engine[0])
    print("       _ Engine is set for thread pool")

def is_symbol(pos: tuple[int,int]) -> bool:
    char = engine[pos[0]][pos[1]]
    return not char.isdigit() and char != '.'

def is_gear_symbol(pos: tuple[int,int]) -> bool:
    return engine[pos[0]][pos[1]] == '*'

def find_neighbour_cells(line: int, start: int, end: int) -> list[tuple[int,int]]:
    pos = []
    # top with overlap
    pos.extend([(line-1,i) for i in range(start-1,end+1) if line > 0 and i>=0 and i<horiz_length])
    # bottom with overlap
    pos.extend([(line+1,i) for i in range(start-1,end+1) if line < (vert_length-1) and i>=0 and i<horiz_length])
    # sides
    if start > 0:
        pos.append((line,start-1))
    if end < horiz_length:
        pos.append((line,end))
    return pos

def is_activated(line: int, start: int, end: int) -> bool:
    pos = find_neighbour_cells(line, start, end)
    return any(map(is_symbol, pos))

def find_numbers(line_index : int) -> int:
    matches = regex_number.finditer(engine[line_index])
    return sum([int(match.group(0)) for match in matches if is_activated(line_index, match.start(), match.end())])

def check_gear_connection_for_number(line: int, start: int, end: int) -> list[tuple[tuple[int,int],int]]: # ((line_pos, col_pos), number) of every gear_number
    pos = find_neighbour_cells(line, start, end)
    active = map(is_gear_symbol, pos)
    gear_list = [pos[i] for (i,act) in enumerate(active) if act]
    return gear_list

def find_numbers_at_gears(line_index : int) -> list[tuple[tuple[int,int],int]]: # ((line_pos, col_pos), number) of every gear_number
    matches = regex_number.finditer(engine[line_index])
    gear_list = [(pos,int(match.group(0))) for match in matches for pos in check_gear_connection_for_number(line_index, match.start(), match.end()) ]
    return gear_list
    

def solve_1(data: list[str]) -> int:
    return perform(data, find_numbers)

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    with Pool(initializer=set_engine, initargs=[data]) as pool:
        results = pool.map(func, range(len(data)))
    return sum(results)

def get_score(gear: tuple[int,int], results: list[tuple[tuple[int,int],int]]) -> int:
    from functools import reduce
    from operator import mul
    numbers = [item[1] for item in results if item[0]==gear]
    return (len(numbers)==2) * reduce(mul,numbers)
    
def solve_2(data: list[str]) -> int:
    from multiprocessing import Pool
    with Pool(initializer=set_engine, initargs=[data]) as pool:
        results = pool.map(find_numbers_at_gears, range(len(data)))
    
    flat_list = [item for sublist in results for item in sublist]
    gears = set([result[0] for result in flat_list])
    from functools import reduce
    return reduce(lambda value,gear : value + get_score(gear,flat_list), gears, 0)


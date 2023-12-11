
map: list[list[bool]] = None
empty_rows: list[int] = []
empty_cols: list[int] = []
expansion_factor = 1

def set_map(data: list[list[bool]], expansion: int = 2):
    global map, empty_rows, empty_cols, expansion_factor
    map = data
    expansion_factor = expansion
    empty_rows = [i for i in range(len(data)) if not any(data[i])]
    empty_cols = [i for i in range(len(data[0])) if not any([row[i] for row in data])]
    print("       _ Map is set for thread pool")


def vertical_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    x1 = min(pos1[0], pos2[0])
    x2 = max(pos1[0], pos2[0])
    return x2-x1 + len([i for i in range(x1, x2) if i in empty_rows]) * (expansion_factor-1)

def horizontal_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    y1 = min(pos1[1], pos2[1])
    y2 = max(pos1[1], pos2[1])
    return y2-y1 + len([i for i in range(y1, y2) if i in empty_cols]) * (expansion_factor-1)

def get_distance(pair: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return vertical_distance(pair[0], pair[1]) + horizontal_distance(pair[0], pair[1])


from itertools import combinations

def solve_1(data: list[str]) -> int:
    map=[[data[i][j]=='#' for j in range(len(data[0]))] for i in range(len(data))]
    galaxies: list[tuple[int,int]] = [(i,j) for i in range(len(map)) for j in range(len(map[0])) if map[i][j]]
    pairs: list[tuple[tuple[int,int],tuple[int,int]]] = list(combinations(galaxies,2))
    return perform(map, pairs, get_distance)

def solve_2(data: list[str]) -> int:
    map=[[data[i][j]=='#' for j in range(len(data[0]))] for i in range(len(data))]
    galaxies: list[tuple[int,int]] = [(i,j) for i in range(len(map)) for j in range(len(map[0])) if map[i][j]]
    pairs: list[tuple[tuple[int,int],tuple[int,int]]] = list(combinations(galaxies,2))
    return perform(map, pairs, get_distance, 1000000)

def perform(array: list[list[bool]], pairs: list[tuple[tuple[int,int],tuple[int,int]]], func: callable, expansion_factor: int = 2) -> int:
    from multiprocessing import Pool
    with Pool(initializer=set_map, initargs=[array, expansion_factor]) as pool:
        results = pool.map(func, pairs)
    return sum(results)



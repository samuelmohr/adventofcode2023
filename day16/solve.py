
map: list[str] = None

def set_map(data: list[str]):
    global map
    map = data
    print("       _ Map is set for thread pool")

slash_map = {
    'r': 'u',
    'l': 'd',
    'u': 'r',
    'd': 'l'
}
backslash_map = {
    'r': 'd',
    'l': 'u',
    'u': 'l',
    'd': 'r'
}

def light_step(pos: tuple[int,int,str]) -> list[tuple[int,int,str]]:
    new_pos = None
    match pos[2]:
        case 'r':
            if pos[1] == len(map[0])-1:
                return []
            else:
                new_pos = (pos[0], pos[1]+1)
        case 'l':
            if pos[1] == 0:
                return []
            else:
                new_pos = (pos[0], pos[1]-1)
        case 'u':
            if pos[0] == 0:
                return []
            else:
                new_pos = (pos[0]-1, pos[1])
        case 'd':
            if pos[0] == len(map)-1:
                return []
            else:
                new_pos = (pos[0]+1, pos[1])

    if map[new_pos[0]][new_pos[1]] == '.':
        return [(new_pos[0], new_pos[1], pos[2])]
    if map[new_pos[0]][new_pos[1]] == '-' and pos[2] in ['l', 'r']:
        return [(new_pos[0], new_pos[1], pos[2])]
    if map[new_pos[0]][new_pos[1]] == '|' and pos[2] in ['u', 'd']:
        return [(new_pos[0], new_pos[1], pos[2])]
    if map[new_pos[0]][new_pos[1]] == '/':
        return [(new_pos[0], new_pos[1], slash_map[pos[2]])]
    if map[new_pos[0]][new_pos[1]] == '\\':
        return [(new_pos[0], new_pos[1], backslash_map[pos[2]])]
    if map[new_pos[0]][new_pos[1]] == '-':
        return [(new_pos[0], new_pos[1], 'r'), (new_pos[0], new_pos[1], 'l')]
    if map[new_pos[0]][new_pos[1]] == '|':
        return [(new_pos[0], new_pos[1], 'u'), (new_pos[0], new_pos[1], 'd')]
    raise ValueError(f"Unknown map character {map[new_pos[0]][new_pos[1]]}")          

def solve_1(data: list[str]) -> int:
    return analyse_rays(data)

def analyse_rays(data: list[str], start : tuple[int,int,str] = (0,-1,'r')) -> int:
    return len(perform(data, start, light_step))

def perform(data: list[str], start: tuple[int,int,str], func: object) -> int:
    from concurrent.futures import ThreadPoolExecutor
    import shutil
    visits = set()
    with ThreadPoolExecutor(initializer=set_map, initargs=[data]) as executor:
        futures = []
        futures.append(executor.submit(func, start))
        while futures:
            #print("Queue size: ", '#' * len(futures), ' ' * (shutil.get_terminal_size().columns - len(futures) - 14), end='\r')
            future = futures.pop()
            if future.result():
                for pos in future.result():
                    if pos not in visits:
                        visits.add(pos)
                        futures.append(executor.submit(func, pos))
    return set([visit[:2] for visit in visits])

def solve_2(data: list[str]) -> int:
    starts = []
    for i in range(len(data)):
        starts.extend([(i,-1,'r'), (i,len(data[0]),'l')])
    for i in range(len(data[0])):
        starts.extend([(-1,i,'d'), (len(data),i,'u')])

    from concurrent.futures import ProcessPoolExecutor
    import tqdm
    with ProcessPoolExecutor() as executor:
        results = executor.map(analyse_rays, [data for _ in range(len(starts))], starts)
    return max(results)
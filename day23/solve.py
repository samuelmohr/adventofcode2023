incidence_map : dict[tuple[int,int],list[tuple[int,int]]] = dict()
xlen = 0
ylen = 0

def set_map(data: list[str], use_slope: bool = True):
    global xlen, ylen
    xlen = len(data[0])
    ylen = len(data)

    incidence = dict()
    for y in range(ylen):
        for x in range(xlen):
            if data[y][x] == '#':
                continue
            incidence[(x,y)] = []
            if use_slope:
                if data[y][x] in ['<', '>', '^', 'v']:
                    if data[y][x] == '<':
                        incidence[(x,y)].append((x-1,y))
                    elif data[y][x] == '>':
                        incidence[(x,y)].append((x+1,y))
                    elif data[y][x] == '^':
                        incidence[(x,y)].append((x,y-1))
                    elif data[y][x] == 'v':
                        incidence[(x,y)].append((x,y+1))
                    continue
            if x > 0 and data[y][x-1] != '#':
                incidence[(x,y)].append((x-1,y))
            if x < xlen-1 and data[y][x+1] != '#':
                incidence[(x,y)].append((x+1,y))
            if y > 0 and data[y-1][x] != '#':
                incidence[(x,y)].append((x,y-1))
            if y < ylen-1 and data[y+1][x] != '#':
                incidence[(x,y)].append((x,y+1))
    
    global incidence_map
    for key, value in incidence.items():
        if len(value) <= 2 and key[1] != 0 and key[1] != ylen-1:
            continue
        incidence_map[key] = []
        for v in value:
            next = v
            previous = key
            steps = 1
            while len(incidence[next]) <= 2 and next[1] != 0 and next[1] != ylen-1:
                tmp = set(incidence[next]).difference({previous})
                if len(tmp) == 0:
                    steps = -1
                    break
                previous = next
                next = tmp.pop()
                steps += 1
            if steps > 0:
                incidence_map[key].append((next, steps))

def complete_path(pos: tuple[int,int], finish: tuple[int,int], path: list[tuple[int,int]]) -> int:
    if pos == finish:
        return 0
    if len(incidence_map[pos]) == 0:
        raise ValueError("No path found")
    length = 0
    for next in incidence_map[pos]:
        if next[0] in path:
            continue
        path2 = path.copy()
        path2.append(pos)
        try:
            length = max(length, complete_path(next[0], finish, path2) + next[1])
        except ValueError:
            continue
    if length == 0:
        raise ValueError("No path found")
    return length

def find_longest_path() -> int:
    start = [item for item in incidence_map.keys() if item[1] == 0][0]
    end = [item for item in incidence_map.keys() if item[1] == ylen-1][0]
    return complete_path(start, end, [])




def solve_1(data: list[str]) -> int:
    set_map(data)
    return find_longest_path()

def solve_2(data: list[str]) -> int:
    set_map(data, False)
    return find_longest_path()
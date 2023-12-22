
row_map: dict[list[tuple[int,str]]] = dict()

def default_decoder(line: str) -> tuple[int,str]:
    parts = line.split(' ')
    return (int(parts[1]), parts[0])

def set_map(data: list[str], decoder: object = default_decoder):
    global row_map
    xpos = 0
    ypos = 0
    for row in data:
        distance, direction = decoder(row)
        match direction:
            case 'U':
                for i in range(0,distance+1):
                    x = xpos+i
                    if not x in row_map:
                        row_map[x] = [(ypos,'U')]
                    else:
                        row_map[x].append((ypos,'U'))
                xpos += distance
            case 'D':
                for i in range(0,distance+1):
                    x = xpos-i
                    if not x in row_map:
                        row_map[x] = [(ypos,'D')]
                    else:
                        row_map[x].append((ypos,'D'))
                xpos -= distance
            case 'R':
                if not xpos in row_map:
                    row_map[xpos] = [(ypos+0.5,'R')]
                else:
                    row_map[xpos].append((ypos+0.5,'R'))
                ypos += distance
            case 'L':
                if not xpos in row_map:
                    row_map[xpos] = [(ypos-0.5,'L')]
                else:
                    row_map[xpos].append((ypos-0.5,'L'))
                ypos -= distance
    print("       _ Map is set for thread pool")

def analyse_row(row: list[int]) -> int:
    row.sort()
    score = 0
    out = True
    last_el = None
    horizontal = False
    for el in row:
        if el[1] in ['R', 'L']:
            horizontal = True
            continue
        if last_el == None:
            score += 1
            out = False
        else:
            if not out or horizontal:
                score += el[0] - last_el[0]
            else:
                score += 1
            if el[1] != last_el[1]:
                out = not out
        last_el = el
        horizontal = False
    return score

def analyse_lagoon() -> int:
    from functools import reduce
    return sum([analyse_row(row) for row in row_map.values()])



def solve_1(data: list[str]) -> int:
    set_map(data)
    return analyse_lagoon()

directions_list = ['R', 'D', 'L', 'U']
def hex_decoder(line: str) -> tuple[int,str]:
    parts = line.split(' ')
    len_part = parts[2][2:7]
    dir_part = int(parts[2][7])
    return (int(len_part,16), directions_list[dir_part])

def solve_2(data: list[str]) -> int:
    set_map(data, hex_decoder)
    return analyse_lagoon()

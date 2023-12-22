
vmap: list[tuple[int,int,int,str]] = []
hmap: list[tuple[int,int,int,str,str,str]] = []
horizontal_knots : list[int] = []

def default_decoder(line: str) -> tuple[int,str]:
    parts = line.split(' ')
    return (int(parts[1]), parts[0])

def set_map(data: list[str], decoder: object = default_decoder):
    global vmap, hmap, horizontal_knots
    vmap = []
    hmap = []
    horizontal_knots = []
    xpos = 0
    ypos = 0
    last = ['X']
    for row in data:
        distance, direction = decoder(row)
        match direction:
            case 'U':
                hmap.append((xpos, last[1], last[2], last[0], 'U', last[3]))
                vmap.append((xpos+1,xpos+distance-1,ypos,'U'))
                xpos += distance
                last = ['U']
            case 'D':
                hmap.append((xpos, last[1], last[2], last[0], 'D', last[3]))
                vmap.append((xpos-distance+1,xpos-1,ypos,'D'))
                xpos -= distance
                last = ['D']
            case 'R':
                last.extend([ypos,ypos+distance,'R'])
                horizontal_knots.append(xpos)
                ypos += distance
            case 'L':
                last.extend([ypos-distance,ypos,'L'])
                horizontal_knots.append(xpos)
                ypos -= distance
    hmap[0] = (hmap[0][0], hmap[0][1], hmap[0][2], last[0], hmap[0][4], hmap[0][5])
    print("       _ Map is set for thread pool")

def analyse_row(row: int) -> int:
    score = 0
    hinfo = [el[1:] for el in hmap if el[0]==row]
    hinfo.sort()
    vinfo = [(el[2],el[3]) for el in vmap if el[0]<=row and el[1]>=row]
    vinfo.sort()
    out = 0
    last_el = None
    while len(hinfo)>0 or len(vinfo)>0:
        if len(hinfo)==0 or (len(vinfo)>0 and vinfo[0][0]<=hinfo[0][0]):
            el = vinfo.pop(0)
            if last_el == None or el[0] > last_el:
                if out != 0:
                    score += el[0] - last_el
                else:
                    score += 1
                last_el = el[0]
            if el[1] == 'D':
                out -= 1
            else:
                out += 1
        else:
            el = hinfo.pop(0)
            if last_el == None or el[0] > last_el:
                if out != 0:
                    score += el[0] - last_el
                else:
                    score += 1
                last_el = el[0]
            if el[1] > last_el:
                score += el[1] - last_el
                last_el = el[1]
            if el[2] == 'D' and el[3] == 'D':
                out -= 1
            elif el[2] == 'U' and el[3] == 'U':
                out += 1
    assert(out==0)
    return score

def analyse_lagoon() -> int:
    score = 0
    row_min = min(horizontal_knots)
    row_max = max(horizontal_knots)
    row = row_min
    while row <= row_max:
        to_add = analyse_row(row)
        if row in horizontal_knots:
            row += 1
            score += to_add
        else:
            row_old = row
            row = min([i for i in horizontal_knots if i>row])
            score += to_add*(row-row_old)

    return score

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

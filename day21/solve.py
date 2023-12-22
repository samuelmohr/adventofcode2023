
gardens: list[list[bool]] = None
active: list[list[bool]] = None
startpos: tuple[int,int] = None

def set_map(data: list[str]):
    global gardens, active, startpos
    gardens = [[(data[i][j]!='#') for j in range(len(data[0]))] for i in range(len(data))]
    active = [[(data[i][j]=='S') for j in range(len(data[0]))] for i in range(len(data))]
    for i in range(len(gardens)):
        for j in range(len(gardens[0])):
            if active[i][j]:
                startpos = (i,j)
    print("       _ Map is set for thread pool")
    print(f"       _ Debug info: dimension {len(gardens)} x {len(gardens[0])} and start position {startpos}")

def set_start(start: tuple[int,int]):
    global active
    active = [[False for _ in range(len(gardens[0]))] for _ in range(len(gardens))]
    active[start[0]][start[1]] = True

def find_neighbours(parity: int):
    for i in range(len(gardens)):
        for j in range(len(gardens[0])):
            if (i+j)%2 != parity%2:
                continue
            if not active[i][j]:
                continue
            if i>0:
                if gardens[i-1][j]:
                    active[i-1][j] = True
            if i<len(gardens)-1:
                if gardens[i+1][j]:
                    active[i+1][j] = True
            if j>0:
                if gardens[i][j-1]:
                    active[i][j-1] = True
            if j<len(gardens[0])-1:
                if gardens[i][j+1]:
                    active[i][j+1] = True
            active[i][j] = False

def do_steps_and_count(start: tuple[int,int], steps_to_perform : int) -> int:
    if steps_to_perform<0:
        return 0
    set_start(start)
    for i in range(steps_to_perform):
        find_neighbours(i+start[0]+start[1])
    ret = sum([sum([1 for j in range(len(active[0])) if active[i][j]]) for i in range(len(active))])
    print(steps_to_perform, ret)
    return ret

def solve_1(data: list[str]) -> int:
    set_map(data)
    return do_steps_and_count(startpos, 64)

def solve_2(data: list[str]) -> int:
    set_map(data)

    xlen = len(gardens[0])
    ylen = len(gardens)
    assert(xlen==ylen)
    assert(startpos[0]*2+1==xlen)
    assert(startpos[1]*2+1==ylen)
    assert(all(gardens[startpos[0]]))
    assert(all([gardens[i][startpos[1]] for i in range(ylen)]))
    # this ensures that we start in the middle and can go straight through all tiles
    
    steps = 26501365
    intermediate = steps - (xlen+1)//2
    count = intermediate//xlen
    count -= 1
    
    diameter = count*2 + 1
    print(f"       _ Debug info: First {count*xlen} steps are assumed to fill full squares of diameter {diameter}. That means that {steps-count*xlen} steps remain for the three outer circles")
    
    inner=count_diamond(diameter,(startpos[0]+startpos[1]))
    print(f"       _ Debug info: inner area: {inner} possible positions in the garden")
    
    # outer but 2 cycle
    remaining_side_steps = steps - startpos[0] - count*xlen - 1
    remaining_diagonal_steps = remaining_side_steps - ylen//2 - 1 + xlen
    left = do_steps_and_count((xlen-1,startpos[1]), remaining_side_steps)
    lefttop = count * do_steps_and_count((xlen-1,ylen-1), remaining_diagonal_steps)
    top = do_steps_and_count((startpos[0],ylen-1), remaining_side_steps)
    righttop = count * do_steps_and_count((0, ylen-1), remaining_diagonal_steps)
    right = do_steps_and_count((0,startpos[1]), remaining_side_steps)
    rightbottom = count * do_steps_and_count((0,0), remaining_diagonal_steps)
    bottom = do_steps_and_count((startpos[0],0), remaining_side_steps)
    leftbottom = count * do_steps_and_count((xlen-1,0), remaining_diagonal_steps)
    medium = left+lefttop+top+righttop+right+rightbottom+bottom+leftbottom
    print(f"       _ Debug info: next circle area: {medium} possible positions in the garden")
    
    # outer but 1 cycle
    remaining_side_steps = remaining_side_steps - xlen
    remaining_diagonal_steps = remaining_diagonal_steps - xlen
    count += 1
    left = do_steps_and_count((xlen-1,startpos[1]), remaining_side_steps)
    lefttop = count * do_steps_and_count((xlen-1,ylen-1), remaining_diagonal_steps)
    top = do_steps_and_count((startpos[0],ylen-1), remaining_side_steps)
    righttop = count * do_steps_and_count((0, ylen-1), remaining_diagonal_steps)
    right = do_steps_and_count((0,startpos[1]), remaining_side_steps)
    rightbottom = count * do_steps_and_count((0,0), remaining_diagonal_steps)
    bottom = do_steps_and_count((startpos[0],0), remaining_side_steps)
    leftbottom = count * do_steps_and_count((xlen-1,0), remaining_diagonal_steps)
    outer = left+lefttop+top+righttop+right+rightbottom+bottom+leftbottom
    print(f"       _ Debug info: outer circle area: {outer} possible positions in the garden")

    # outer but 1 cycle
    remaining_side_steps = remaining_side_steps - xlen
    remaining_diagonal_steps = remaining_diagonal_steps - xlen
    count += 1
    left = do_steps_and_count((xlen-1,startpos[1]), remaining_side_steps)
    lefttop = count * do_steps_and_count((xlen-1,ylen-1), remaining_diagonal_steps)
    top = do_steps_and_count((startpos[0],ylen-1), remaining_side_steps)
    righttop = count * do_steps_and_count((0, ylen-1), remaining_diagonal_steps)
    right = do_steps_and_count((0,startpos[1]), remaining_side_steps)
    rightbottom = count * do_steps_and_count((0,0), remaining_diagonal_steps)
    bottom = do_steps_and_count((startpos[0],0), remaining_side_steps)
    leftbottom = count * do_steps_and_count((xlen-1,0), remaining_diagonal_steps)
    afield = left+lefttop+top+righttop+right+rightbottom+bottom+leftbottom
    print(f"       _ Debug info: the afield outskirts circle area: {afield} possible positions in the garden")

    return inner+medium+outer+afield

def count_diamond(diameter: int, parity: int) -> int:
    assert(diameter%2==1)
    x=diameter//2
    # sum(i=1..x) 4*i + centre
    tiles = x*(x+1)*4//2+1
    centre_type_tiles = x//2*(x//2+1)*8//2 + 1
    
    odd_elements = do_steps_and_count((0,1), len(gardens)*3)
    even_elements = do_steps_and_count((0,0), len(gardens)*3)
    
    if parity%2==1:
        return centre_type_tiles*odd_elements + (tiles-centre_type_tiles)*even_elements
    else:
        return centre_type_tiles*even_elements + (tiles-centre_type_tiles)*odd_elements


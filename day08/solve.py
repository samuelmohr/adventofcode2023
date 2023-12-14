import re
regex_direction=re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")

def parse_line(line: str) -> tuple[str,list[str]]:
    match=regex_direction.match(line)
    if match==None:
        raise runtime_error("Failed to parse line.")
    return (match.group(1),[match.group(2),match.group(3)])

def do_walk(pos: str, step: str, stepcounter: int, directions: dict[str,list[str]]) -> tuple[str,int]:
    if step=='L':
        return (directions[pos][0],stepcounter+1)
    elif step=='R':
        return (directions[pos][1],stepcounter+1)
    else:
        raise runtime_error("Unknown direction")

def do_walk_to_end(pos: str, step: str, stepcounter: int, directions: dict[str,list[str]]) -> tuple[str,int]:
    if pos=="ZZZ":
        return ("ZZZ",stepcounter)
    return do_walk(pos,step,stepcounter,directions)

def solve_1(data: list[str]) -> int:
    walk=data[0]
    directions=dict()
    for line in data[2:]:
        origin,connections=parse_line(line)
        directions[origin]=connections
    
    from functools import reduce
    position="AAA"
    steps=0
    while position!="ZZZ":
        position,steps=reduce(lambda state,step : do_walk_to_end(state[0],step,state[1], directions),list(walk),(position,steps))
    return steps

def solve_2(data: list[str]) -> int:
    walk=data[0]
    directions=dict()
    for line in data[2:]:
        origin,connections=parse_line(line)
        directions[origin]=connections
    
    from functools import reduce
    positions=[start for start in directions.keys() if start.endswith('A')]
    periods=[]

    for position in positions:
        print(f"    • Start from {position}:")
        visits=[]
        steps=0
        for _ in range(1050):
            result=reduce(lambda state,step : all_finishs(state[0][0],step,state[0][1],state[1],directions),list(walk),((position,steps),visits))
            position=result[0][0]
            steps=result[0][1]
            visits=result[1]
        # well, not nice but in this case the following assertion is true:
        assert(visits==[visits[0]*i for i in range(1,len(visits)+1)])
        print(f"      Periodicity: {visits[0]}")
        periods.append(visits[0])
        
    import math
    return reduce(math.lcm, periods, 1)

def all_finishs(pos: str, step: str, stepcounter: int, visits: list[int], directions: dict[str,list[str]]) -> tuple[tuple[str,int],list[int]]:
    if pos.endswith('Z'):
        visits.append(stepcounter)
    return (do_walk(pos, step, stepcounter, directions), visits)





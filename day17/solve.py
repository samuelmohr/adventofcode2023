
map: list[list[int]] = None
xlength: int = None
ylength: int = None

def set_map(data: list[str]):
    global map, xlength, ylength
    map = [[int(char) for char in row] for row in data]
    xlength = len(map[0])
    ylength = len(map)
    print("       _ Map is set for thread pool")

def do_step(pos: tuple[int,int], direction: str) -> tuple[int,int]:
    if pos==None:
        return None
    match direction:
        case 'r':
            if pos[1] < len(map[0])-1:
                return (pos[0], pos[1]+1)
        case 'l':
            if pos[1] > 0:
                return (pos[0], pos[1]-1)
        case 'u':   
            if pos[0] > 0:
                return (pos[0]-1, pos[1])
        case 'd':
            if pos[0] < len(map)-1:
                return (pos[0]+1, pos[1])
    return None

opposite_direction = {
    'r': 'l',
    'l': 'r',
    'u': 'd',
    'd': 'u'
}

def get_cost(pos: tuple[int,int]) -> int:
    if pos==None:
        return 0
    return map[pos[0]][pos[1]]

def all_direct_neighbours(pos: tuple[int,int]) -> list[tuple[tuple[int,int],str]]:
    neighbours = []
    for direction in ['r', 'l', 'u', 'd']:
        new_pos = do_step(pos, direction)
        if new_pos:
            neighbours.append([new_pos, opposite_direction[direction]])
    return neighbours

def all_neighbours(pos: tuple[int,int], level: str) -> list[tuple[int,tuple[int,int],str]]:
    neighbours = []
    if level=="horizontal":
        directions = ['r', 'l']
    elif level=="vertical":
        directions = ['u', 'd']
    else:
        raise ValueError(f"{level} is not accepted here.")
    
    for direction in directions:
        for steps in range(1,4):
            new_pos = pos
            cost = get_cost(pos)
            for _ in range(steps-1):
                new_pos = do_step(new_pos, direction)
                cost+=get_cost(new_pos)
            new_pos = do_step(new_pos, direction)
            if new_pos:
                neighbours.append([cost, new_pos, str(steps)+opposite_direction[direction]])
    return neighbours
    
shortest_path_map: list[list[int]] = None
shortest_direction_map: list[list[str]] = None
infinity = int(1e9)

def create_shortest_path_map(destination: tuple[int,int], neighbour_creator: object):
    shortest_path_map_vertical: list[list[int]] = [[infinity for _ in range(xlength)] for _ in range(ylength)]
    shortest_path_map_horizontal: list[list[int]] = [[infinity for _ in range(xlength)] for _ in range(ylength)]
    shortest_direction_map_vertical: list[list[str]] = [['' for _ in range(xlength)] for _ in range(ylength)]
    shortest_direction_map_horizontal: list[list[str]] = [['' for _ in range(xlength)] for _ in range(ylength)]

    shortest_path_map_horizontal[destination[0]][destination[1]] = 0
    shortest_path_map_vertical[destination[0]][destination[1]] = 0
    shortest_direction_map_horizontal[destination[0]][destination[1]] = 'x'
    shortest_direction_map_vertical[destination[0]][destination[1]] = 'x'

    from sortedcontainers import SortedList
    queue = SortedList()
    final_distance = 0
    for cost,neighbour,direction in neighbour_creator(destination, "horizontal"):
        queue.add((final_distance + cost, neighbour, direction))
    for cost,neighbour,direction in neighbour_creator(destination, "vertical"):
        queue.add((final_distance + cost, neighbour, direction))
    
    while queue:
        final_distance,position,step = queue.pop(0)
        xpos=position[0]
        ypos=position[1]
        if step[-1] in ['r', 'l']:
            # horizontal
            old_value = shortest_path_map_horizontal[xpos][ypos]
            if old_value<=final_distance:
                continue
            shortest_path_map_horizontal[xpos][ypos]=final_distance
            shortest_direction_map_horizontal[xpos][ypos]=step
            level="vertical"
        elif step[-1] in ['u', 'd']:
            old_value = shortest_path_map_vertical[xpos][ypos]
            if old_value<=final_distance:
                continue
            shortest_path_map_vertical[xpos][ypos]=final_distance
            shortest_direction_map_vertical[xpos][ypos]=step
            level="horizontal"
        else:
            raise ValueError("unknown axis")
        
        for cost,neighbour,direction in neighbour_creator(position, level):
            queue.add((final_distance+cost, neighbour, direction))

    global shortest_path_map, shortest_direction_map
    shortest_path_map = [[min(shortest_path_map_horizontal[a][b],shortest_path_map_vertical[a][b]) for b in range(xlength)] for a in range(ylength)]
    shortest_direction_map = [[shortest_direction_map_horizontal[a][b] if shortest_path_map[a][b]==shortest_path_map_horizontal[a][b] else shortest_direction_map_vertical[a][b] for b in range(xlength)] for a in range(ylength)]
    print("       _ Shortest path map created")

visualisation_map = {
    'r': '→',
    'l': '←',
    'u': '↑',
    'd': '↓',
    'x': 'x'
}

def print_shortest_path_map():
    print("Shortest path map:")
    for row in shortest_path_map:
        print(row)
    print("Shortest direction map:")
    for row in shortest_direction_map:
        print("".join([visualisation_map[char[-1]] for char in row]))

def solve_1(data: list[str]) -> int:
    set_map(data)
    create_shortest_path_map((xlength-1, ylength-1), all_neighbours)
    print_shortest_path_map()
    return shortest_path_map[0][0]

def solve_2(data: list[str]) -> int:
    set_map(data)
    create_shortest_path_map((xlength-1, ylength-1), all_neighbours_for_ultra)
    print_shortest_path_map()
    return shortest_path_map[0][0]

def all_neighbours_for_ultra(pos: tuple[int,int], level: str) -> list[tuple[int,tuple[int,int],str]]:
    neighbours = []
    if level=="horizontal":
        directions = ['r', 'l']
    elif level=="vertical":
        directions = ['u', 'd']
    else:
        raise ValueError(f"{level} is not accepted here.")
    
    for direction in directions:
        for steps in range(4,11):
            new_pos = pos
            cost = get_cost(pos)
            for _ in range(steps-1):
                new_pos = do_step(new_pos, direction)
                cost+=get_cost(new_pos)
            new_pos = do_step(new_pos, direction)
            if new_pos:
                neighbours.append([cost, new_pos, str(steps)+opposite_direction[direction]])
    return neighbours
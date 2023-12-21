
bricks: list[tuple[tuple[int,int,int],int,int]] = []

def set_bricks(data: list[str]):
    global bricks
    bricks = []
    import re
    regex = re.compile(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)')

    for line in data:
        match = regex.match(line)
        if match:
            end1 = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
            end2 = (int(match.group(4)), int(match.group(5)), int(match.group(6)))
            diff = (end2[0]-end1[0], end2[1]-end1[1], end2[2]-end1[2])
            assert(sum([1 for el in diff if el != 0]) <= 1)
            try:
                orientation = [(diff[i]!=0) for i in range(3)].index(True)
            except ValueError:
                # cube
                orientation = 2
            length = diff[orientation]
            if length > 0:
                bricks.append((end1, length+1, orientation))
            else:
                bricks.append((end2, -length+1, orientation))
        else:
            raise ValueError(f"Unknown instruction {line}")
    print("       _ Bricks are set for thread pool")


def is_cube_in_brick(cube: tuple[int,int,int], brick: tuple[tuple[int,int,int],int,int]) -> bool:
    end = brick[0]
    length = brick[1]
    orientation = brick[2]
    if orientation == 0:
        return end[0] <= cube[0] <= end[0]+length-1 and end[1] == cube[1] and end[2] == cube[2]
    elif orientation == 1:
        return end[1] <= cube[1] <= end[1]+length-1 and end[0] == cube[0] and end[2] == cube[2]
    elif orientation == 2:
        return end[2] <= cube[2] <= end[2]+length-1 and end[0] == cube[0] and end[1] == cube[1]
    else:
        raise ValueError(f"Unknown orientation {orientation}")
    
def find_brick_for_cube(cube: tuple[int,int,int]) -> int:
    for i in range(len(bricks)):
        if is_cube_in_brick(cube, bricks[i]):
            return i
    return -1

xlen = 10
ylen = 10
zlen = 500

occupied: list[list[list[bool]]] = None

def find_bricks():
    global occupied
    occupied = [[[False for _ in range(zlen)] for _ in range(ylen)] for _ in range(xlen)]
    for brick in bricks:
        end = brick[0]
        length = brick[1]
        orientation = brick[2]
        if orientation == 0:
            for i in range(length):
                occupied[end[0]+i][end[1]][end[2]] = True
        elif orientation == 1:
            for i in range(length):
                occupied[end[0]][end[1]+i][end[2]] = True
        elif orientation == 2:
            for i in range(length):
                occupied[end[0]][end[1]][end[2]+i] = True
        else:
            raise ValueError(f"Unknown orientation {orientation}")

def drop_bricks() -> bool:
    global bricks
    changed = False
    for j in range(len(bricks)):
        brick = bricks[j]
        end = brick[0]
        length = brick[1]
        orientation = brick[2]
        if end[2] == 1:
            continue
        if orientation == 0:
            overlap = [occupied[end[0]+i][end[1]][end[2]-1] for i in range(length)]
            if any(overlap):
                continue                    
        elif orientation == 1:
            overlap = [occupied[end[0]][end[1]+i][end[2]-1] for i in range(length)]
            if any(overlap):
                continue
        elif orientation == 2:
            if occupied[end[0]][end[1]][end[2]-1]:
                continue
        else:
            raise ValueError(f"Unknown orientation {orientation}")
        changed = True
        bricks[j] = ((end[0], end[1], end[2]-1), length, orientation)
    return changed

bricks_dependencies : list[list[bool]] = None

def create_bricks_dependencies():
    global bricks_dependencies
    bricks_dependencies = [[False for _ in range(len(bricks))] for _ in range(len(bricks))]
    find_bricks()
    for i in range(len(bricks)):
        brick = bricks[i]
        end = brick[0]
        length = brick[1]
        orientation = brick[2]
        if orientation == 0:
            for j in range(length):
                if occupied[end[0]+j][end[1]][end[2]+1]:
                    bricks_dependencies[i][find_brick_for_cube((end[0]+j, end[1], end[2]+1))] = True
        elif orientation == 1:
            for j in range(length):
                if occupied[end[0]][end[1]+j][end[2]+1]:
                    bricks_dependencies[i][find_brick_for_cube((end[0], end[1]+j, end[2]+1))] = True
        elif orientation == 2:
            if occupied[end[0]][end[1]][end[2]+length]:
                bricks_dependencies[i][find_brick_for_cube((end[0], end[1], end[2]+length))] = True

def set_bricks_dependencies(dependencies: list[list[bool]]):
    global bricks_dependencies
    bricks_dependencies = dependencies
    print("       _ Bricks dependencies are set for thread pool")

def count_disintegratable_bricks() -> int:
    import copy
    dependencies = copy.deepcopy(bricks_dependencies)
    for i in range(len(bricks)):
        if [dependencies[j][i] for j in range(len(bricks))].count(True) > 1:
            for j in range(len(bricks)):
                dependencies[j][i] = False
    
    return sum([1 for i in range(len(bricks)) if not any(dependencies[i])])

def get_disintegrate_score(brick_number: int) -> int:
    import copy
    dependencies = copy.deepcopy(bricks_dependencies)
    queue = []
    while any(dependencies[brick_number]):
        index = dependencies[brick_number].index(True)
        queue.append(index)
        dependencies[brick_number][index] = False
    fallen = set()
    while queue:
        index = queue.pop(0)
        if any([dependencies[i][index] for i in range(len(bricks))]):
            continue
        fallen.add(index)
        while any(dependencies[index]):
            index2 = dependencies[index].index(True)
            queue.append(index2)
            dependencies[index][index2] = False

    return len(fallen)


def solve_1(data: list[str]) -> int:
    set_bricks(data)
    find_bricks()
    while drop_bricks():
        find_bricks()
    create_bricks_dependencies()
    return count_disintegratable_bricks()

def solve_2(data: list[str]) -> int:
    set_bricks(data)
    find_bricks()
    while drop_bricks():
        find_bricks()
    create_bricks_dependencies()

    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(initializer=set_bricks_dependencies, initargs=[bricks_dependencies]) as executor:
        results = executor.map(get_disintegrate_score, range(len(bricks)))
    return sum(results)

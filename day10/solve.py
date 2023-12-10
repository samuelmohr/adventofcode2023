# 4 bit number to code each field
# left right top bottom flags
# each field has a 2 out of 4 bits set

NORTH=2
SOUTH=1
WEST=8
EAST=4
symbols = {'|': NORTH+SOUTH, \
           '-': WEST+EAST, \
           'L': NORTH+EAST, \
           'J': NORTH+WEST, \
           '7': SOUTH+WEST, \
           'F': SOUTH+EAST, \
           '.': 0, \
           'S': 15}


import numpy as np
map: np.array = None
width: int = 0
height: int = 0

import sys
sys.setrecursionlimit(20000)

def set_map(data: np.array):
    global map, width, height
    map = data
    width = data.shape[1]
    height = data.shape[0]
    print("       _ Map is set for thread pool")


def vertical_connected(sym1, sym2) -> bool:
    return (sym1 & EAST) and (sym2 & WEST)

def horizontal_connected(sym1, sym2) -> bool:
    return (sym1 & SOUTH) and (sym2 & NORTH)

def next_left(pos1 : tuple[int,int], pos2 : tuple[int,int]) -> tuple[int,int]:
    vdiff=pos2[0]-pos1[0]
    hdiff=pos2[1]-pos1[1]
    if vdiff!=0:
        return (pos2[0],(pos2[1]+vdiff)%height)
    if hdiff!=0:
        return ((pos2[0]-hdiff)%width,pos2[1])
    raise RuntimeError("no neighbouring positions")

def next_right(pos1 : tuple[int,int], pos2 : tuple[int,int]) -> tuple[int,int]:
    vdiff=pos2[0]-pos1[0]
    hdiff=pos2[1]-pos1[1]
    if vdiff!=0:
        return (pos2[0],(pos2[1]-vdiff)%height)
    if hdiff!=0:
        return ((pos2[0]+hdiff)%width,pos2[1])
    raise RuntimeError("no neighbouring positions")

def next_straight(pos1 : tuple[int,int], pos2 : tuple[int,int]) -> tuple[int,int]:
    vdiff=pos2[0]-pos1[0]
    hdiff=pos2[1]-pos1[1]
    if abs(vdiff)+abs(hdiff)!=1:
        raise RuntimeError("no neighbouring positions")
    return ((pos2[0]+vdiff)%width,(pos2[1]+hdiff)%height)

def find_start() -> tuple[int,int]:
    for i in range(height):
      for j in range(width):
        if map[i,j]==15:
          return (i,j)

def find_neighbours(pos: tuple[int,int], overwrite=None)->list[tuple[int,int]]:
    base=map[pos]
    if overwrite!=None:
        base=overwrite
    neighbours=[]
    # west
    if horizontal_connected(map[(pos[0]-1)%width,pos[1]],base):
        neighbours.append(((pos[0]-1)%width,pos[1]))
    # east
    if horizontal_connected(base,map[(pos[0]+1)%width,pos[1]]):
        neighbours.append(((pos[0]+1)%width,pos[1]))
    # north
    if vertical_connected(map[pos[0],(pos[1]-1)%height],base):
        neighbours.append((pos[0],(pos[1]-1)%height))
    # south
    if vertical_connected(base,map[pos[0],(pos[1]+1)%height]):
        neighbours.append((pos[0],(pos[1]+1)%height))
    return neighbours
    
def solve_1(data: list[str]) -> int:
    array=np.empty((len(data),len(data[0])),dtype=np.uint8)
    for i in range(len(data)):
      for j in range(len(data[0])):
        array[i,j]=np.uint8(symbols[data[i][j]])
    return perform(array, start_cycle)

def perform(array, func: object) -> int:
    from multiprocessing import Pool
    with Pool(initializer=set_map, initargs=[array]) as pool:
        results = pool.map(func, range(6))
    return max(results)


def start_cycle(setting: int) -> int:
    start_pos=find_start()
    symbol=symbols[list(symbols.keys())[setting]]
    neighbours=find_neighbours(start_pos,symbol)
    if len(neighbours)!=2:
        return 0
    return follow_path(neighbours[0],neighbours[1],start_pos)/2+1

def follow_path(pos:tuple[int,int],destination:tuple[int,int],previous:tuple[int,int])->int:
    if pos==destination:
        return 0
    neighbours=find_neighbours(pos)
    if len(neighbours)!=2:
        raise RuntimeError("dead end")
    if neighbours[0]==previous:
        return follow_path(neighbours[1],destination,pos)+1
    return follow_path(neighbours[0],destination,pos)+1

def solve_2(data: list[str]) -> int:
    array=np.empty((len(data),len(data[0])),dtype=np.uint8)
    for i in range(len(data)):
      for j in range(len(data[0])):
        array[i,j]=np.uint8(symbols[data[i][j]])
    return perform(array, find_interiour)


marking = None

def find_interiour(setting: int) -> int:
    global marking
    start_pos=find_start()
    symbol=symbols[list(symbols.keys())[setting]]
    neighbours=find_neighbours(start_pos,symbol)
    if len(neighbours)!=2:
        return 0
    marking=np.zeros((height,width),dtype=np.uint8)
    marking[start_pos]=1
    # marking code: unknown 0, visited 1, left 5, right 6
    follow_path_and_mark(neighbours[0],neighbours[1],start_pos)
    complete_markings()
    marker=find_internal_marker()
    return sum([col.count(marker) for col in marking.tolist()])

def mark_if_possible(pos: tuple[int,int], colour: int):
    if marking[pos]==0:
        marking[pos]=colour

def follow_path_and_mark(pos:tuple[int,int],destination:tuple[int,int],previous:tuple[int,int]):
    marking[pos]=1
    if pos==destination:
        return 
    neighbours=find_neighbours(pos)
    if len(neighbours)!=2:
        raise RuntimeError("dead end")
    if next_left(previous,pos) in neighbours:
        mark_if_possible(next_straight(previous,pos),6)
        mark_if_possible(next_right(previous,pos),6)
        follow_path_and_mark(next_left(previous,pos),destination,pos)
    elif next_straight(previous,pos) in neighbours:
        mark_if_possible(next_left(previous,pos),5)
        mark_if_possible(next_right(previous,pos),6)
        follow_path_and_mark(next_straight(previous,pos),destination,pos)
    elif next_right(previous,pos) in neighbours:
        mark_if_possible(next_left(previous,pos),5)
        mark_if_possible(next_straight(previous,pos),5)
        follow_path_and_mark(next_right(previous,pos),destination,pos)
    else:
        raise RuntimeError("heavy calculation error")

def neighbour_markings(pos: tuple[int,int]) -> list[int]:
    return [marking[(pos[0]-1)%width,pos[1]],marking[(pos[0]+1)%width,pos[1]],marking[pos[0],(pos[1]-1)%height],marking[pos[0],(pos[1]+1)%height]]

def complete_markings():
    unknown=False
    for i in range(height):
      for j in range(width):
        if marking[i,j]==0:
          options=neighbour_markings((i,j))
          if 5 in options:
            marking[i,j]=5
          elif 6 in options:
            marking[i,j]=6
          else:
            unknown=True
    if unknown:
        complete_markings()

def find_internal_marker() -> int:
    line=list(marking[0,:])
    if 5 in line:
      return 6
    if 6 in line:
      return 5
    line=list(marking[-1,:])
    if 5 in line:
      return 6
    if 6 in line:
      return 5
    row=list(marking[:,0])
    if 5 in row:
      return 6
    if 6 in row:
      return 5
    row=list(marking[:,-1])
    if 5 in row:
      return 6
    if 6 in row:
      return 5



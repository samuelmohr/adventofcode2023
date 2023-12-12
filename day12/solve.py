def index_of_possible_element(line: str) -> int:
    if '?' in line:
        if '#' in line:
            return min(line.index('#'),line.index('?'))
        return line.index('?')
    return line.index('#')

# returns possible starting values
def find_special_element(line: str, groups: list[int], index: int) -> list[int]:
    if index>=len(groups):
        raise IndexError("index does not point to valid capture group")
    left_cut=sum(groups[0:index])+index
    while 0<left_cut<=len(line) and line[left_cut-1]=='#':
        left_cut=left_cut+1
    right_cut=len(line)- ( sum(groups[index+1:])+len(groups)-index-1 )
    while len(line)>right_cut>=0 and line[right_cut]=='#':
        right_cut=right_cut-1
    return [a+left_cut for a in find_element(line[left_cut:right_cut],groups[index])]

# get exclusive positions of element, e.g. all others must be '.'
def resolve_element(line: str, group: int) -> list[int]:
    if len(line)==0:
        return []
    if line[0]=='.':
        offset=index_of_possible_element(line)
        return [a+offset for a in resolve_element(line[offset:], group)]
    if line[-1]=='.':
        return resolve_element(line[0:len(line)-index_of_possible_element(line[::-1])], group)
    if '#' not in line:
        if group>len(line):
            return []
        if '.' in line:
            index=line.index('.')
            return resolve_element(line[:index], group)+[a+index+1 for a in resolve_element(line[index+1:], group)]
        return list(range(0,len(line)-group+1))
    else:
        if group>len(line):
            raise RuntimeError("impossible because the string is too short")
        index_left=line.index('#')
        index_right=len(line)-line[::-1].index('#')-1
        if index_right-index_left>=group:
            raise RuntimeError("impossible because '#'s are too far away")
        if '.' in line[index_left:index_right+1]:
            raise RuntimeError("impossible because of '.' between '#'s.")
        if '.' in line[0:index_left]:
            offset=line.index('.')
            return [a+offset for a in resolve_element(line[offset+1:],group)]
        if '.' in line:
            return resolve_element(line[0:len(line)-line[::-1].index('.')], group)
        return list(range(max(0,index_right-group+1),min(len(line)-group+1,index_left+1)))

# gets all positions of group regardless of other '#' arounds
def find_element(line: str, group: int) -> list[int]:
    if group>len(line):
        return []
    if line[0]=='.':
        offset=index_of_possible_element(line)
        return [a+offset for a in find_element(line[offset:], group)]
    if line[-1]=='.':
        return find_element(line[0:len(line)-index_of_possible_element(line[::-1])], group)
    if '.' in line:
        index=line.index('.')
        return find_element(line[:index], group)+[a+index+1 for a in find_element(line[index+1:], group)]
    if '#' not in line:
        return list(range(0,len(line)-group+1))
    if len(line)==group:
        return [0]
    positions=[]
    if line[group]!='#':
        positions.append(0)
    for a in range(1,len(line)-group):
        if line[a-1]!='#' and line[a+group]!='#':
            positions.append(a)
    if line[len(line)-group-1]!='#':
        positions.append(len(line)-group)
    return positions

def is_empty(line: str) -> int:
    if "#" in line:
        return 0
    return 1

def count_possibilities(line: str, groups: list[int]) -> int:
    if len(groups)==0:
        return is_empty(line)
    if len(groups)==1:
        return len(resolve_element(line, groups[0]))
    max_length=max(groups)
    max_indices=[i for i in range(len(groups)) if groups[i]==max_length]
    max_index=max_indices[int(len(max_indices)/2)]
    possibilities=0
    for index in find_special_element(line, groups, max_index):
        try:
            possibilities=possibilities+count_possibilities(line[0:max(index-1,0)], groups[:max_index])*count_possibilities(line[index+max_length+1:], groups[max_index+1:])
        except:
            pass
    return possibilities


def process_line(row: str) -> int:
    line=row.split(' ')[0]
    groups=[int(el) for el in row.split(' ')[1].split(',')]
    return count_possibilities(line, groups)

def unfold_and_process_line(row: str) -> int:
    line=row.split(' ')[0]
    line=line+'?'+line+'?'+line+'?'+line+'?'+line
    groups=[int(el) for el in row.split(' ')[1].split(',')]
    groups=groups+groups+groups+groups+groups
    return count_possibilities(line, groups)

def solve_1(data: list[str]) -> int:
    return perform(data, process_line)

def solve_2(data: list[str]) -> int:
    return perform(data, unfold_and_process_line)

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    import tqdm
    results=[]
    with Pool() as pool:
        for c in tqdm.tqdm(pool.imap_unordered(func, data), total=len(data)):
            results.append(c)
    return sum(results)



map: dict[str,list[tuple[str,str]]] = dict()

def set_map(data: list[str]):
    global map
    import re
    regex = re.compile(r'([a-zA-Z]+)\{(.*?)\}')
    for line in data:
        match = regex.match(line)
        if match:
            map[match.group(1)] = [instr.split(':') for instr in match.group(2).split(',')]
    print("       _ Map is set for thread pool")


from dataclasses import dataclass

import re
part_regex = re.compile(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}')
@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @staticmethod
    def from_string(line: str):
        match = part_regex.match(line)
        if match:
            return Part(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))
        raise ValueError(f"Unknown part format {line}")
    
    def __str__(self):
        return f"Part(x={self.x},m={self.m},a={self.a},s={self.s})"
    
    @property
    def score(self):
        return self.x + self.m + self.a + self.s

def run_line(line: str, item: Part) -> str:
    for check in map[line][:-1]:
        # assume check = "x>=100"
        # let python evaluate it on item
        result = eval(f"item.{check[0]}")
        if result:
            return check[1]
    return map[line][-1][0]

def is_accepted(item: Part) -> bool:
    current = 'in'
    while current not in ['A', 'R']:
        current = run_line(current, item)
    return current == 'A'

def solve_1(data: list[str]) -> int:
    # find empty line
    for i in range(len(data)):
        if data[i] == '':
            break

    return perform(data[:i], data[i+1:], [1 for _ in range(len(data[i+1:]))], run_workflow_and_score)

def run_workflow_and_score(line: str) -> int:
    item = Part.from_string(line)
    return run_workflow(item)*item.score

def run_workflow(item: Part) -> int:
    if is_accepted(item):
        return 1
    return 0

def perform(data: list[str], items: list[str], factors: list[int], func: object) -> int:
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(initializer=set_map, initargs=[data]) as executor:
        results = executor.map(func, items)
    return sum([result*factor for result, factor in zip(results, factors)])

def solve_2(data: list[str]) -> int:   
    for i in range(len(data)):
        if data[i] == '':
            break

    from concurrent.futures import ThreadPoolExecutor
    import shutil
    configs = 0
    with ThreadPoolExecutor(initializer=set_map, initargs=[data[:i]]) as executor:
        futures = []
        futures.append(executor.submit(analyse, ("in",[(1,4000) for _ in range(4)])))
        while futures:
            print("Queue size: ", '#' * len(futures), ' ' * (shutil.get_terminal_size().columns - len(futures) - 14), end='\r')
            future = futures.pop()
            if future.result():
                res = future.result()
                if res[0] >= 0:
                    configs += res[0]
                else:
                    for config in res[1]:
                        futures.append(executor.submit(analyse, config))
            else:
                raise ValueError("No result")
    return configs

import re
instruction_regex = re.compile(r'([a-zA-Z])([<>])(\d+)')
fields = ['x', 'm', 'a', 's']

def analyse(config: tuple[str,list[tuple[int,int]]]) -> tuple[int,list[tuple[str,list[tuple[int,int]]]]]:
    mapping = config[0]
    ranges = config[1]

    if mapping == 'A':
        return ((ranges[0][1]-ranges[0][0]+1)*(ranges[1][1]-ranges[1][0]+1)*(ranges[2][1]-ranges[2][0]+1)*(ranges[3][1]-ranges[3][0]+1), [])
    elif mapping == 'R':
        return (0, [])

    next_configs = []

    for check in map[mapping][:-1]:
        match = instruction_regex.match(check[0])
        if match:
            field = fields.index(match.group(1))
            if match.group(2) == '>':
                if match.group(3) == '4000':
                    raise ValueError("4000 is not expected")
                comparison = int(match.group(3))

                if ranges[field][0]>comparison:
                    next_configs.append((check[1], ranges))
                    break
                elif ranges[field][1]<=comparison:
                    continue
                else:
                    ranges_copy = [x for x in ranges]
                    ranges_copy[field] = (comparison+1, ranges_copy[field][1])
                    next_configs.append((check[1], ranges_copy))
                    ranges[field] = (ranges[field][0], comparison)
            elif match.group(2) == '<':
                if match.group(3) == '1':
                    raise ValueError("1 is not expected")
                comparison = int(match.group(3))

                if ranges[field][1]<comparison:
                    next_configs.append((check[1], ranges))
                    break
                elif ranges[field][0]>=comparison:
                    continue
                else:
                    ranges_copy = [x for x in ranges]
                    ranges_copy[field] = (ranges_copy[field][0], comparison-1)
                    next_configs.append((check[1], ranges_copy))
                    ranges[field] = (comparison, ranges[field][1])
            else:
                raise ValueError(f"Unknown comparison {match.group(2)}")
        else:
            raise ValueError(f"Unknown instruction {check[0]}")
    next_configs.append((map[mapping][-1][0], ranges))
    
    return (-1, next_configs)


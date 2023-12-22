
TYPE = ['%', '&', 'broadcaster']

modules : dict[str, tuple[int, list[str]]] = dict()
flipflop_states : dict[str, bool] = dict()
conjunction_states : dict[str, dict[bool]] = dict()

def set_modules(data: list[str]):
    global modules
    for line in data:
        front, back = line.split('->')
        destinations = [x.strip() for x in back.split(',')]
        if front.startswith('broadcaster'):
            modules["broadcaster"] = (TYPE.index("broadcaster"), destinations)
        else:
            type = front[0]
            name = front[1:].strip()
            modules[name] = (TYPE.index(type), destinations)

    global flipflop_states, conjunction_states
    flipflop_states = {name: False for name in modules if modules[name][0] == TYPE.index('%')}
    for name in modules:
        if modules[name][0] == TYPE.index('&'):
            destinations = []
            for key,value in modules.items():
                if name in value[1]:
                    destinations.append(key)
            conjunction_states[name] = {dest: False for dest in destinations}

high_count = 0
low_count = 0



def solve_1(data: list[str]) -> int:
    set_modules(data)
    global high_count, low_count, notify_round
    high_count = 0
    low_count = 0
    
    round = 0
    while round<1000:
        round += 1
        notify_round = round
        perform_round()
        if is_initial_state():
            factor = 1000//round
            high_count *= factor
            low_count *= factor
            round *= factor


    print(f"High count: {high_count}")
    print(f"Low count: {low_count}")
    return high_count * low_count

def is_initial_state() -> bool:
    if any(flipflop_states.values()):
        return False
    for conjunction in conjunction_states.values():
        if any(conjunction.values()):
            return False        
    return True

def perform_round():
    queue = [("broadcaster", -1, "button")]
    while len(queue) > 0:
        name, value, origin = queue.pop(0)
        queue.extend(perform_module(name, value, origin))

notify_list = dict()
notify_round = 0

def perform_module(name: str, value: int, origin: str) -> list[tuple[str, int, str]]:   
    global high_count, low_count
    if value<0:
        low_count += 1
    elif value>0:
        high_count += 1
    else:
        raise ValueError("Value should not be 0")
    if name not in modules:
        return []
    
    if name in notify_list:
        if value<=0:
            notify_list[name].append(notify_round)
    
    type, destinations = modules[name]
    if type == TYPE.index('%'):
        if value>0:
            return []
        flipflop_states[name] = not flipflop_states[name]
        if flipflop_states[name]:
            return [(dest, 1, name) for dest in destinations]
        else:
            return [(dest, -1, name) for dest in destinations]
    elif type == TYPE.index('&'):
        conjunction_states[name][origin] = value>0
        if all(conjunction_states[name].values()):
            return [(dest, -1, name) for dest in destinations]
        else:
            return [(dest, 1, name) for dest in destinations]
    else:
        return [(dest, value, name) for dest in destinations]
    
def solve_2(data: list[str]) -> int:
    set_modules(data)
    global notify_list, notify_round
    notify_list={name: [] for name in analyse_network()}

    round = 0
    while round<5000:
        round += 1
        notify_round = round
        perform_round()
    for name in notify_list:
        print(f"{name}: {notify_list[name][0]}")
    from functools import reduce
    from operator import mul
    return reduce(mul, [notify_list[name][0] for name in notify_list])

def analyse_network() -> list[str]:
    ancestors = {name: [] for name in modules}
    ancestors["rx"] = []
    for name in modules:
        for destination in modules[name][1]:
            ancestors[destination].append(name)
    
    inverters = []
    for name in ancestors['rx']:
        inverters.extend(ancestors[name])
    for name in inverters:
        assert(modules[name][0] == TYPE.index('&'))
    return inverters

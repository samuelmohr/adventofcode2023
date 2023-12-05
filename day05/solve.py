
def parse_input(data: list[str]):
    seed_str = data.pop(0)
    seeds = [int(item) for item in seed_str.split(' ')[1:] if item]
    assert(data.pop(0)=='')
    
    assert(data.pop(0)=="seed-to-soil map:")
    se_to_so=[]
    line=data.pop(0)
    while line != "":
        se_to_so.append([int(item) for item in line.split(' ')])
        line=data.pop(0)
    else:
        assert(line=='')
    
    assert(data.pop(0)=="soil-to-fertilizer map:")
    so_to_fe=[]
    line=data.pop(0)
    while line != "":
        so_to_fe.append([int(item) for item in line.split(' ')])
        line=data.pop(0)
    else:
        assert(line=='')
    
    assert(data.pop(0)=="fertilizer-to-water map:")
    fe_to_wa=[]
    line=data.pop(0)
    while line != "":
        fe_to_wa.append([int(item) for item in line.split(' ')])
        line=data.pop(0)
    else:
        assert(line=='')
    
    assert(data.pop(0)=="water-to-light map:")
    wa_to_li=[]
    line=data.pop(0)
    while line != "":
        wa_to_li.append([int(item) for item in line.split(' ')])
        line=data.pop(0)
    else:
        assert(line=='')
    
    assert(data.pop(0)=="light-to-temperature map:")
    li_to_te=[]
    line=data.pop(0)
    while line != "":
        li_to_te.append([int(item) for item in line.split(' ')])
        line=data.pop(0)
    else:
        assert(line=='')
    
    assert(data.pop(0)=="temperature-to-humidity map:")
    te_to_hu=[]
    line=data.pop(0)
    while line != "":
        te_to_hu.append([int(item) for item in line.split(' ')])
        line=data.pop(0)
    else:
        assert(line=='')
    
    assert(data.pop(0)=="humidity-to-location map:")
    hu_to_lo=[]
    while len(data)!=0:
        line=data.pop(0)
        hu_to_lo.append([int(item) for item in line.split(' ')])
    
    return seeds,[se_to_so,so_to_fe,fe_to_wa,wa_to_li,li_to_te,te_to_hu,hu_to_lo]

def translate_item(mappings: list[list[int]], position: int) -> int:
    for mapping in mappings:
        assert(len(mapping)==3)
        if position in range(mapping[1],mapping[1]+mapping[2]):
            return mapping[0]+position-mapping[1]
    return position

def translate(positions: list[int], mappings: list[list[int]]) -> list[int]:
    return [translate_item(mappings,item) for item in positions]

def solve_1(data: list[str]) -> int:
    seeds,transforms=parse_input(data.copy())
    from functools import reduce
    result=reduce(translate,transforms,seeds)
    return min(result)

def translate_item_range(mappings: list[list[int]], position: list[int]) -> list[list[int]]:
    assert(len(position)==2)
    for mapping in mappings:
        assert(len(mapping)==3)
        if position[0] in range(mapping[1],mapping[1]+mapping[2]):
            end=position[0]+position[1]
            if end<=mapping[1]+mapping[2]:
                return [[mapping[0]+position[0]-mapping[1],position[1]]]
            else:
                length=mapping[1]+mapping[2]-position[0]
                out=translate_item_range(mappings, [position[0]+length,position[1]-length])
                out.append([mapping[0]+position[0]-mapping[1],length])
                return out
    starts=[mapping[0] for mapping in mappings]
    bigger_starts=[i for i in starts if i>position[0]]
    if bigger_starts:
        next=min(bigger_starts)
        out=translate_item_range(mappings,[next,position[1]+position[0]-next])
        out.append([position[0],next-position[0]])
        return out
    else:
        return [position]

def translate_ranges(position_ranges: list[list[int]], mappings: list[list[int]]) -> list[list[int]]:
    next_ranges=[]
    #print("    info: ranges are "+str(position_ranges))
    for position in position_ranges:
        next_ranges.extend(translate_item_range(mappings,position))
    return next_ranges

def solve_2(data: list[str]) -> int:
    seeds,transforms=parse_input(data)
    import numpy as np
    seed_ranges=np.reshape(np.array(seeds),(-1,2)).tolist()
    from functools import reduce
    result=reduce(translate_ranges,transforms,seed_ranges)
    return min([item[0] for item in result])



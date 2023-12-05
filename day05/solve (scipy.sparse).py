
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

import numpy as np
from scipy.sparse import csr_matrix,find

MAXSIZE=10000000000

def create_seed_vector(seeds : list[int]):
    row=np.array(seeds,dtype=np.int8)
    ones=np.array([1 for _ in range(len(seeds))],dtype=np.int8)
    zeros=np.array([0 for _ in range(len(seeds))],dtype=np.int8)
    vector = csr_matrix((ones,(row,zeros)),shape=(MAXSIZE,1),dtype=np.int8)
    return vector

def create_transfer_matrix(mappings : list[list[int]]):
    input=[]
    output=[]
    for mapping in mappings:
        assert(len(mapping)==3)
        input.extend(range(mapping[1],mapping[1]+mapping[2]))
        output.extend(range(mapping[0],mapping[0]+mapping[2]))
    unlisted=[i for i in range(MAXSIZE) if i not in input]
    input.extend(unlisted)
    output.extend(unlisted)
    data=np.array([1 for _ in range(len(input))],dtype=np.int8)
    matrix = csr_matrix((data,(np.array(output,dtype=np.int8),np.array(input,dtype=np.int8))),shape=(MAXSIZE,MAXSIZE),dtype=np.int8)
    return matrix

def solve_1(data: list[str]) -> int:
    seeds,transforms=parse_input(data)
    seed_vector=create_seed_vector(seeds)
    transfer_matrix_list=[create_transfer_matrix(mappings) for mappings in transforms]
    from functools import reduce
    result=reduce(lambda vector,matrix:matrix @ vector,transfer_matrix_list,seed_vector)
    return min(find(result)[0])

    

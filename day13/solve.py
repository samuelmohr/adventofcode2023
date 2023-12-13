import numpy as np

def analyse_field(block: list[str]) -> int:
    matrix=create_matrix(block)
    return row_analysis(matrix.transpose())+100*row_analysis(matrix)

def relaxed_analyse_field(block: list[str]) -> int:
    matrix=create_matrix(block)
    return relaxed_row_analysis(matrix.transpose())+100*relaxed_row_analysis(matrix)

def create_matrix(block: list[str]) -> np.array:
    vsize=len(block)
    hsize=len(block[0])
    matrix=np.zeros((vsize,hsize),dtype=np.int8)
    for i in range(vsize):
        for j in range(hsize):
            if block[i][j]=='#':
                matrix[i,j]=1
    return matrix

def row_analysis(matrix: np.array) -> int:
    score=0
    indices=get_candidates(matrix)
    for i in indices:
        if is_symmetric(matrix, i):
            score=score+i
    return score

def relaxed_row_analysis(matrix: np.array) -> int:
    score=0
    indices=relaxed_get_candidates(matrix)
    for i in indices:
        if is_one_off_symmetric(matrix, i):
            score=score+i
    return score

def get_candidates(matrix: np.array) -> list[int]:
    size=matrix.shape[0]
    test_matrix=np.zeros((size-1,size),dtype=np.int8)
    for i in range(size-1):
        test_matrix[i,i]=1
        test_matrix[i,i+1]=-1
    test=np.matmul(test_matrix,matrix).any(axis=1)
    return [i+1 for i in range(size-1) if not test[i]]

def relaxed_get_candidates(matrix: np.array) -> list[int]:
    size=matrix.shape[0]
    test_matrix=np.zeros((size-1,size),dtype=np.int8)
    for i in range(size-1):
        test_matrix[i,i]=1
        test_matrix[i,i+1]=-1
    test=np.absolute(np.matmul(test_matrix,matrix)).sum(axis=1)
    return [i+1 for i in range(size-1) if test[i]<=1]

def is_symmetric(matrix: np.array, index: int) -> bool:
    size=matrix.shape[0]
    length=min(index,size-index)
    test_matrix=np.zeros((length,size),dtype=np.int8)
    for i in range(length):
        test_matrix[i,index-i-1]=1
        test_matrix[i,index+i]=-1
    test=np.matmul(test_matrix,matrix).any(axis=1)
    return not any(test)

def is_one_off_symmetric(matrix: np.array, index: int) -> bool:
    size=matrix.shape[0]
    length=min(index,size-index)
    test_matrix=np.zeros((length,size),dtype=np.int8)
    for i in range(length):
        test_matrix[i,index-i-1]=1
        test_matrix[i,index+i]=-1
    test=np.matmul(test_matrix,matrix)
    return np.count_nonzero(test)==1


def solve_1(data: list[str]) -> int:
    breaks=[i for i in range(len(data)) if data[i]==""]
    blocks=[data[a+1:b] for a,b in zip([-1]+breaks,breaks+[len(data)])]
    return perform(blocks, analyse_field)

def solve_2(data: list[str]) -> int:
    breaks=[i for i in range(len(data)) if data[i]==""]
    blocks=[data[a+1:b] for a,b in zip([-1]+breaks,breaks+[len(data)])]
    return perform(blocks, relaxed_analyse_field)

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    import tqdm
    results=[]
    with Pool() as pool:
        for c in tqdm.tqdm(pool.imap_unordered(func, data), total=len(data)):
            results.append(c)
    return sum(results)


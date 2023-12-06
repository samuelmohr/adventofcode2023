import math

def quadr_zeros(coeff: tuple[float,float,float]) -> tuple[float,float]:
    qq=math.sqrt((coeff[1]**2)-4*coeff[0]*coeff[2])
    z1=(-coeff[1]+qq)/(2*coeff[0])
    z2=(-coeff[1]-qq)/(2*coeff[0])
    return (z1,z2)

def strategy_count(input: tuple[int,int]) -> int:
    polynom_coeff=(-1.,float(input[0]),-float(input[1]))
    z1,z2=quadr_zeros(polynom_coeff)
    assert(z1<=z2)
    distance=math.floor(z2)-math.ceil(z1)+1-(math.floor(z2)==z2)-(math.ceil(z1)==z1)
    return distance

def solve_1(data: list[str]) -> int:
    assert(len(data)==2)
    time=data[0].split(':')[1]
    time_pts=[int(number) for number in time.split(' ') if number]
    distance=data[1].split(':')[1]
    distance_pts=[int(number) for number in distance.split(' ') if number]
    return perform(zip(time_pts,distance_pts), strategy_count)


def solve_2(data: list[str]) -> int:
    assert(len(data)==2)
    time=data[0].split(':')[1]
    time_pts=[int("".join([number for number in time.split(' ') if number]))]
    distance=data[1].split(':')[1]
    distance_pts=[int("".join([number for number in distance.split(' ') if number]))]
    return perform(zip(time_pts,distance_pts), strategy_count)
    
def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    with Pool() as pool:
        results = pool.map(func, data)
    from functools import reduce
    return reduce(lambda a,b: a*b,results,1)


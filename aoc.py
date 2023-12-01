def read(filename: str) -> list[str]:
    import os
    if not os.path.exists(filename):
        raise RuntimeError(f"File {filename} does not exist.")
    with open(filename,"r") as file:
        return file.readlines()


def import_solve(day: int) -> object:
    import importlib
    name = f"day{day:0=2}.solve"
    solver=importlib.import_module(name)
    return solver


def process(day: int, filename: str) -> None:
    print("Welcome to Advent of Code 2023")
    print(f"Solving day {day}:")
    print("  Import solver …")
    solver=import_solve(day)
    print("  -> Found")
    print("  Read input …")
    data=read(filename)
    print("  -> Done")
    print("  Solve Task 1 …")
    if "solve_1" in dir(solver):
        answer=solver.solve_1(data)
        print("  -> Solved")
        print(f"  -> The solution of Task 1 is {answer}")
    else:
        print("  !! Solver has no implementation for Task 1")
    print("  Solve Task 2 …")
    if "solve_2" in dir(solver):
        answer=solver.solve_2(data)
        print("  -> Solved")
        print(f"  -> The solution of Task 2 is {answer}")
    else:
        print("  !! Solver has no implementation for Task 2")
    
    

if __name__ == '__main__':
    import sys
    if len(sys.argv)!=3:
        print("Use aoc with day number and input file: python aoc.py [day of December] [filename]")
        sys.exit(255)
    day = int(sys.argv[1])
    filename = "day{day:0=2}/{name}".format(day=day, name=sys.argv[2])
    process(day, filename)
    sys.exit(0)


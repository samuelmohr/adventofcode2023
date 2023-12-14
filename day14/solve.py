
def analyse_column(row: str) -> int:
    return sum([cost for char,cost in zip(row, range(len(row), 0, -1)) if char == "O"])

def tilt_and_analyse_column(row: str) -> int:
    return analyse_column(tilt_row(row))

def solve_1(data: list[str]) -> int:
    columns = ["".join([data[j][i] for j in range(len(data))]) for i in range(len(data[0]))]
    return sum(map(tilt_and_analyse_column, columns))

def solve_2(data: list[str]) -> int:
    columns = ["".join([data[j][i] for j in range(len(data))]) for i in range(len(data[0]))]
    states = dict()
    allow_checks = True
    total_rounds = 1000000000
    i = 0
    while i < total_rounds:
        columns = cycle(columns)
        key = hash("".join(columns))
        if allow_checks and key in states:
            allow_checks = False
            cycle_length = i - states[key]
            remaining_rounds = total_rounds - i
            i += cycle_length * (remaining_rounds // cycle_length)
        else:
            states[key] = i
        i += 1
    return sum(map(analyse_column, columns))

def cycle(data: list[str]) -> list[str]:
    return tilt(tilt(tilt(tilt(data))))

def tilt(data: list[str]) -> list[str]:
    # tilts left and return as a list from bottom to top
    data = [*map(tilt_row, data)]
    return ["".join([data[j][i] for j in range(len(data))]) for i in range(len(data[0]))][::-1]

def tilt_row(row: str) -> str:
    s = []
    spaces = 0
    for i in range(len(row)):
        if row[i] == ".":
            spaces += 1
        elif row[i] == "O":
            s.append("O")
        elif row[i] == "#":
            s.extend(["." for _ in range(spaces)])
            s.append("#")
            spaces = 0
    s.extend(["." for _ in range(spaces)])
    return "".join(s)

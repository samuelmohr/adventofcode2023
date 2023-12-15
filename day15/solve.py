def aoc_hash(x: str) -> int:
    val = 0
    for i in range(len(x)):
        val += ord(x[i])
        val *= 17
        val %= 256
    return val

def solve_1(data: list[str]) -> int:
    sequence=data[0].split(',')
    return sum(perform(sequence, aoc_hash))

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    with Pool() as pool:
        results = pool.map(func, data)
    return results

def solve_2(data: list[str]) -> int:
    sequence=data[0].split(',')
    boxes = [dict() for _ in range(256)]

    from functools import reduce
    final_boxes = reduce(follow_instruction, sequence, boxes)
    return sum([(number+1)*score(box) for number,box in enumerate(final_boxes)])

def follow_instruction(boxes: list[dict], instruction: str) -> list[dict]:
    if '-' in instruction:
        label = instruction.split('-')[0]
        number = aoc_hash(label)
        if label in boxes[number]:
            del boxes[number][label]
    elif '=' in instruction:
        label, value = instruction.split('=')
        number = aoc_hash(label)
        boxes[number][label] = int(value)
    else:
        raise ValueError(f"Unknown instruction {instruction}")
    return boxes

def score(box: dict) -> int:
    return sum((number+1)*value for number, value in enumerate(box.values()))

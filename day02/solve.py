import re
regex_game = re.compile(r"Game (\d+): (.*)")
regex_red = re.compile(r"(?:^|.*\D)(\d+) red")
regex_green = re.compile(r"(?:^|.*\D)(\d+) green")
regex_blue = re.compile(r"(?:^|.*\D)(\d+) blue")

class Configuration:
    def __init__(self, red : int, green : int, blue : int):
        self.red : int = red
        self.green : int = green
        self.blue : int = blue
        
    def __str__(self):
        return f"{self.red} red, {self.green} green, {self.blue} blue"
    
    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue
    
    def __le__(self, other):
        return (self.red <= other.red) and (self.green <= other.green) and (self.blue <= other.blue)
        
    def max(self, other):
        return Configuration(max(self.red, other.red), max(self.green, other.green), max(self.blue, other.blue))
    
    def score(self) -> int:
        return self.red * self.green * self.blue

main_game = Configuration(12,13,14)

def parse_config(input: str) -> Configuration:
    red=0
    redmatch = regex_red.match(input)
    if redmatch != None:
        red=int(redmatch.group(1))
    green=0
    greenmatch = regex_green.match(input)
    if greenmatch != None:
        green=int(greenmatch.group(1))
    blue=0
    bluematch = regex_blue.match(input)
    if bluematch != None:
        blue=int(bluematch.group(1))
    return Configuration(red, green, blue)

def read_game(input: str) -> tuple[int, list[Configuration]]:
    match = regex_game.match(input)
    if match == None:
        return (-1,[])
    
    number = int(match.group(1))
    draws = match.group(2).split(';')
    configs = list(map(parse_config, draws))
    return [number, configs]


def plausibility_check(input: str) -> int:
    game_nr, configs = read_game(input)
    if game_nr < 0:
        return 0
    possible = [bool(config <= main_game) for config in configs]
    return all(possible) * game_nr

def calc_power(input: str) -> int:
    game_nr, configs = read_game(input)
    if game_nr < 0:
        return 0
    from functools import reduce
    return reduce(lambda base, next: Configuration.max(base,next), configs, Configuration(0,0,0)).score()

def solve_1(data: list[str]) -> int:
    return perform(data, plausibility_check)
    
def solve_2(data: list[str]) -> int:
    return perform(data, calc_power)

def perform(data: list[str], func: object) -> int:
    from multiprocessing import Pool
    with Pool() as pool:
        results = pool.map(func, data)
    return sum(results)
    
    

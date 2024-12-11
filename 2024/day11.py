def get_input():
    with open("day11.txt", "r") as file:
        data = file.read().splitlines()[0]

    return [int(i) for i in data.split(" ")]


def replace_stone(stone):
    if stone == 0:
        return [1]
    
    string = str(stone)

    if len(string) % 2 == 0:
        mid = len(string) // 2

        a = int(string[:mid])
        b = int(string[mid:])

        return [a, b]
    else:
        return [stone * 2024]
    

def blink(stones):
    new_stones = []
    for i in stones:
        new_stones += replace_stone(i)

    return new_stones


def part1():
    stones = get_input()

    for _ in range(25):
        stones = blink(stones)

    print(len(stones))


part1()


#--------


def increment_dict(dict, key, inc_num):
    if key in dict:
        dict[key] += inc_num
    else:
        dict[key] = inc_num


def build_dict(stones):
    occurences = {}

    for i in stones:
        increment_dict(occurences, i, 1)

    return occurences


def faster_blink(stone_dict):
    new_dict = {}
    for stone, num in stone_dict.items():
        new_stones = replace_stone(stone)

        for i in new_stones:
            increment_dict(new_dict, i, num)

    return new_dict


def part2():
    stones = get_input()
    stone_dict = build_dict(stones)

    for _ in range(75):
        stone_dict = faster_blink(stone_dict)

    total = sum(stone_dict.values())

    print(total)


part2()
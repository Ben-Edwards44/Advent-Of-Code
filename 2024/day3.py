import re


def get_input():
    with open("day3.txt", "r") as file:
        data = file.read()

    return data[:-1]


def evaluate_mul(string):
    a, b = [int(i) for i in re.findall(r"[0-9]+", string)]

    return a * b


def eval_string(string):
    muls = re.findall(r"mul\([0-9]?[0-9]?[0-9]?,[0-9]?[0-9]?[0-9]?\)", string)

    return sum(evaluate_mul(i) for i in muls)


def part1():
    inp = get_input()
    
    print(eval_string(inp))


part1()


#-----------


def part2():
    inp = get_input()

    total = 0

    do_lists = inp.split("do()")
    for i in do_lists:
        dont_lists = i.split("don't()")
        total += eval_string(dont_lists[0])

    print(total)


part2()
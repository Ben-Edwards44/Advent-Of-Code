import re


FILENAME = "day6.txt"


def get_input():
    with open(FILENAME, "r") as file:
        data = file.read().splitlines()

    return [re.findall(r"[0-9]+|\+|\*", i) for i in data]


def mul(list):
    total = 1
    for i in list:
        total *= i

    return total


def eval(col):
    if col[-1] == "+":
        func = sum
    else:
        func = mul

    nums = map(int, col[:-1])

    return func(nums)


def part1():
    rows = get_input()

    total = 0
    for i in range(len(rows[0])):
        total += eval([x[i] for x in rows])

    print(total)


part1()


#------


def new_get_input():
    with open(FILENAME, "r") as file:
        data = file.read().splitlines()

    vert_nums = []
    current_nums = []
    for i in range(len(data[0])):
        num = ""
        for x in range(len(data) - 1):
            char = data[x][i]
            if char != " ":
                num += char

        if num == "":
            vert_nums.append(current_nums)
            current_nums = []
        else:
            current_nums.append(num)

    vert_nums.append(current_nums)

    return vert_nums, re.findall(r"\+|\*", data[-1])


def part2():
    nums, ops = new_get_input()

    total = 0
    for i, x in enumerate(nums):
        total += eval(x + [ops[i]])

    print(total)


part2()
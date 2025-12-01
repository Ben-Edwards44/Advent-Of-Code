def get_input():
    with open("day1.txt", "r") as file:
        data = file.read().splitlines()

    return [(i[0], int(i[1:])) for i in data]


def part1():
    num = 50
    total = 0
    turns = get_input()

    for i in turns:
        if i[0] == "L":
            mult = -1
        else:
            mult = 1

        num = (num + mult * i[1]) % 100

        if num == 0:
            total += 1

    print(total)


part1()


#----------


def get_num_clicks(current_num, step, mult):
    if mult == -1:
        to_zero = current_num
    else:
        to_zero = 100 - current_num

    if step >= to_zero and to_zero != 0:
        zeros_before = 1
    else:
        zeros_before = 0

    zeros_after = max(0, (step - to_zero) // 100)

    return zeros_before + zeros_after


def part2():
    num = 50
    total = 0
    turns = get_input()

    for i in turns:
        if i[0] == "L":
            mult = -1
        else:
            mult = 1

        total += get_num_clicks(num, i[1], mult)

        num = (num + mult * i[1]) % 100

    print(total)


part2()
def get_input():
    with open("day3.txt", "r") as file:
        data = file.read().splitlines()

    return [[int(x) for x in i] for i in data]


def get_max_joltage(bank):
    a = 0
    b = 0

    for i, x in enumerate(bank):
        if x > a and i < len(bank) - 1:
            a = x
            b = bank[i + 1]
        elif x > b:
            b = x

    return 10 * a + b


def part1():
    banks = get_input()

    total = sum(map(get_max_joltage, banks))

    print(total)


part1()


#--------


def new_max_joltage(bank, num_after):
    if num_after == -1:
        return 0

    max_joltage = 0
    index = 0
    for i, x in enumerate(bank[:len(bank) - num_after]):
        if x > max_joltage:
            max_joltage = x
            index = i

    return max_joltage * 10**num_after + new_max_joltage(bank[index + 1:], num_after - 1)


def part2():
    banks = get_input()

    total = sum([new_max_joltage(i, 11) for i in banks])

    print(total)


part2()
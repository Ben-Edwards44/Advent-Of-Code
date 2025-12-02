def get_input():
    with open("day2.txt", "r") as file:
        data = file.read().strip()

    ranges = []
    for i in data.split(","):
        s, e = i.split("-")
        ranges.append((int(s), int(e)))

    return ranges


def get_invalid(s, e):
    str_s = str(s)
    mid = len(str_s) // 2

    if mid == 0:
        repeat = 1
    else:
        repeat = int(str_s[:mid])

    invalid = []
    while True:
        n = int(f"{repeat}{repeat}")

        if n > e:
            break
        elif n >= s:
            invalid.append(n)

        repeat += 1

    return invalid


def part1():
    ranges = get_input()

    total = 0
    for i in ranges:
        total += sum(get_invalid(*i))

    print(total)


part1()


#----------


def get_repeated(s, e, num_repeats):
    str_s = str(s)
    mid = len(str_s) // num_repeats

    if mid == 0:
        repeat = 1
    else:
        repeat = int(str_s[:mid])

    invalid = []
    while True:
        n = int(str(repeat) * num_repeats)

        if n > e:
            break
        elif n >= s:
            invalid.append(n)

        repeat += 1

    return invalid


def get_new_invalid(s, e):
    invalid = set()
    max_repeats = len(str(e))
    for i in range(2, max_repeats + 1):
        for x in get_repeated(s, e, i):
            invalid.add(x)

    return invalid


def part2():
    ranges = get_input()

    total = 0
    for i in ranges:
        total += sum(get_new_invalid(*i))

    print(total)


part2()
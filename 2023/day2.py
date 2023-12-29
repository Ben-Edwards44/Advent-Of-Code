def get_input():
    with open("day2.txt", "r") as file:
        data = file.read()

    return [i.split(": ") for i in data.split("\n")[:-1]]


def get_max(string):
    string = string.split("; ")

    max_r = 0
    max_g = 0
    max_b = 0

    for i in string:
        i = i.split(", ")

        for x in i:
            num, colour = x.split(" ")
            num = int(num)

            if colour == "red" and num > max_r:
                max_r = num
            elif colour == "blue" and num > max_b:
                max_b = num
            elif colour == "green" and num > max_g:
                max_g = num

    return max_r, max_g, max_b


def part1():
    games = get_input()

    total = 0

    for i in games:
        g_id = int(i[0][5:])

        r, g, b = get_max(i[1])

        if r <= 12 and g <= 13 and b <= 14:
            total += g_id

    print(total)


part1()

# --------

def part2():
    games = get_input()

    total = 0

    for i in games:
        g_id = int(i[0][5:])

        r, g, b = get_max(i[1])

        total += r * g * b

    print(total)


part2()
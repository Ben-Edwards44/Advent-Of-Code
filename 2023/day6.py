def get_input():
    with open("day6.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    data = [get_nums(i) for i in data]

    return data


def get_nums(string):
    nums = []
    current = ""

    for i in string:
        if i in "0123456789":
            current += i
        elif i == " ":
            if current != "":
                nums.append(int(current))
                current = ""

    if current != "":
        nums.append(int(current))

    return nums


dist = lambda time_left, speed: time_left * speed


def find_total(total_time, best_dist):
    first = 0
    for i in range(total_time):
        speed = i
        time = total_time - i

        d = dist(time, speed)

        if d > best_dist:
            first = i
            break

    sym = total_time - first

    return sym - first + 1


def part1():
    times, bests = get_input()

    total = 1
    for time, best in zip(times, bests):
        t = find_total(time, best)
        total *= t

    print(total)


part1()


# -------


def new_input():
    with open("day6.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    data = [new_nums(i) for i in data]

    return data


def new_nums(string):
    num = ""

    for i in string:
        if i in "0123456789":
            num += i

    return int(num)


def part2():
    time, best_dist = new_input()

    total = find_total(time, best_dist)

    print(total)


part2()
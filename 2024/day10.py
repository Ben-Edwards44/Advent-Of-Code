def get_input():
    with open("day10.txt", "r") as file:
        data = file.read().splitlines()

    return [[int(i) for i in x] for x in data]


def take_steps(map, x, y, end_dests):
    current = map[x][y]

    if current == 9:
        end_dests.append((x, y))
        return
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j or i != 0 and j != 0: continue

            new_x = x + i
            new_y = y + j
            in_bounds = 0 <= new_x < len(map) and 0 <= new_y < len(map[0])

            if in_bounds and map[new_x][new_y] == current + 1: take_steps(map, new_x, new_y, end_dests)


def get_trailhead_score(map, x, y):
    dests = []
    take_steps(map, x, y, dests)

    return len(set(dests))


def part1():
    map = get_input()

    total = 0
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == 0: total += get_trailhead_score(map, i, j)

    print(total)


part1()


#--------


def get_trailhead_rating(map, x, y):
    dests = []
    take_steps(map, x, y, dests)

    return len(dests)


def part2():
    map = get_input()

    total = 0
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == 0: total += get_trailhead_rating(map, i, j)

    print(total)


part2()
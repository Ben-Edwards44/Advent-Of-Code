def get_input():
    with open("day20.txt", "r") as file:
        data = file.read().splitlines()

    return [[i for i in x] for x in data]


def get_char_pos(map, char):
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == char:
                map[i][j] = "."

                return i, j


def get_neighbours(map, x, y, char):
    neighbours = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_x, new_y = x + i, y + j

            if i == 0 and j == 0 or i != 0 and j != 0: continue
            if not 0 <= new_x < len(map) or not 0 <= new_y < len(map[0]): continue

            if map[new_x][new_y] == char: neighbours.append((new_x, new_y))

    return neighbours


def fill_neighbours(x, y, map, dists, value):
    neighbours = get_neighbours(map, x, y, ".")

    for i, j in neighbours:
        if dists[i][j] is None: dists[i][j] = value


def get_dists(map):
    end_x, end_y = get_char_pos(map, "E")
    start_x, start_y = get_char_pos(map, "S")

    dists = [[None for _ in i] for i in map]
    dists[start_x][start_y] = 0

    current = 0
    while dists[end_x][end_y] is None:
        for i, x in enumerate(dists):
            for j, k in enumerate(x):
                if k == current:
                    fill_neighbours(i, j, map, dists, current + 1)

        current += 1

    return dists    


def disable_one_picosecond(map, dists, start_dist, wall_x, wall_y, all_shortcuts):
    clear_neighbours = get_neighbours(map, wall_x, wall_y, ".")

    for end_x, end_y in clear_neighbours:
        saved = dists[end_x][end_y] - start_dist - 2

        if saved > 0:
            if saved in all_shortcuts:
                all_shortcuts[saved] += 1
            else:
                all_shortcuts[saved] = 1


def get_shortcuts(map, dists, wall_x, wall_y, all_shortcuts):
    clear_neighbours = get_neighbours(map, wall_x, wall_y, ".")

    for start_x, start_y in clear_neighbours:
        start_dist = dists[start_x][start_y]

        disable_one_picosecond(map, dists, start_dist, wall_x, wall_y, all_shortcuts)


def part1():
    map = get_input()
    dists = get_dists(map)

    shortcuts = {}
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == "#": get_shortcuts(map, dists, i, j, shortcuts)

    total = 0
    for saved, num in shortcuts.items():
        if saved >= 100:
            total += num

    print(total)


part1()


#-------


manhattan_dist = lambda start_x, start_y, end_x, end_y: abs(start_x - end_x) + abs(start_y - end_y)


def get_long_shortcuts(dists, start_x, start_y, all_shortcuts):
    start_dist = dists[start_x][start_y]

    for i, x in enumerate(dists):
        if i - start_x > 20: break

        for j, k in enumerate(x):
            if k is None: continue
            if j - start_y > 20: break

            cheat_len = manhattan_dist(start_x, start_y, i, j)
            saved = dists[i][j] - start_dist - cheat_len

            if cheat_len <= 20 and saved > 0:
                if saved in all_shortcuts:
                    all_shortcuts[saved] += 1
                else:
                    all_shortcuts[saved] = 1


def part2():
    map = get_input()
    dists = get_dists(map)

    shortcuts = {}
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == ".": get_long_shortcuts(dists, i, j, shortcuts)

    total = 0
    for saved, num in shortcuts.items():
        if saved >= 100:
            total += num

    print(total)


part2()
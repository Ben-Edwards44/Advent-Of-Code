def get_input():
    with open("t.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    final = []
    for i, x in enumerate(data):
        l = list(x)
        final.append(l)

        if "S" in l:
            start_x = i
            start_y = l.index("S")

    return final, start_x, start_y


def get_possible(grid, x, y):
    possible = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0 or i != 0 and j != 0:
                continue

            new_x = x + i
            new_y = y + j

            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and (grid[new_x][new_y] == "." or grid[new_x][new_y] == "S"):
                possible.append((new_x, new_y))

    return possible


def complete_step(grid, prev_coords):
    new_coords = []

    for i in prev_coords:
        new_coords += get_possible(grid, i[0], i[1])

    return list(set(new_coords))


def part1():
    grid, s_x, s_y = get_input()

    coords = [(s_x, s_y)]

    for _ in range(50):
        coords = complete_step(grid, coords)

    total = len(coords)

    print(total)


part1()


#---------


#Did not manage part 2
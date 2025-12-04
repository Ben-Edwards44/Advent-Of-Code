def get_input():
    with open("day4.txt", "r") as file:
        data = file.read().splitlines()

    return [[i for i in x] for x in data]


def get_neighbours(grid, x, y):
    neighbours = []
    for i in range(-1, 2):
        new_x = x + i

        if not 0 <= new_x < len(grid):
            continue

        for j in range(-1, 2):
            new_y = y + j

            if not 0 <= new_y < len(grid[0]) or i == 0 and j == 0:
                continue

            neighbours.append(grid[new_x][new_y])

    return neighbours


def can_access(grid, x, y):
    return grid[x][y] == "@" and get_neighbours(grid, x, y).count("@") < 4


def part1():
    grid = get_input()

    total = 0
    for i in range(len(grid)):
        for x in range(len(grid[0])):
            if can_access(grid, i, x):
                total += 1

    print(total)


part1()


#-------


def remove_all(grid):
    total = 0
    for i in range(len(grid)):
        for x in range(len(grid[0])):
            if can_access(grid, i, x):
                grid[i][x] = "."
                total += 1

    return total


def part2():
    grid = get_input()

    total = 0
    just_removed = remove_all(grid)
    while just_removed > 0:
        total += just_removed
        just_removed = remove_all(grid)

    print(total)


part2()
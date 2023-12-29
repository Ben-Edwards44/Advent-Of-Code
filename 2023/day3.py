def get_input():
    with open("day3.txt", "r") as file:
        data = file.read()

    return data.split("\n")[:-1]


def get_entire_num(grid, x, y, done_inxs):
    start_y = y

    while grid[x][start_y - 1] in "0123456789":
        start_y -= 1

    num = ""
    i = 0
    while start_y + i < len(grid[x]) and grid[x][start_y + i] in "0123456789":
        if (x, start_y + i) in done_inxs:
            return 0

        done_inxs.add((x, start_y + i))
        
        num += grid[x][start_y + i]
        i += 1

    return int(num)


def get_surround_inxs(grid, x, y, done_inxs):
    inxs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            inx1 = x + i
            inx2 = y + j

            if (inx1, inx2) not in done_inxs and 0 <= inx1 < len(grid) and 0 <= inx2 < len(grid[x]):
                if grid[inx1][inx2] in "0123456789":
                    inxs.append((inx1, inx2))

    return inxs


is_symbol = lambda char: char != "." and char not in "0123456789"


def get_total(grid):
    total = 0
    done_inxs = set()

    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if is_symbol(k):
                num_inxs = get_surround_inxs(grid, i, j, done_inxs)

                for n, m in num_inxs:
                    total += get_entire_num(grid, n, m, done_inxs)

    return total


def part1():
    grid = get_input()
    total = get_total(grid)

    print(total)


part1()

#---------

def get_adj_parts(grid, x, y):
    #one part num can be adjacent to 2 gears
    done_inxs = set()

    num_inxs = get_surround_inxs(grid, x, y, done_inxs)

    adj_nums = []

    for n, m in num_inxs:
        num = get_entire_num(grid, n, m, done_inxs)

        if num != 0:
            adj_nums.append(num)

    return adj_nums


def total_gears(grid):
    total = 0

    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == "*":
                adj = get_adj_parts(grid, i, j)

                if len(adj) == 2:
                    total += adj[0] * adj[1]

    return total


def part2():
    grid = get_input()
    total = total_gears(grid)

    print(total)


part2()
WIDTH = 101
HEIGHT = 103


def get_input():
    with open("day14.txt", "r") as file:
        data = file.read().splitlines()

    pos = []
    vels = []
    for i in data:
        p, v = i.split(" ")

        px, py = p.split(",")
        vx, vy = v.split(",")

        pos.append([int(px[2:]), int(py)])
        vels.append([int(vx[2:]), int(vy)])

    return pos, vels


def get_pos(time, pos, vel):
    px = (pos[0] + vel[0] * time) % WIDTH
    py = (pos[1] + vel[1] * time) % HEIGHT

    return px, py


def get_quadrant(x, y):
    if x == WIDTH // 2 or y == HEIGHT // 2: return

    if x < WIDTH // 2:
        if y < HEIGHT // 2:
            return 0
        else:
            return 1
    else:
        if y < HEIGHT // 2:
            return 2
        else:
            return 3


def part1():
    pos, vels = get_input()

    quads = [0, 0, 0, 0]
    for p, v in zip(pos, vels):
        x, y = get_pos(100, p, v)
        quad = get_quadrant(x, y)

        if quad is not None:
            quads[quad] += 1

    total = 1
    for i in quads:
        total *= i

    print(total)


part1()


#------


def print_grid(grid):
    for i in grid:
        print("".join(i))


def is_christmas_tree(grid):
    num_adj = 0
    total = 0

    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k != "#": continue

            total += 1

            lx = i
            ly = j - 1
            ux = i - 1
            uy = j

            if 0 <= lx < len(grid) and 0 <= ly < len(grid[0]) and grid[lx][ly] == "#": num_adj += 1
            if 0 <= ux < len(grid) and 0 <= uy < len(grid[0]) and grid[ux][uy] == "#": num_adj += 1

    return num_adj >= total * 0.5 and total > 0


def part2():
    pos, vels = get_input()

    t = 0
    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    while not is_christmas_tree(grid):
        t += 1

        quads = [0, 0, 0, 0]
        grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for p, v in zip(pos, vels):
            x, y = get_pos(t, p, v)
            quad = get_quadrant(x, y)

            if quad is not None:
                quads[quad] += 1

            grid[y][x] = "#"

    print_grid(grid)
    print(t)


part2()
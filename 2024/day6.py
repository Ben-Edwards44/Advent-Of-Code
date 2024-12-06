def get_input():
    with open("day6.txt", "r") as file:
        data = file.read().splitlines()

    return [[i for i in x] for x in data]


def get_next(facing, pos):
    match facing:
        case 0:
            return pos[0] - 1, pos[1]
        case 1:
            return pos[0], pos[1] + 1
        case 2:
            return pos[0] + 1, pos[1]
        case 3:
            return pos[0], pos[1] - 1
        

def get_start_pos(grid):
    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == "^":
                return i, j
            

def get_stepped(grid, start):
    facing = 0
    pos = tuple(start)

    steps = set()
    while True:
        steps.add(pos)

        next_pos = get_next(facing, pos)

        if not 0 <= next_pos[0] < len(grid) or not 0 <= next_pos[1] < len(grid[0]):
            break

        if grid[next_pos[0]][next_pos[1]] == "#":
            facing = (facing + 1) % 4
            next_pos = get_next(facing, pos)

        if grid[next_pos[0]][next_pos[1]] != "#":
            pos = next_pos

    return steps


def part1():
    grid = get_input()
    start = get_start_pos(grid)
    steps = get_stepped(grid, start)

    print(len(steps))


part1()


#--------


def check_loop(grid, start):
    facing = 0
    pos = tuple(start)

    steps = set()
    while True:
        to_add = pos + (facing,)

        if to_add in steps:
            return True
        
        steps.add(to_add)

        next_pos = get_next(facing, pos)

        if not 0 <= next_pos[0] < len(grid) or not 0 <= next_pos[1] < len(grid[0]):
            break

        if grid[next_pos[0]][next_pos[1]] == "#":
            facing = (facing + 1) % 4
            next_pos = get_next(facing, pos)

        if grid[next_pos[0]][next_pos[1]] != "#":
            pos = next_pos

    return False


def add_obstacles(grid):
    start = get_start_pos(grid)
    possible = get_stepped(grid, start)

    total = 0
    for i in possible:
        if i == start: continue

        grid[i[0]][i[1]] = "#"

        if check_loop(grid, start): total += 1

        grid[i[0]][i[1]] = "."

    return total


def part2():
    grid = get_input()
    total = add_obstacles(grid)

    print(total)


part2()
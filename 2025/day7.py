def get_input():
    with open("day7.txt", "r") as file:
        data = file.read().splitlines()

    return data


def step_beams(grid, prev_beams):
    num_split = 0
    new_beams = set()
    for x, y in prev_beams:
        if not 0 <= x < len(grid) or not 0 <= y < len(grid[0]):
            continue

        if grid[x + 1][y] == ".":
            new_beams.add((x + 1, y))
        else:
            num_split += 1
            new_beams.add((x + 1, y - 1))
            new_beams.add((x + 1, y + 1))

    return num_split, new_beams


def part1():
    grid = get_input()

    total = 0
    beams = set((i, j) for i, x in enumerate(grid) for j, k in enumerate(x) if k == "S")
    
    for _ in range(len(grid) - 1):
        num_split, beams = step_beams(grid, beams)
        total += num_split

    print(total)


part1()


#-----------


def simulate_particle(grid, x, y, cache):
    if cache[x][y] != 0:
        return cache[x][y]
    elif x >= len(grid) - 1:
        return 1
    
    if grid[x + 1][y] == ".":
        result = simulate_particle(grid, x + 1, y, cache)
    else:
        left = simulate_particle(grid, x + 1, y - 1, cache)
        right = simulate_particle(grid, x + 1, y + 1, cache)

        result = left + right

    cache[x][y] = result

    return result
    

def part2():
    grid = get_input()

    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == "S":
                start_x = i
                start_y = j

    cache = [[0 for _ in i] for i in grid]

    print(simulate_particle(grid, start_x, start_y, cache))


part2()
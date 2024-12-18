GRID_SIZE = 71
NUM_SIMULATE = 1024


def get_input():
    with open("day18.txt", "r") as file:
        data = file.read().splitlines()

    return [[int(i) for i in x.split(",")] for x in data]


def simulate_bytes(bytes):
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in bytes[:NUM_SIMULATE]:
        grid[i[1]][i[0]] = "#"

    return grid


def fill_neighbours(x, y, grid, dists, value):
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_x, new_y = x + i, y + j

            if i == 0 and j == 0 or i != 0 and j != 0: continue
            if not 0 <= new_x < len(grid) or not 0 <= new_y < len(grid[0]): continue
            
            if grid[new_x][new_y] == "." and dists[new_x][new_y] is None:
                dists[new_x][new_y] = value


def get_shortest_dist(grid):
    dists = [[None for _ in i] for i in grid]
    dists[0][0] = 0

    current = 0
    while dists[-1][-1] is None:
        for i, x in enumerate(dists):
            for j, k in enumerate(x):
                if k == current:
                    fill_neighbours(i, j, grid, dists, current + 1)

        current += 1

    return dists[-1][-1]


def part1():
    bytes = get_input()
    grid = simulate_bytes(bytes)

    dist = get_shortest_dist(grid)

    print(dist)


part1()


#-----------


def get_dists(grid):
    dists = [[None for _ in i] for i in grid]
    dists[0][0] = 0

    current = 0
    found_new = True
    while found_new and dists[-1][-1] is None:
        found_new = False
        for i, x in enumerate(dists):
            for j, k in enumerate(x):
                if k == current:
                    found_new = True
                    fill_neighbours(i, j, grid, dists, current + 1)

        current += 1

    return dists


def extract_path(dists):
    path = [(len(dists) - 1, len(dists[0]) - 1)]

    while path[-1] != (0, 0):
        x, y = path[-1]
        
        found = False
        for i in range(-1, 2):
            if found: break

            for j in range(-1, 2):
                new_x, new_y = x + i, y + j

                if i == 0 and j == 0 or i != 0 and j != 0: continue
                if not 0 <= new_x < len(dists) or not 0 <= new_y < len(dists[0]): continue

                if dists[new_x][new_y] == dists[x][y] - 1:
                    found = True
                    path.append((new_x, new_y))

                    break

    return path


def part2():
    bytes = get_input()

    best_path = []
    grid = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    t = 0
    for i in bytes:
        t += 1
        grid[i[1]][i[0]] = "#"

        if len(best_path) == 0 or (i[1], i[0]) in best_path:
            dists = get_dists(grid)

            if dists[-1][-1] is None:
                print(f"{i[0]},{i[1]}")
                break
            else:
                best_path = extract_path(dists)


part2()
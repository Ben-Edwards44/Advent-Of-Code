def get_input():
    with open("day23.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    return data


def get_neighbour_coords(grid, x, y):
    if grid[x][y] == ">":
        return [(x, y + 1)]
    elif grid[x][y] == "<":
        return [(x, y - 1)]
    elif grid[x][y] == "^":
        return [(x - 1, y)]
    elif grid[x][y] == "v":
        return [(x + 1, y)]
    
    coords = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0 or i != 0 and j != 0:
                continue

            new_x = x + i
            new_y = y + j

            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                if grid[new_x][new_y] != "#":
                    coords.append((new_x, new_y))

    return coords


def inverse_bfs(grid, steps, step):
    changed = False
    for i, x in enumerate(steps):
        for j, k in enumerate(x):
            if k == step:
                coords = get_neighbour_coords(grid, i, j)

                for new_x, new_y in coords:
                    if steps[new_x][new_y] < step - 1 or step == 1:
                        steps[new_x][new_y] = step + 1
                        changed = True

    return changed


def init_steps(grid):
    for i, x in enumerate(grid[0]):
        if x == ".":
            inx = i
            break

    steps = [[0 for _ in grid[0]] for _ in grid]
    steps[0][inx] = 1

    return steps


def get_end_inx(grid):
    for i, x in enumerate(grid[-1]):
        if x == ".":
            return i


def part1():
    grid = get_input()
    steps = init_steps(grid)

    end_inx = get_end_inx(grid)

    step = 1
    while inverse_bfs(grid, steps, step):
        step += 1

    total = steps[-1][end_inx] - 1

    print(total)


part1()


#-------


def replace(grid):
    new_grid = [[None for _ in grid[0]] for _ in grid]

    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == "#":
                char = "#"
            else:
                char = "."

            new_grid[i][j] = char

    return new_grid


def get_start_end_inx(grid):
    for i in range(len(grid[0])):
        if grid[0][i] == ".":
            start = i
        if grid[-1][i] == ".":
            end = i

    return start, end


def dfs(grid, x, y, path, end_x, end_y):
    global longest

    path = {i for i in path}

    if (end_x, end_y) in path:
        if longest == None or len(path) > longest:
            longest = len(path)
            print(longest - 1)
            return

    temp_coords = get_neighbour_coords(grid, x, y)
    act_coords = [i for i in temp_coords if i not in path]

    while len(act_coords) == 1:
        x = act_coords[0][0]
        y = act_coords[0][1]

        path.add((x, y))

        if (end_x, end_y) in path:
            if longest == None or len(path) > longest:
                longest = len(path)
                print(longest - 1)
                return

        temp_coords = get_neighbour_coords(grid, x, y)
        act_coords = [i for i in temp_coords if i not in path]

    for new_x, new_y in act_coords:
        path.add((new_x, new_y))

        dfs(grid, new_x, new_y, path, end_x, end_y)

        path.remove((new_x, new_y))


def can_be_two_ways(grid, steps, x, y):
    coords = get_neighbour_coords(grid, x, y)

    total = 0
    for new_x, new_y in coords:
        if steps[new_x][new_y] == 0:
            total += 1

    return total > 0


def new_inverse_bfs(grid, steps, step, two_ways):
    changed = False

    zero_this_step = set()

    for i, x in enumerate(steps):
        for j, k in enumerate(x):
            if k == step:
                coords = get_neighbour_coords(grid, i, j)

                total_new = 0
                for new_x, new_y in coords:
                    if steps[new_x][new_y] < step - 1 or step == 1:
                        if steps[new_x][new_y] == 0:
                            zero_this_step.add((new_x, new_y))

                        changed = True
                        total_new += 1
                        steps[new_x][new_y] = step + 1
                    elif steps[new_x][new_y] == step - 1:
                        #if there are two ways of reaching current cell
                        if (i, j) in two_ways:
                            #update anyway
                            steps[new_x][new_y] = step + 1
                            changed = True
                            total_new += 1
                    elif steps[new_x][new_y] == step + 1:
                        #there are 2 ways of reaching cell
                        if can_be_two_ways(grid, steps, new_x, new_y):
                            two_ways.add((new_x, new_y))

                    if (i, j) in two_ways:
                        two_ways.remove((i, j))

    return changed


def display(grid, steps):
    for i, x in enumerate(grid):
        line = ""
        for j, k in enumerate(x):
            if k == "#":
                line += k
            else:
                line += "O" if steps[i][j] > 0 else "."

        print(line)

    print()


def part2():
    global longest

    longest = None

    grid = get_input()
    new_grid = replace(grid)
 
    start, end = get_start_end_inx(new_grid)

    dfs(new_grid, 0, start, {(0, start)}, len(new_grid) - 1, end)

    total = longest - 1

    print(total)


part2()
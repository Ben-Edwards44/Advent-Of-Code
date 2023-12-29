def get_input():
    with open("day14.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    return data


def get_round_pos(col):
    prev_cube = 0
    num_round = 0

    round_pos = []
    for i, x in enumerate(col):
        if x == "#":
            prev_cube = i + 1
            num_round = 0
        elif x == "O":
            pos = prev_cube + num_round
            round_pos.append(pos)
            num_round += 1

    return round_pos


def get_total(grid):
    total = 0
    for i in range(len(grid[0])):
        col = [x[i] for x in grid]
        pos = get_round_pos(col)
        
        totals = [len(col) - x for x in pos]

        total += sum(totals)

    return total


def part1():
    grid = get_input()
    total = get_total(grid)

    print(total)


part1()


#------


def roll(col):
    prev_cube = 0
    num_round = 0

    round_pos = []
    new_col = [None for _ in col]

    for i, x in enumerate(col):
        if x == "#":
            prev_cube = i + 1
            num_round = 0
            new_col[i] = x
        elif x == "O":
            pos = prev_cube + num_round
            round_pos.append(pos)
            num_round += 1

            new_col[i] = "."
        else:
            new_col[i] = x

    for i in round_pos:
        new_col[i] = "O"

    return new_col


def back_roll(col):
    prev_cube = 0
    num_round = 0

    round_pos = []
    new_col = [None for _ in col]

    for r_inx, i in enumerate(reversed(col)):
        act_inx = len(col) - r_inx - 1

        if i == "#":
            prev_cube = r_inx + 1
            num_round = 0
            new_col[act_inx] = i
        elif i == "O":
            pos_from_end = prev_cube + num_round
            round_pos.append(pos_from_end)
            num_round += 1
            new_col[act_inx] = "."
        else:
            new_col[act_inx] = i

    for pos_from_end in round_pos:
        act_inx = len(new_col) - pos_from_end - 1
        new_col[act_inx] = "O"

    return new_col


def roll_n(grid):
    new_grid = [[None for _ in i] for i in grid]

    for i in range(len(grid[0])):
        col = [x[i] for x in grid]

        new_col = roll(col)
        
        for x, y in enumerate(new_col):
            new_grid[x][i] = y

    return new_grid


def roll_s(grid):
    new_grid = [[None for _ in i] for i in grid]

    for i in range(len(grid[0])):
        col = [x[i] for x in grid]

        new_col = back_roll(col)
        
        for x, y in enumerate(new_col):
            new_grid[x][i] = y

    return new_grid


roll_w = lambda grid: [roll(i) for i in grid]
roll_e = lambda grid: [back_roll(i) for i in grid]


def complete_cycle(grid):
    n = roll_n(grid)
    w = roll_w(n)
    s = roll_s(w)
    e = roll_e(s)

    return e


def new_total(final_pos, grid):
    total = 0
    col_length = len(grid)
    for i in final_pos:
        load = col_length - i[0]
        total += load

    return total


def hash_grid(grid):
    string = ""
    for i in grid:
        string += "".join(i)

    return string


def go_to_seen(grid):
    seen_set = {hash_grid(grid)}
    seen_list = [grid]

    while True:
        grid = complete_cycle(grid)

        hash = hash_grid(grid)

        if hash in seen_set:
            start = seen_list.index(grid)
            
            return seen_list, start

        seen_set.add(hash)
        seen_list.append(grid)


def get_final(pattern, start):
    num = 1000000000

    loopy_bit = num - start
    loop = pattern[start:]

    inx = loopy_bit % len(loop)

    return loop[inx]


def get_pos(grid):
    pos = []
    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == "O":
                pos.append((i, j))

    return pos


def part2():
    grid = get_input()

    pattern, start = go_to_seen(grid)

    final_pattern = get_final(pattern, start)

    pos = get_pos(final_pattern)
    total = new_total(pos, final_pattern)

    print(total)


part2()
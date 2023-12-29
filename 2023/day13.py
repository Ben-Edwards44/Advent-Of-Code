def get_input():
    with open("day13.txt", "r") as file:
        data = file.read()

    grids = data.split("\n\n")

    final = []
    for i, x in enumerate(grids):
        line = x.split("\n")
        if i == len(grids) - 1:
            final.append(line[:-1])
        else:
            final.append(line)

    return final


def is_row_reflect(grid, top_inx):
    bottom_inx = top_inx + 1

    while 0 <= top_inx and bottom_inx < len(grid):
        row1 = grid[top_inx]
        row2 = grid[bottom_inx]

        top_inx -= 1
        bottom_inx += 1

        if row1 != row2:
            return False
        
    return True


def is_col_reflect(grid, left_inx):
    right_inx = left_inx + 1

    while 0 <= left_inx and right_inx < len(grid[0]):
        col1 = [i[left_inx] for i in grid]
        col2 = [i[right_inx] for i in grid]

        left_inx -= 1
        right_inx += 1

        if col1 != col2:
            return False
        
    return True


def get_rows(grid):
    num_above = 0

    for i in range(len(grid) - 1):
        if is_row_reflect(grid, i):
            num_above += i + 1

    return num_above * 100


def get_cols(grid):
    left_sum = 0
    total = 0
    for i in range(len(grid[0]) - 1):
        left_sum += 1

        if is_col_reflect(grid, i):
            total += left_sum

    return total


def part1():
    grids = get_input()

    total = 0
    for i in grids:
        total += get_rows(i) + get_cols(i)

    print(total)


part1()


# ------


def get_num_diff(list1, list2):
    num = 0
    for i, x in zip(list1, list2):
        if i != x:
            num += 1

        if num > 1:
            #doesn't really matter if num > 1
            return num
        
    return num


def get_row_diff(grid, top_inx):
    bottom_inx = top_inx + 1

    num_diff = 0
    while 0 <= top_inx and bottom_inx < len(grid):
        row1 = grid[top_inx]
        row2 = grid[bottom_inx]

        top_inx -= 1
        bottom_inx += 1

        num_diff += get_num_diff(row1, row2)

        if num_diff > 1:
            return num_diff
        
    return num_diff


def get_col_diff(grid, left_inx):
    right_inx = left_inx + 1

    num_diff = 0
    while 0 <= left_inx and right_inx < len(grid[0]):
        col1 = [i[left_inx] for i in grid]
        col2 = [i[right_inx] for i in grid]

        left_inx -= 1
        right_inx += 1

        num_diff += get_num_diff(col1, col2)

        if num_diff > 1:
            return num_diff
        
    return num_diff


def new_rows(grid):
    num_above = 0

    for i in range(len(grid) - 1):
        if get_row_diff(grid, i) == 1:
            num_above += i + 1

    return num_above * 100


def new_cols(grid):
    left_sum = 0
    total = 0
    for i in range(len(grid[0]) - 1):
        left_sum += 1

        if get_col_diff(grid, i) == 1:
            total += left_sum

    return total


def part2():
    grids = get_input()

    total = 0
    for i in grids:
        total += new_rows(i) + new_cols(i)

    print(total)


part2()
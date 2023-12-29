def get_input():
    with open("day11.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    return [[x for x in i] for i in data]


def expand_col(list, col):
    for i in range(len(list)):
        list[i].insert(col, ".")


def expand_row(list, row):
    new_row = ["." for _ in range(len(list[0]))]
    list.insert(row, new_row)


def expand_list(list, rows, cols):
    new = [[x for x in i] for i in list]

    for i, x in enumerate(rows):
        expand_row(new, i + x)
    for i, x in enumerate(cols):
        expand_col(new, i + x)

    return new


def is_empty(list):
    for i in list:
        if i == "#":
            return False

    return True


def get_rows_cols(list):
    rows = []
    for i in range(len(list)):
        if is_empty(list[i]):
            rows.append(i)

    cols = []
    for i in range(len(list[0])):
        if is_empty([list[x][i] for x in range(len(list))]):
            cols.append(i)

    return rows, cols


def get_coords(list):
    coords = []
    for i, x in enumerate(list):
        for j, k in enumerate(x):
            if k == "#":
                coords.append((i, j))

    return coords


get_dist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_total(coords):
    total = 0

    for i in range(len(coords)):
        for x in range(i + 1, len(coords)):
            total += get_dist(coords[i], coords[x])

    return total


def part1():
    grid = get_input()
    r, c = get_rows_cols(grid)
    expanded = expand_list(grid, r, c)

    coords = get_coords(expanded)

    total = get_total(coords)

    print(total)


part1()


#------


def get_intercept_num(set, start, end):
    num = 0
    start_inx = min(start, end)
    end_inx = max(start, end)

    for i in range(start_inx, end_inx):
        if i in set:
            num += 1

    return num


def new_dist(a, b, rows, cols):
    og_dist = get_dist(a, b)

    r_int = get_intercept_num(rows, a[0], b[0])
    c_int = get_intercept_num(cols, a[1], b[1])

    tot = r_int + c_int

    return og_dist - tot + 1000000 * tot


def new_total(coords, rows, cols):
    total = 0

    for i in range(len(coords)):
        for x in range(i + 1, len(coords)):
            total += new_dist(coords[i], coords[x], rows, cols)

    return total


def part2():
    grid = get_input()
    r, c = get_rows_cols(grid)

    rows = {i for i in r}
    cols = {i for i in c}

    coords = get_coords(grid)

    total = new_total(coords, rows, cols)

    print(total)


part2()
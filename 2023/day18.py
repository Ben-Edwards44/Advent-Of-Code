def get_input():
    with open("day18.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    final = []
    for i in data:
        d, n, c = i.split(" ")

        final.append([d, int(n), c])

    return final


def get_outline(dirs):
    current_x = 0
    current_y = 0

    min_x = None
    min_y = None

    outline = []

    for dir, num, _ in dirs:
        for _ in range(num):
            if dir == "U":
                current_x -= 1
            elif dir == "D":
                current_x += 1
            elif dir == "L":
                current_y -= 1
            else:
                current_y += 1

            if min_x == None or min_x > current_x:
                min_x = current_x
            if min_y == None or min_y > current_y:
                min_y = current_y

            outline.append([current_x, current_y])

    return {(i[0] + abs(min_x) + 1, i[1] + abs(min_y) + 1) for i in outline}


def build_grid(outline):
    max_x = 0
    max_y = 0

    for x, y in outline:
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    return [[0 for _ in range(max_y + 4)] for _ in range(max_x + 4)]


def fill(grid, step, outline):
    done = False
    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == step:
                for y in range(-1, 2):
                    for m in range(-1, 2):
                        if y != 0 and m != 0 or y == m == 0:
                            continue

                        new_x = i + y
                        new_y = j + m

                        if not 0 <= new_x < len(grid) or not 0 <= new_y < len(grid[0]):
                            continue

                        if (new_x, new_y) not in outline and grid[new_x][new_y] == 0:
                            grid[new_x][new_y] = step + 1
                            done = True

    return done


def fill_grid(grid, outline):
    grid[-1][-1] = 1
    step = 1

    while fill(grid, step, outline):
        step += 1


def get_total(grid):
    total = 0
    for i in grid:
        total += i.count(0)

    return total


def part1():
    dirs = get_input()
    outline = get_outline(dirs)
    grid = build_grid(outline)

    fill_grid(grid, outline)

    total = get_total(grid)

    print(total)


part1()


#----------


def get_inst(dirs):
    final = []
    for _, _, colour in dirs:
        colour = colour[2:-1]

        dir = int(colour[-1])
        num = int(colour[:-1], 16)

        final.append([dir, num])

    return final


def get_coords(inst):
    outline = []
    x_coords = []

    current_x = 0
    current_y = 0

    for dir, num in inst:
        if dir == 3:
            current_x += num
            x_coords.append(current_x)
        elif dir == 1:
            current_x -= num
            x_coords.append(current_x)
        elif dir == 2:
            current_y -= num
        else:
            current_y += num

        outline.append([current_x, current_y])

    return outline, x_coords


def get_corresponding_coords(x_coord, outline):
    y_coords = []

    for i, x in enumerate(outline):
        a = outline[i - 1]

        if a[1] == x[1]:
            if (a[0] <= x_coord <= x[0] or x[0] <= x_coord <= a[0]) and a[0] != x[0]:
                y_coords.append(a[1])

    return y_coords


def get_x_coords(y_coord, outline):
    x_coords = []

    for i, x in enumerate(outline):
        a = outline[i - 1]

        if a[0] == x[0]:
            if (a[1] <= y_coord <= x[1] or x[1] <= y_coord <= a[1]) and a[1] != x[1]:
                x_coords.append(a[0])

    return x_coords


def cross_even_times(coords, coord):
    coords.sort()

    inx = len(coords)
    for i, j in enumerate(coords):
        if j > coord:
            inx = i
            break

    before = coords[:inx]
    after = coords[inx:]

    return len(before) % 2 == 0 or len(after) % 2 == 0


def is_in_shape(x, y, y_coords, outline):
    x_coords = get_x_coords(y, outline)

    if x in x_coords or y in y_coords:
        return True
    else:
        return not cross_even_times(x_coords, x)


def get_incut_width(y_coords, x, outline):
    y_coords.sort()

    width = 0
    for i in range(len(y_coords)):
        if i < len(y_coords) - 1 and not is_in_shape(x, y_coords[i] + 1, y_coords, outline):
            width += y_coords[i + 1] - y_coords[i] - 1

    return width


def get_area(x_coords, outline):
    area = 0
    for i, x in enumerate(x_coords):
        current_y = get_corresponding_coords(x, outline)
        width = max(current_y) - min(current_y) + 1
        width -= get_incut_width(current_y, x, outline)

        area += width

        if i < len(x_coords) - 1:
            start_x = x - 1
            end_x = x_coords[i + 1] + 1

            height = start_x - end_x + 1

            below_y = get_corresponding_coords(x - 1, outline)

            if len(below_y) == 0:
                continue

            width = max(below_y) - min(below_y) + 1
            width -= get_incut_width(below_y, x - 1, outline)

            area += width * height

    return area


def offset(x_coords, outline):
    min_x = abs(min(x_coords))

    for i in range(len(x_coords)):
        x_coords[i] += min_x
    for i in range(len(outline)):
        outline[i][0] += min_x


def part2():
    dirs = get_input()
    inst = get_inst(dirs)

    outline, x_coords = get_coords(inst)

    x_coords = list(set(x_coords))
    x_coords.sort(reverse=True)

    offset(x_coords, outline)

    total = get_area(x_coords, outline)

    print(total)


part2()
def get_input():
    with open("day12.txt", "r") as file:
        data = file.read().splitlines()

    return data


def check_cell(copy, map, x, y, region_type, current):
    perims = []
    for x_step in range(-1, 2):
        for y_step in range(-1, 2):
            if x_step != 0 and y_step != 0 or x_step == 0 and y_step == 0: continue

            new_x = x + x_step
            new_y = y + y_step

            perim_to_store = ((x, y), (new_x, new_y))

            if not 0 <= new_x < len(map) or not 0 <= new_y < len(map[0]):
                perims.append(perim_to_store)
                continue

            if map[new_x][new_y] != region_type:
                perims.append(perim_to_store)
            elif type(copy[new_x][new_y]) != int:
                copy[new_x][new_y] = current + 1  

    return perims


def explore_region(map, start_x, start_y):
    type = map[start_x][start_y]
    copy = [[i for i in x] for x in map]

    copy[start_x][start_y] = 0
    current = 0

    area = 0
    perims = []

    found_new = True
    while found_new:
        found_new = False
        for i, x in enumerate(copy):
            for j, k in enumerate(x):
                if k != current: continue

                area += 1

                cell_borders = check_cell(copy, map, i, j, type, current)
                perims += cell_borders

                found_new = True

        current += 1

    return area, perims, copy


def is_new_region(copies, x, y):
    for i in copies:
        if type(i[x][y]) == int:
            return False
        
    return True


part1_price = lambda area, perims: area * len(perims)


def get_price(price_func):
    map = get_input()

    total = 0
    copies = []
    for i in range(len(map)):
        for x in range(len(map[0])):
            if is_new_region(copies, i, x):
                area, perims, copy = explore_region(map, i, x)

                copies.append(copy)

                total += price_func(area, perims)

    return total


def part1():
    total = get_price(part1_price)

    print(total)


part1()


#--------


def are_same_side(a, b):
    if a[0] == b[0]:
        return abs(a[1] - b[1]) == 1
    elif a[1] == b[1]:
        return abs(a[0] - b[0]) == 1
    else:
        return False
    

on_hor_side = lambda a, b: a[0] == b[0] and abs(a[1] - b[1]) == 1
on_vert_side = lambda a, b: a[1] == b[1] and abs(a[0] - b[0]) == 1
    

def check_side(perims, start, on_side_func):
    side = [start]

    on_side = False
    added = True
    while added:
        added = False

        for i, x in enumerate(perims):
            if x in side: continue

            start_in, start_out = side[0]
            end_in, end_out = side[-1]

            if on_side_func(x[0], start_in) and on_side_func(x[1], start_out):
                side.insert(0, x)
                added = True
            elif on_side_func(x[0], end_in) and on_side_func(x[1], end_out):
                side.append(x)
                added = True

            if added:
                inx = i
                break

        if added:
            perims.pop(inx)
            on_side = True

    return on_side
    

def get_sides(perims):
    sides = 0
    while len(perims) > 0:
        is_hor = check_side(perims, perims[0], on_hor_side)
        if not is_hor: check_side(perims, perims[0], on_vert_side)

        sides += 1
        perims.pop(0)

    return sides


part2_price = lambda area, perims: area * get_sides(perims)


def part2():
    total = get_price(part2_price)

    print(total)


part2()
def get_input():
    with open("day5.txt", "r") as file:
        data = file.read()

    fresh, available = data.split("\n\n")

    available = [int(i) for i in available.splitlines()]
    fresh = [[int(x) for x in i.split("-")] for i in fresh.splitlines()]

    return fresh, available


def is_fresh(id, fresh):
    for l, u in fresh:
        if l <= id <= u:
            return True
        
    return False


def part1():
    fresh, available = get_input()

    total = 0
    for i in available:
        if is_fresh(i, fresh):
            total += 1

    print(total)


part1()


#---------


def expand_range(current_range, other_ranges):
    c_l, c_u = current_range

    disjoint = []
    for l, u in other_ranges:
        if c_l <= l <= c_u:
            c_u = max(u, c_u)
        elif c_l <= u <= c_u:
            c_l = min(l, c_l)
        elif l <= c_l and u >= c_u:
            c_u = u
            c_l = l
        else:
            disjoint.append([l, u])

    return [c_l, c_u], disjoint


def fully_expand(fresh, inx):
    other_ranges = []
    current_range = fresh[inx]
    new_disjoint = fresh[:inx] + fresh[inx + 1:]

    while new_disjoint != other_ranges:
        other_ranges = new_disjoint
        current_range, new_disjoint = expand_range(current_range, other_ranges)

    return current_range, other_ranges


def get_total_range(fresh):
    total_range = []

    while len(fresh) > 0:
        expanded, fresh = fully_expand(fresh, 0)
        total_range.append(expanded)

    return total_range


def part2():
    fresh, _ = get_input()
    total_range = get_total_range(fresh)

    total = 0
    for l, u in total_range:
        total += u - l + 1

    print(total)


part2()
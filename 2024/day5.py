def get_input():
    with open("day5.txt", "r") as file:
        inst, pages = file.read().split("\n\n")

    inst = [[int(i) for i in x.split("|")] for x in inst.split("\n")]
    pages = [[int(i) for i in x.split(",")] for x in pages.split("\n")[:-1]]

    return inst, pages


def check_rule(pages, before, after):
    b_inx = None
    a_inx = None

    for i, x in enumerate(pages):
        if x == before:
            b_inx = i
        elif x == after:
            a_inx = i

    return (b_inx is None or a_inx is None) or b_inx < a_inx


def check_pages(pages, rules):
    for i in rules:
        if not check_rule(pages, i[0], i[1]):
            return False
        
    return True


def part1():
    inst, pages = get_input()

    total = 0
    for i in pages:
        if check_pages(i, inst):
            total += i[(len(i) - 1) // 2]

    print(total)


part1()


#----


def get_position(page, rules, cache):
    if page in cache:
        return cache[page]

    position = 0
    for before, after in rules:
        if page == before:
            new_pos = get_position(after, rules, cache) + 1
            position = max(position, new_pos)

    cache[page] = position

    return position


def re_order(pages, rules):
    relevant_rules = tuple(tuple(i) for i in rules if i[0] in pages and i[1] in pages)

    ordered = [None for _ in pages]
    for i in pages:
        inx = len(ordered) - get_position(i, relevant_rules, {}) - 1
        ordered[inx] = i

    return ordered


def part2():
    inst, pages = get_input()
    incorrect = [i for i in pages if not check_pages(i, inst)]

    total = 0
    for i in incorrect:
        correct = re_order(i, inst)
        total += correct[(len(correct) - 1) // 2]

    print(total)


part2()
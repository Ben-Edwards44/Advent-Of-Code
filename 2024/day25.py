def get_input():
    with open("day25.txt", "r") as file:
        data = file.read().strip()

    blocks = data.split("\n\n")

    keys_locks = []
    for i in blocks:
        keys_locks.append(i.splitlines())

    return keys_locks


def parse_keys_locks(keys_locks):
    keys = []
    locks = []
    for i in keys_locks:
        cols = [[i[x][y] for x in range(len(i))] for y in range(len(i[0]))]
        heights = [x.count("#") - 1 for x in cols]

        if i[0][0] == "#":
            locks.append(heights)
        else:
            keys.append(heights)

    return keys, locks


def fits(key, lock):
    for i, x in zip(key, lock):
        if i + x > 5: return False

    return True


def part1():
    keys_locks = get_input()
    keys, locks = parse_keys_locks(keys_locks)

    total = 0
    for i in keys:
        for x in locks:
            if fits(i, x): total += 1

    print(total)


part1()
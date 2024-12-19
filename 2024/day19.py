def get_input():
    with open("day19.txt", "r") as file:
        data = file.read().strip()

    got, want = data.split("\n\n")

    return got.split(", "), want.splitlines()


def is_possible(design, got_towels):
    if design == "": return True

    for i in got_towels:
        if len(i) <= len(design) and i == design[:len(i)]:
            possible = is_possible(design[len(i):], got_towels)

            if possible: return True

    return False


def part1():
    got, want = get_input()

    total = 0
    for i in want:
        if is_possible(i, got): total += 1

    print(total)


part1()


#---------


def get_ways(design, got_towels, cache):
    if design == "": return 1
    elif design in cache: return cache[design]

    total_ways = 0
    for i in got_towels:
        if len(i) <= len(design) and i == design[:len(i)]:
            ways = get_ways(design[len(i):], got_towels, cache)
            total_ways += ways

    cache[design] = total_ways

    return total_ways


def part2():
    got, want = get_input()

    total = 0
    cache = {}
    for i in want:
        total += get_ways(i, got, cache)

    print(total)


part2()
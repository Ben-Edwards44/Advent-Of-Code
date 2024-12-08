from math import gcd


def get_input():
    with open("day8.txt", "r") as file:
        data = file.read().splitlines()

    return data


def get_vector(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    return dx, dy


def find_antinodes(pos, freqs):
    freq = freqs[pos[0]][pos[1]]

    antinodes = []
    for i, x in enumerate(freqs):
        for j, k in enumerate(x):
            if i == pos[0] and j == pos[1] or freq != k: continue

            vect = get_vector(pos, (i, j))
            antinode = (pos[0] + vect[0], pos[1] + vect[1])

            if 0 <= antinode[0] < len(freqs) and 0 <= antinode[1] < len(freqs[1]):
                antinodes.append(antinode)

    return antinodes


def part1():
    freqs = get_input()

    all_antinodes = []
    for i, x in enumerate(freqs):
        for j, k in enumerate(x):
            if k != ".":
                all_antinodes += find_antinodes((i, j), freqs)

    print(len(set(all_antinodes)))


part1()


#-------


def get_simplest_vector(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    hcf = gcd(dx, dy)

    return dx // hcf, dy // hcf


def find_harmonic_antinodes(pos, freqs):
    freq = freqs[pos[0]][pos[1]]

    antinodes = []
    for i, x in enumerate(freqs):
        for j, k in enumerate(x):
            if i == pos[0] and j == pos[1] or freq != k: continue

            vect = get_simplest_vector(pos, (i, j))
            antinode = (i + vect[0], j + vect[1])

            while 0 <= antinode[0] < len(freqs) and 0 <= antinode[1] < len(freqs[1]):
                antinodes.append(antinode)
                antinode = (antinode[0] + vect[0], antinode[1] + vect[1])

    return antinodes


def part2():
    freqs = get_input()

    all_antinodes = []
    for i, x in enumerate(freqs):
        for j, k in enumerate(x):
            if k != ".":
                all_antinodes += find_harmonic_antinodes((i, j), freqs)

    print(len(set(all_antinodes)))


part2()
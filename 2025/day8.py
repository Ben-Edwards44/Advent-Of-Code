def get_input():
    with open("day8.txt", "r") as file:
        data = file.read().splitlines()

    return [tuple(int(i) for i in x.split(",")) for x in data]


def get_dists(coords):
    dists = []
    for i, x in enumerate(coords):
        for j in coords[:i]:
            dist_sq = (x[0] - j[0])**2 + (x[1] - j[1])**2 + (x[2] - j[2])**2
            to_add = (x, j, dist_sq)
            dists.append(to_add)

    return sorted(dists, key=lambda x: x[2])


def add_to_circuit(circuits, a, b):
    joined = []
    to_rem = []
    for i, x in enumerate(circuits):
        if a in x:
            joined += x
            to_rem.append(i)
        elif b in x:
            joined += x
            to_rem.append(i)

    new_circuits = [x for i, x in enumerate(circuits) if i not in to_rem]
    new_circuits.append(joined)

    return new_circuits


def part1():
    coords = get_input()
    dists = get_dists(coords)

    circuits = [[i] for i in coords]

    for a, b, _ in dists[:1000]:
        circuits = add_to_circuit(circuits, a, b)

    circuits.sort(key=lambda x: len(x), reverse=True)

    total = 1
    for i in circuits[:3]:
        total *= len(i)

    print(total)


part1()


#-------


def part2():
    coords = get_input()
    dists = get_dists(coords)

    circuits = [[i] for i in coords]

    i = 0
    while len(circuits) > 1:
        a, b, _ = dists[i]
        circuits = add_to_circuit(circuits, a, b)
        i += 1

    print(a[0] * b[0])


part2()
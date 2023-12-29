def get_input():
    with open("day5.txt", "r") as file:
        data = file.read()[:-1]

    sections = data.split("\n\n")

    all = [i.split("\n") for i in sections]

    map = []
    for i in all:
        if i[0][:5] == "seeds":
            _, line = i[0].split(": ")
            map.append([int(j) for j in line.split(" ")])
        else:
            line = i[1:]
            splitted = [[int(j) for j in x.split(" ")] for x in line]
            map.append(splitted)

    return map


def get_dest(source, map, map_inx):
    for dest_start, source_start, range in map[map_inx]:
        pos = source - source_start

        if 0 <= pos < range:
            return dest_start + pos
        
    return source
        

def get_location_num(seed_inx, map):
    current = map[0][seed_inx]

    for i in range(1, len(map)):
        current = get_dest(current, map, i)

    return current


def part1():
    map = get_input()
    
    locations = []
    for i in range(len(map[0])):
        locations.append(get_location_num(i, map))

    print(min(locations))


part1()


#--------------


def get_source(dest, map, map_inx):
    for dest_start, source_start, range in map[map_inx]:
        pos = dest - dest_start

        if 0 <= pos < range:
            return source_start + pos
        
    return dest


def work_backwards(location, map):
    current = location

    for i in range(len(map) - 1, 0, -1):
        current = get_source(current, map, i)

    return current


def get_location_equiv(bound, map, layer_inx):
    current = bound

    for i in range(layer_inx + 1, len(map)):
        current = get_dest(current, map, i)

    return current


def get_layer_bounds(map, layer_inx):
    bounds = []
    for i in map[layer_inx]:
        bounds.append(i[0])
        bounds.append(i[0] + i[2])

    return [get_location_equiv(i, map, layer_inx) for i in bounds]


def get_all_location_bounds(map):
    bounds = []

    for i in range(len(map) - 1, 0, -1):
        bounds += get_layer_bounds(map, i)

    return bounds


def loop_bounds(map, bounds):
    for i, x in enumerate(bounds):
        if i == 0 or x != bounds[i - 1]:
            seed = work_backwards(x, map)

            if valid_seed(seed, map):
                return x
            

def valid_seed(seed, map):
    seeds = map[0]

    for i in range(0, len(seeds), 2):
        start = seeds[i]
        r = seeds[i + 1]

        if start <= seed < start + r:
            return True
        
    return False


def part2():
    map = get_input()

    bounds = get_all_location_bounds(map)
    bounds.sort()

    result = loop_bounds(map, bounds)

    print(result)


part2()
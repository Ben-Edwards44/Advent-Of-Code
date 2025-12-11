def get_input():
    with open("day11.txt", "r") as file:
        data = file.read().splitlines()

    connections = {}
    for i in data:
        start, end = i.split(": ")
        connections[start] = end.split(" ")

    return connections


def dfs(current, target, connections, cache):
    if current == target:
        return 1
    elif current in cache:
        return cache[current]
    
    total = 0
    for i in connections[current]:
        total += dfs(i, target, connections, cache)

    cache[current] = total

    return total


def part1():
    connections = get_input()

    print(dfs("you", "out", connections, {}))


part1()


#----------


def new_dfs(current, target, connections, cache, done_fft, done_dac):
    if current == "fft":
        done_fft = True
    elif current == "dac":
        done_dac = True

    cache_key = f"{current}{done_fft}{done_dac}"
    
    if current == target:
        if done_fft and done_dac:
            return 1
        else:
            return 0
    elif cache_key in cache:
        return cache[cache_key]
    
    total = 0
    for i in connections[current]:
        total += new_dfs(i, target, connections, cache, done_fft, done_dac)

    cache[cache_key] = total

    return total


def part2():
    connections = get_input()

    print(new_dfs("svr", "out", connections, {}, False, False))


part2()
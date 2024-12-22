NUM_KEYPAD = (("7", "8", "9"),
              ("4", "5", "6"),
              ("1", "2", "3"),
              (" ", "0", "A"))


DIR_KEYPAD = ((" ", "^", "A"),
              ("<", "v", ">"))


def get_input():
    with open("day21.txt", "r") as file:
        data = file.read().splitlines()

    return data


def get_paths(start_key, end_key, keypad):
    if start_key == end_key: return [""]

    for i, x in enumerate(keypad):
        for j, k in enumerate(x):
            if k == start_key:
                start_x = i
                start_y = j
            elif k == end_key:
                end_x = i
                end_y = j

    all_paths = []
    if start_x < end_x:
        new_x = start_x + 1
        new_y = start_y
        
        if keypad[new_x][new_y] != " ":
            paths = get_paths(keypad[new_x][new_y], keypad[end_x][end_y], keypad)
            all_paths += ["v" + i for i in paths]
    elif start_x > end_x:
        new_x = start_x - 1
        new_y = start_y
        
        if keypad[new_x][new_y] != " ":
            paths = get_paths(keypad[new_x][new_y], keypad[end_x][end_y], keypad)
            all_paths += ["^" + i for i in paths]

    if start_y < end_y:
        new_x = start_x
        new_y = start_y + 1
        
        if keypad[new_x][new_y] != " ":
            paths = get_paths(keypad[new_x][new_y], keypad[end_x][end_y], keypad)
            all_paths += [">" + i for i in paths]
    elif start_y > end_y:
        new_x = start_x
        new_y = start_y - 1
        
        if keypad[new_x][new_y] != " ":
            paths = get_paths(keypad[new_x][new_y], keypad[end_x][end_y], keypad)
            all_paths += ["<" + i for i in paths]

    return all_paths


def press(robot, max_robots, start_key, end_key, cache):
    if robot >= max_robots:
        return 1

    cache_key = (robot, start_key, end_key)
    if cache_key in cache:
        return cache[cache_key]
    
    paths = get_paths(start_key, end_key, DIR_KEYPAD)  #not including final A

    best = None
    for path in paths:
        current_len = 0
        prev_key = "A"

        for key in path:
            current_len += press(robot + 1, max_robots, prev_key, key, cache)
            prev_key = key

        current_len += press(robot + 1, max_robots, prev_key, "A", cache)

        if best is None or current_len < best: best = current_len

    cache[cache_key] = best

    return best


def get_num_path_len(num_path, max_robots):
    #num_path must include As
    prev = "A"
    cache = {}
    total_length = 0
    for key in num_path:
        total_length += press(0, max_robots, prev, key, cache)
        prev = key

    return total_length


def get_all_num_paths(num_code):
    paths = [""]
    prev = "A"
    for num_key in num_code:
        paths_to_key = get_paths(prev, num_key, NUM_KEYPAD)
        prev = num_key

        new_paths = []
        for prev_paths in paths:
            for add_path in paths_to_key:
                new_paths.append(prev_paths + add_path + "A")

        paths = [i for i in new_paths]

    return paths


def get_sequence_len(num_code, max_robots):
    initial_paths = get_all_num_paths(num_code)

    best_len = None
    for i in initial_paths:
        length = get_num_path_len(i, max_robots)

        if best_len is None or length < best_len: best_len = length

    return best_len


def part1():
    codes = get_input()

    total = 0
    for code in codes:
        int_part = int(code[:-1])
        seq_len = get_sequence_len(code, 2)

        total += int_part * seq_len

    print(total)


part1()


#--------


def part2():
    codes = get_input()

    total = 0
    for code in codes:
        int_part = int(code[:-1])
        seq_len = get_sequence_len(code, 25)

        total += int_part * seq_len

    print(total)


part2()
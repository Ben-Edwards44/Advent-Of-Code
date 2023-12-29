def get_input():
    with open("day12.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    springs = []
    nums = []
    for i in data:
        s, n = i.split(" ")

        springs.append(s)
        nums.append([int(x) for x in n.split(",")])

    return springs, nums


def check_valid(string, nums):
    num_inx = 0
    current = 0

    for i in string:
        if i == "#":
            current += 1
        elif i == ".":
            if current > 0:
                if num_inx >= len(nums) or current != nums[num_inx]:
                    return False, False
                else:
                    current = 0
                    num_inx += 1
        elif i == "?":
            return False, True
                        
    if num_inx == len(nums) - 1:
        valid = current == nums[num_inx]

        return True, valid
    elif num_inx < len(nums) - 1:
        return True, False
    else:
        return True, current == 0


def backtrack(current_string, nums):
    global total

    current_string = [i for i in current_string]

    done, valid = check_valid(current_string, nums)

    if done and valid:
        total += 1
        return
    elif not valid:
        return
    
    inx = 0
    for i, x in enumerate(current_string):
        if x == "?":
            inx = i
            break

    possible = []

    need_hash = sum(nums) - current_string.count("#")
    
    if need_hash > 0:
        possible.append("#")
    if current_string.count("?") > need_hash:
        possible.append(".")

    for i in possible:
        current_string[inx] = i

        backtrack(current_string, nums)

        current_string[inx] = "?"


def part1():
    global total

    string, nums = get_input()

    overall = 0
    for i, x in zip(string, nums):
        total = 0
        backtrack(i, x)
        overall += total

    print(overall)


part1()


#------


def new_backtrack(current_string, nums):
    global total, done_cache

    current_string = [i for i in current_string]

    key = get_key(current_string, nums)
    if key in done_cache.keys():
        total += done_cache[key]
        return

    done, valid = check_valid(current_string, nums)

    if done and valid:
        total += 1
        return
    elif not valid:
        return
    
    if "." in current_string:
        groups = get_groups("".join(current_string))
        total += work_backwards(groups, nums, len(groups) - 1, {tuple() : 1})
        return
    
    inx = 0
    for i, x in enumerate(current_string):
        if x == "?":
            inx = i
            break

    possible = []

    need_hash = sum(nums) - current_string.count("#")
        
    if need_hash > 0:
        possible.append("#")
    if current_string.count("?") > need_hash:
        possible.append(".")

    before = total
    for i in possible:
        current_string[inx] = i

        new_backtrack(current_string, nums)

        current_string[inx] = "?"
    after = total

    done_cache[key] = after - before


def get_total(string, nums):
    global total, done_cache

    total = 0

    new_backtrack(string, nums)

    key = get_key(list(string), nums)
    done_cache[key] = total

    return total


def work_backwards(groups, nums, inx, prev_cache):
    if inx == -1:
        key = tuple(reversed(nums))

        if key in prev_cache.keys():
            return prev_cache[tuple(reversed(nums))]
        else:
            #no combinations
            return 0
    
    group = groups[inx]
    g_max = round(len(group) / 2)

    new_cache = {}
    for path, comb in prev_cache.items():
        current_nums = []
        num_inx = len(nums) - len(path)

        while num_inx >= 0 and len(current_nums) <= g_max + 1:
            local_combs = get_total(group, list(reversed(current_nums)))

            if local_combs > 0:
                path_to = path + tuple(current_nums)

                if path_to in new_cache.keys():
                    new_cache[path_to] += local_combs * comb
                else:
                    new_cache[path_to] = local_combs * comb

            num_inx -= 1
            if num_inx >= 0:
                current_nums.append(nums[num_inx])

    return work_backwards(groups, nums, inx - 1, new_cache)


get_groups = lambda string: [i for i in string.split(".") if i != ""]
get_key = lambda current_string, nums: f"{''.join(current_string)}.{str(nums)}"


def update_string(string, nums):
    string = [i for i in string]
    nums = [i for i in nums]

    og_s = [i for i in string]
    og_n = [i for i in nums]

    for _ in range(4):
        string.append("?")
        string += og_s

        nums += og_n

    return string, nums


def find_combs(string, nums):
    s, n = update_string(string, nums)

    g = get_groups("".join(s))
    return work_backwards(g, n, len(g) - 1, {tuple() : 1})


def part2():
    global done_cache

    string, nums = get_input()

    total = 0
    for i, x in zip(string, nums):
        done_cache = {}
        add = find_combs(i, x)
        total += add

    print(total)


part2()
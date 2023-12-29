def get_input():
    with open("day4.txt", "r") as file:
        data = file.read()

    return data.split("\n")[:-1]


def get_nums(string):
    nums = []
    current_num = ""

    for i in string:
        if i != " ":
            current_num += i
        else:
            if current_num != "":
                nums.append(int(current_num))
                current_num = ""

    nums.append(int(current_num))

    return nums


def build_lists(data):
    lists = []

    for i in data:
        _, line = i.split(": ")
        win, act = line.split(" | ")

        win_list = get_nums(win)
        act_list = get_nums(act)

        lists.append([win_list, act_list])

    return lists


def get_points(win_list, act_list):
    points = 0

    for i in win_list:
        if i in act_list:
            if points > 0:
                points *= 2
            else:
                points = 1

    return points


def part1():
    data = get_input()
    lists = build_lists(data)

    total = 0
    for w, a in lists:
        total += get_points(w, a)

    print(total)


part1()


#---------


def get_num_match(win_list, act_list):
    num = 0

    for i in win_list:
        if i in act_list:
            num += 1

    return num

    
def get_win_inxs(card_inx, lists):
    w, a = lists[card_inx]
    num = get_num_match(w, a)

    return [card_inx + i for i in range(1, num + 1)]


def main(result_list, lists):
    #dynamic programming
    for i in range(len(result_list) - 1, -1, -1):
        win_inxs = get_win_inxs(i, lists)

        for x in win_inxs:
            cached = result_list[x]

            for j in cached:
                result_list[i].append(j)

    return result_list


def part2():
    data = get_input()
    lists = build_lists(data)

    totals = [0 for _ in range(len(lists))]

    result_list = [[i] for i in range(len(lists))]

    main(result_list, lists)

    for i in result_list:
        for x in i:
            totals[x] += 1

    print(sum(totals))


part2()
def get_input():
    with open("day1.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    return data


def get_first_int(string):
    for inx, i in enumerate(string):
        if i in "0123456789":
            return i, inx
        
    return None, len(string) + 1
        

def part1():
    data = get_input()

    total = 0
    for i in data:
        dig1, _ = get_first_int(i)
        dig2, _ = get_first_int(i[::-1])

        total += int(dig1 + dig2)

    print(total)


part1()
# --------


def get_spell(string, reverse):
    nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    if reverse:
        inxs = range(len(string) - 1, -1, -1)
    else:
        inxs = range(len(string))

    for i in inxs:
        if reverse:
            act_inx = len(string) - 1 - i
        else:
            act_inx = i

        three_letter = ""
        four_letter = ""
        five_letter = ""

        for x in range(5):
            if i + x >= len(string):
                break

            char = string[i + x]

            if x < 3:
                three_letter += char
            if x < 4:
                four_letter += char
            if x < 5:
                five_letter += char

        if three_letter in nums:
            return str(nums.index(three_letter) + 1), act_inx
        elif four_letter in nums:
            return str(nums.index(four_letter) + 1), act_inx
        elif five_letter in nums:
            return str(nums.index(five_letter) + 1), act_inx
        
    return None, len(string) + 1
        

def part2():
    data = get_input()

    total = 0
    for i in data:
        dig1, inx = get_first_int(i)
        spell1, s_inx = get_spell(i, False)

        if s_inx < inx:
            dig1 = spell1

        dig2, inx = get_first_int(i[::-1])
        spell2, s_inx = get_spell(i, True)

        if s_inx < inx:
            dig2 = spell2

        total += int(dig1 + dig2)

    print(total)


part2()
def get_input():
    with open("day4.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    return data


def get_run(wordsearch, x, y, dx, dy):
    word = ""
    for i in range(4):
        inx1 = x + i * dx
        inx2 = y + i * dy

        if not 0 <= inx1 < len(wordsearch) or not 0 <= inx2 < len(wordsearch[0]):
            continue

        word += wordsearch[inx1][inx2]

    return word


get_surrounding = lambda wordsearch, x, y: [get_run(wordsearch, x, y, i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]


def part1():
    wordsearch = get_input()

    total = 0
    for i, x in enumerate(wordsearch):
        for j, k in enumerate(x):
            if k == "X":
                total += get_surrounding(wordsearch, i, j).count("XMAS")

    print(total)


part1()


#------


def check_diag(wordsearch, x, y, dy):
    d = []
    for i in range(-1, 2):
        inx1 = x + i
        inx2 = y + i * dy

        if not 0 <= inx1 < len(wordsearch) or not 0 <= inx2 < len(wordsearch[0]):
            return False
        
        d.append(wordsearch[inx1][inx2])

    return d[1] == "A" and sorted([d[0], d[2]]) == ["M", "S"]


check_cross = lambda wordsearch, x, y: check_diag(wordsearch, x, y, 1) and check_diag(wordsearch, x, y, -1)


def part2():
    wordsearch = get_input()

    total = 0
    for i, x in enumerate(wordsearch):
        for j, k in enumerate(x):
            if k == "A":
                if check_cross(wordsearch, i, j):
                    total += 1

    print(total)


part2()
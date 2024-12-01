def get_input():
    with open("day1.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    l1 = []
    l2 = []
    for i in data:
        n1, n2 = [int(x) for x in i.split("   ")]

        l1.append(n1)
        l2.append(n2)

    return l1, l2


def part1():
    l1, l2 = get_input()

    l1.sort()
    l2.sort()

    total = sum([abs(i - x) for i, x in zip(l1, l2)])

    print(total)


part1()

#-------
def get_occurences(l):
    occurences = {}
    for i in l:
        if i in occurences:
            occurences[i] += 1
        else:
            occurences[i] = 1

    return occurences


def part2():
    l1, l2 = get_input()
    
    occurences = get_occurences(l2)

    similarity = 0
    for i in l1:
        if i in occurences:
            o = occurences[i]
        else:
            o = 0

        similarity += i * o

    print(similarity)


part2()
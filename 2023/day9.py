def get_input():
    with open("day9.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    return [[int(x) for x in i.split(" ")] for i in data]


def extrapolate(sequence):
    if sequence.count(0) == len(sequence):
        return 0
    
    diffs = []
    for i, x in enumerate(sequence):
        if i > 0:
            diffs.append(x - sequence[i - 1])

    added_num = extrapolate(diffs)
    new_value = added_num + sequence[-1]

    return new_value


def part1():
    sequences = get_input()

    total = 0
    for i in sequences:
        total += extrapolate(i)

    print(total)


part1()


#------


def back_extrapolate(sequence):
    if sequence.count(0) == len(sequence):
        return 0
    
    diffs = []
    for i, x in enumerate(sequence):
        if i > 0:
            diffs.append(x - sequence[i - 1])

    added_num = back_extrapolate(diffs)
    new_value = sequence[0] - added_num

    return new_value


def part2():
    sequences = get_input()

    back_extrapolate(sequences[2])

    total = 0
    for i in sequences:
        total += back_extrapolate(i)

    print(total)

#f - x = diff
#x = f - diff
part2()
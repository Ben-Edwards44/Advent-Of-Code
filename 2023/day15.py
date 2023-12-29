def get_input():
    with open("day15.txt", "r") as file:
        data = file.read()[:-1]

    return data.split(",")


def apply_hash(string):
    current_value = 0

    for i in string:
        code = ord(i)
        current_value += code
        current_value *= 17
        current_value %= 256

    return current_value


def part1():
    strings = get_input()

    total = 0
    for i in strings:
        total += apply_hash(i)

    print(total)


part1()


#---------


def dash(boxes, label):
    box = apply_hash(label)

    new_box = []
    for i in boxes[box]:
        if i[0] != label:
            new_box.append(i)

    boxes[box] = new_box


def equals(boxes, label, focal_length):
    box = apply_hash(label)

    for i, x in enumerate(boxes[box]):
        if x[0] == label:
            boxes[box][i][1] = focal_length
            return
        
    boxes[box].append([label, focal_length])


def do_command(string, boxes):
    label = ""
    focal_length = ""
    operation = ""

    for i in string:
        if i == "-" or i == "=":
            operation = i
        elif operation == "":
            label += i
        else:
            focal_length += i

    if operation == "-":
        dash(boxes, label)
    else:
        equals(boxes, label, int(focal_length))


def get_focus_power(boxes):
    total = 0
    for box_num, box in enumerate(boxes):
        for i, x in enumerate(box):
            slot_num = i + 1
            lens_power = (1 + box_num) * slot_num * x[1]

            total += lens_power

    return total


def part2():
    strings = get_input()
    boxes = [[] for _ in range(256)]

    for i in strings:
        do_command(i, boxes)

    total = get_focus_power(boxes)

    print(total)


part2()
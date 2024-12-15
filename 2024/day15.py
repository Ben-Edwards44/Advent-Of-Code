def get_input():
    with open("day15.txt", "r") as file:
        data = file.read().strip()

    map, moves = data.split("\n\n")

    map = [[i for i in x] for x in map.splitlines()]
    moves = [i for i in moves if i != "\n"]

    return map, moves


def move_box(map, box_x, box_y, dir_x, dir_y):
    new_x, new_y = box_x + dir_x, box_y + dir_y

    box_char = map[box_x][box_y]

    if map[new_x][new_y] == ".":
        map[box_x][box_y] = "."
        map[new_x][new_y] = box_char

        return True
    elif map[new_x][new_y] == "#":
        return False
    else:
        moved = move_box(map, new_x, new_y, dir_x, dir_y)

        if moved:
            map[box_x][box_y] = "."
            map[new_x][new_y] = box_char

        return moved
    

def get_dir(move):
    match move:
        case "^": return -1, 0
        case "<": return 0, -1
        case ">": return 0, 1
        case "v": return 1, 0


def make_move(map, x, y, move):
    dir_x, dir_y = get_dir(move)
    new_x, new_y = x + dir_x, y + dir_y

    if map[new_x][new_y] == ".":
        map[x][y] = "."
        map[new_x][new_y] = "@"

        return new_x, new_y
    elif map[new_x][new_y] == "O" and move_box(map, new_x, new_y, dir_x, dir_y):
        map[x][y] = "."
        map[new_x][new_y] = "@"

        return new_x, new_y
    elif (map[new_x][new_y] == "[" or map[new_x][new_y] == "]") and move_wide_box(map, new_x, new_y, dir_x, dir_y, True):
        map[x][y] = "."
        map[new_x][new_y] = "@"

        return new_x, new_y
    else:
        return x, y


def get_robot_pos(map):
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == "@":
                return i, j
            

def get_gps_score(map, moves):
    x, y = get_robot_pos(map)

    for i in moves:
        x, y = make_move(map, x, y, i)

    total = 0
    for i, x in enumerate(map):
        for j, k in enumerate(x):
            if k == "O" or k == "[":
                total += 100 * i + j

    return total


def part1():
    map, moves = get_input()
    total = get_gps_score(map, moves)

    print(total)


part1()


#--------


def resize_map(map):
    new_map = []
    for i in map:
        new_map.append([])

        for x in i:
            match x:
                case "#": new_map[-1] += ["#", "#"]
                case "O": new_map[-1] += ["[", "]"]
                case ".": new_map[-1] += [".", "."]
                case "@": new_map[-1] += ["@", "."]

    return new_map


def move_wide_box(map, box_x, box_y, dir_x, dir_y, actually_move_box):
    if dir_x == 0:
        return move_box(map, box_x, box_y, dir_x, dir_y)
    
    if map[box_x][box_y] == "[":
        lpos = (box_x, box_y)
        rpos = (lpos[0], lpos[1] + 1)
    else:
        rpos = (box_x, box_y)
        lpos = (rpos[0], rpos[1] - 1)

    can_move_left = move_part_wide_box(map, lpos, dir_x, dir_y, False)
    can_move_right = move_part_wide_box(map, rpos, dir_x, dir_y, False)

    if actually_move_box and can_move_left and can_move_right:
        move_part_wide_box(map, lpos, dir_x, dir_y, True)
        move_part_wide_box(map, rpos, dir_x, dir_y, True)

    return can_move_left and can_move_right
    

def move_part_wide_box(map, box_pos, dir_x, dir_y, actually_move_box):
    box_char = map[box_pos[0]][box_pos[1]]
    new_x, new_y = box_pos[0] + dir_x, box_pos[1] + dir_y

    if map[new_x][new_y] == ".":
        if actually_move_box:
            map[box_pos[0]][box_pos[1]] = "."
            map[new_x][new_y] = box_char

        return True
    elif map[new_x][new_y] == "#":
        return False
    else:
        moved = move_wide_box(map, new_x, new_y, dir_x, dir_y, actually_move_box)
    
        if moved and actually_move_box:
            map[box_pos[0]][box_pos[1]] = "."
            map[new_x][new_y] = box_char

        return moved


def part2():
    map, moves = get_input()
    map = resize_map(map)

    total = get_gps_score(map, moves)

    print(total)


part2()
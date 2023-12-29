def get_input():
    with open("day16.txt", "r") as file:
        data = file.read()

    return data.split("\n")[:-1]


def beam_travel(grid, pos_x, pos_y, dir_x, dir_y):
    global done_squares, done_s_inx


    while True:
        if not 0 <= pos_x < len(grid) or not 0 <= pos_y < len(grid[0]):
            return
        
        square = grid[pos_x][pos_y]
        
        key = (pos_x, pos_y, dir_x, dir_y)

        if key in done_s_inx:
            return
        else:
            done_s_inx.add(key)
        
        done_squares.add((pos_x, pos_y))

        if square == "/":
            if dir_x == 0:
                dir_x = -dir_y
                dir_y = 0
            else:
                dir_y = -dir_x
                dir_x = 0
        elif square == "\\":
            if dir_x == 0:
                dir_x = dir_y
                dir_y = 0
            else:
                dir_y = dir_x
                dir_x = 0
        elif square == "|" and dir_x == 0 or square == "-" and dir_y == 0:
            break

        pos_x += dir_x
        pos_y += dir_y

    if square == "|":
        if dir_x == 0:
            for new_dir_x in range(-1, 2, 2):
                new_x = pos_x + new_dir_x

                beam_travel(grid, new_x, pos_y, new_dir_x, 0)
    elif square == "-":
        if dir_y == 0:
            for new_dir_y in range(-1, 2, 2):
                new_y = pos_y + new_dir_y

                beam_travel(grid, pos_x, new_y, 0, new_dir_y)


def part1():
    global done_squares
    global done_s_inx

    done_squares = set()
    done_s_inx = set()

    grid = get_input()

    beam_travel(grid, 0, 0, 0, 1)

    total = len(done_squares)

    print(total)


part1()


#-------


def get_start_pos(length):
    starts = []

    for i in range(1, length - 1):
        for other in [0, length - 1]:
            pos1 = (i, other)
            dir1 = (0, 1) if other == 0 else (0, -1)

            pos2 = (other, i)
            dir2 = (1, 0) if other == 0 else (-1, 0)

            starts.append((pos1, dir1))
            starts.append((pos2, dir2))

    tl = (0, 0)
    tr = (0, length - 1)
    bl = (length - 1, 0)
    br = (length - 1, length - 1)

    d = (1, 0)
    u = (-1, 0)
    l = (0, -1)
    r = (0, 1)

    for dir in [d, r]:
        starts.append((tl, dir))
    for dir in [d, l]:
        starts.append((tr, dir))
    for dir in [u, r]:
        starts.append((bl, dir))
    for dir in [u, l]:
        starts.append((br, dir))

    return starts


def part2():
    global done_squares
    global done_s_inx

    grid = get_input()
    starts = get_start_pos(len(grid))

    best = 0
    for pos, dir in starts:
        done_squares = set()
        done_s_inx = set()

        beam_travel(grid, pos[0], pos[1], dir[0], dir[1])

        if len(done_squares) > best:
            best = len(done_squares)

    print(best)


part2()
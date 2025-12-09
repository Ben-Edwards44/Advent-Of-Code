def get_input():
    with open("day9.txt", "r") as file:
        data = file.read().splitlines()

    return [[int(i) for i in x.split(",")] for x in data]


def get_largest(tiles, start):
    max_area = 0

    for i in tiles:
        area = (abs(start[0] - i[0]) + 1) * (abs(start[1] - i[1]) + 1)

        if area > max_area:
            max_area = area

    return max_area


def part1():
    tiles = get_input()

    largest = 0
    for i in tiles:
        largest = max(largest, get_largest(tiles, i))

    print(largest)


part1()


#----------


def point_inside(tiles, point):
    #shoot horiztonal ray to the left
    crosses = 0
    for i, current in enumerate(tiles):
        next = tiles[(i + 1) % len(tiles)]

        if current[0] == next[0] or current[1] > point[1]:
            continue

        uppermost = min(current[0], next[0])
        lowermost = max(current[0], next[0])

        if uppermost <= point[1] <= lowermost:
            crosses += 1


    return crosses % 2 == 1 


def edge_strictly_in_rect(tiles, tl, br):
    #if there is a point on an edge STRICTLY inside the rect then not a valid rect
    for i, start in enumerate(tiles):
        end = tiles[(i + 1) % len(tiles)]

        if start[0] == end[0]:
            #horizontal line
            if not tl[0] < start[0] < br[0]:
                continue

            leftmost = min(start[1], end[1])
            rightmost = max(start[1], end[1])

            if leftmost < br[1] and rightmost >= br[1] or rightmost > tl[1] and leftmost <= tl[1]:
                return True
        else:
            #vertical line
            if not tl[1] < start[1] < br[1]:
                continue

            uppermost = min(start[0], end[0])
            lowermost = max(start[0], end[0])

            if uppermost < br[0] and lowermost >= br[0] or lowermost > tl[0] and uppermost <= tl[0]:
                return True
            
    return False


def valid_rect(tiles, a, b):
    tl = (min(a[0], b[0]), min(a[1], b[1]))
    br = (max(a[0], b[0]), max(a[1], b[1]))

    if edge_strictly_in_rect(tiles, tl, br):
        return False
    
    #but the rect may still be outside the polygon with just some of its edges in
    all_corners = [
        tl,
        (tl[0], br[1]),
        (br[0], tl[1]),
        br
    ]

    middle_point = (sum(i[0] for i in all_corners) // 4, sum(i[1] for i in all_corners) // 4)

    return point_inside(tiles, middle_point)


def new_largest(tiles, start):
    max_area = 0
    for i in tiles:
        area = (abs(start[0] - i[0]) + 1) * (abs(start[1] - i[1]) + 1)

        if valid_rect(tiles, start, i) and area > max_area:
            max_area = area

    return max_area


def part2():
    tiles = get_input()

    largest = 0
    for i in tiles:
        largest = max(largest, new_largest(tiles, i))

    print(largest)


part2()
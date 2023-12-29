from string import ascii_uppercase


class Brick:
    def __init__(self, point1, point2, name):
        self.point1 = point1
        self.point2 = point2

        self.name = name
    
    def collide(self, other_brick):
        #no z
        for i in range(2):
            if not self.point_cross(other_brick, i):
                return False
            
        return True
    
    def collide_with_z(self, other_brick):
        for i in range(3):
            if not self.point_cross(other_brick, i):
                return False
            
        return True
    
    def lower(self):
        self.point1[2] -= 1
        self.point2[2] -= 1

    def inc(self):
        self.point1[2] += 1
        self.point2[2] += 1
    
    point_cross = lambda self, other_brick, inx: self.lowest_point(inx) <= other_brick.highest_point(inx) and self.highest_point(inx) >= other_brick.lowest_point(inx)
    lowest_point = lambda self, inx: min(self.point1[inx], self.point2[inx])
    highest_point = lambda self, inx: max(self.point1[inx], self.point2[inx])


def get_input():
    with open("day22.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    bricks = []
    inx = 0
    for i in data:
        a, b = i.split("~")

        coord_a = [int(x) for x in a.split(",")]
        coord_b = [int(x) for x in b.split(",")]

        bricks.append(Brick(coord_a, coord_b, "ascii_uppercase[inx]"))
        inx += 1

    return bricks


def adjust_ground(bricks):
    min_z = None
    for i in bricks:
        z = i.lowest_point(2)

        if min_z == None or z < min_z:
            min_z = z

    for i in bricks:
        i.point1[2] -= min_z - 1
        i.point2[2] -= min_z - 1


def add_to_dict(dict, key, value):
    if key in dict.keys():
        if value not in dict[key]:
            dict[key].append(value)
    else:
        dict[key] = [value]


def build_z_dict(bricks):
    z_values = {}
    max = None
    for i in bricks:
        z1 = i.lowest_point(2)
        z2 = i.highest_point(2)

        if max == None or z2 > max:
            max = z2

        add_to_dict(z_values, z1, i)
        add_to_dict(z_values, z2, i)

    return z_values


def can_lower(brick, z_values, z):
    if z < 1:
        return False
    elif z not in z_values.keys():
        return True
    
    for i in z_values[z]:
        if i != brick and brick.collide(i):
            return False
        
    return True


def lower_brick(brick, z_values):
    low_z = brick.lowest_point(2)
    high_z = brick.highest_point(2)
    
    offset = 1

    while can_lower(brick, z_values, low_z - offset):
        brick.lower()
        offset += 1

    z_values[low_z].remove(brick)

    if low_z != high_z:
        z_values[high_z].remove(brick)

    add_to_dict(z_values, low_z - offset + 1, brick)
    add_to_dict(z_values, high_z - offset + 1, brick)


def is_done(bricks, z_values):
    for i in bricks:
        if can_lower(i, z_values, i.lowest_point(2) - 1):
            return False
        
    return True


def lower_layer(z_values, z):
    prev = [i for i in z_values[z]]

    for i in prev:
        lower_brick(i, z_values)

    return prev == z_values[z]


def get_max(z_values):
    max_val = max(z_values.keys())
    for i in range(max_val, 0, -1):
        if i in z_values.keys() and len(z_values[i]) > 0:
            return i
        

def lower_all(z_values):
    moved = True
    while moved:
        moved = False
        max_value = get_max(z_values)

        for i in range(max_value + 1):
            if i not in z_values.keys():
                continue

            same = lower_layer(z_values, i)

            if not same:
                moved = True


def get_contact(brick, z_values):
    low_z = brick.lowest_point(2)

    if low_z - 1 in z_values.keys():
        below_layer = z_values[low_z - 1]
    else:
        below_layer = []

    if below_layer == [] and low_z > 1:
        raise Exception("liuluig")

    in_contact = []
    for i in below_layer:
        if brick.collide(i):
            in_contact.append(i)

    return in_contact


def get_total(bricks, z_values):
    cannot_remove = set()
    for i in bricks:
        contact = get_contact(i, z_values)

        if len(contact) == 1:
            cannot_remove.add(contact[0])

    total = len(bricks) - len(cannot_remove)

    return total


def part1():
    bricks = get_input()
    adjust_ground(bricks)
        
    z_values = build_z_dict(bricks)

    lower_all(z_values)

    total = get_total(bricks, z_values)

    print(total)


part1()


#--------


def get_need_move(bricks, z_values):
    cannot_remove = set()
    for i in bricks:
        contact = get_contact(i, z_values)

        if len(contact) == 1:
            cannot_remove.add(contact[0])

    return cannot_remove


def get_num_fall(bricks, z_values):
    prev_coords = [[[y for y in x] for x in (i.point1, i.point2)] for i in bricks]

    lower_all(z_values)

    total_fall = 0
    for i, x in enumerate(bricks):
        a, b = prev_coords[i]

        if a != x.point1 or b != x.point2:
            total_fall += 1

            #reset stuff
            x.point1 = a
            x.point2 = b

    #reset
    z_values = build_z_dict(bricks)

    return total_fall


def remove_brick(brick, bricks):
    bricks.remove(brick)
    z_values = build_z_dict(bricks)

    num = get_num_fall(bricks, z_values)

    #reset
    bricks.append(brick)
    
    return num


def new_total(bricks, z_values):
    moving = get_need_move(bricks, z_values)

    total = 0
    for i in moving:
        num = remove_brick(i, bricks)
        total += num

    return total


def part2():
    bricks = get_input()
    adjust_ground(bricks)
        
    z_values = build_z_dict(bricks)

    lower_all(z_values)

    total = new_total(bricks, z_values)

    print(total)


part2()
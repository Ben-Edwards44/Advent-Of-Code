class Hailstone:
    def __init__(self, x, y, z, v_x, v_y, v_z):
        self.x = x
        self.y = y
        self.z = z

        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z

        self.m, self.c = self.get_line_eq()

    def get_line_eq(self):
        x1 = self.x
        y1 = self.y

        x2 = self.x + self.v_x
        y2 = self.y + self.v_y

        m = (y1 - y2) / (x1 - x2)
        c = y1 - m * x1

        return m, c
    
    def is_in_past(self, x, y):
        x_dec = x < self.x
        x_vel_dec = self.v_x < 0

        y_dec = y < self.y
        y_vel_dec = self.v_y < 0

        if x_dec != x_vel_dec:
            return True
        elif y_dec != y_vel_dec:
            return True
        else:
            return False
        
    def get_pos(self, time):
        x = self.x + time * self.v_x
        y = self.y + time * self.v_y
        z = self.z + time * self.v_z

        return x, y, z


def get_input():
    with open("day24.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    stones = []

    for line in data:
        pos, vel = line.split(" @ ")
        x, y, z = [int(i) for i in pos.split(", ")]
        v_x, v_y, v_z = [int(i) for i in vel.split(", ")]

        stone = Hailstone(x, y, z, v_x, v_y, v_z)
        stones.append(stone)

    return stones


def get_collide_point(a, b):
    x_coeff = a.m - b.m
    num = b.c - a.c

    if x_coeff == 0:
        #parallel
        return None, None

    x_coord = num / x_coeff
    y_coord = a.m * x_coord + a.c

    if a.is_in_past(x_coord, y_coord) or b.is_in_past(x_coord, y_coord):
        x_coord = None
        y_coord = None

    return x_coord, y_coord


def get_total(stones):
    least = 200000000000000
    most = 400000000000000

    total = 0
    for i, a in enumerate(stones):
        for b in stones[i + 1:]:
            x, y = get_collide_point(a, b)

            if x != None and y != None and least <= x <= most and least <= y <= most:
                total += 1

    return total


def part1():
    stones = get_input()

    total = get_total(stones)

    print(total)


part1()


#---------
    

#Did not manage part 2
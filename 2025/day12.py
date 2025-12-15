class PartialSolution:
    def __init__(self, size, available_points, needs, bound_left, bound_right):
        self.size = size
        self.available_points = available_points
        self.needs = needs
        self.bound_left = bound_left
        self.bound_right = bound_right

    def point_to_bitboard(self, point):
        num_shift = point[0] * self.size[1] + point[1]

        return 1 << num_shift
    
    def gen_possible_points(self):
        points = []
        for i in range(self.size[0]):
            for x in range(self.size[1]):
                point = (i, x)

                if self.point_to_bitboard(point) & self.available_points > 0:
                    points.append(point)

        return points


class Present:
    def __init__(self, string):
        self.points1 = self.extract_local_points(string)
        self.points2 = self.rot90(self.points1)
        self.points3 = self.rot90(self.points2)
        self.points4 = self.rot90(self.points3)

        self.points = (
            self.points1,
            self.points2,
            self.points3,
            self.points4
        )

        self.area = len(self.points1)

    def extract_local_points(self, string):
        points = []
        for i, x in enumerate(string):
            for j, k in enumerate(x):
                if k == "#":
                    points.append((i, j))

        return points
    
    def rot90(self, points):
        return [(-y, x) for x, y in points]
    
    def can_fit(self, partial_solution, top_left, rot_inx):
        bound_left = partial_solution.bound_left
        bound_right = partial_solution.bound_right

        bitboard = 0
        for x, y in self.points[rot_inx]:
            global_x = top_left[0] + x
            global_y = top_left[1] + y

            if global_x < 0 or global_y < 0:
                return False, None, None, None

            bitboard |= partial_solution.point_to_bitboard((global_x, global_y))

            if bound_left is None:
                bound_left = (global_x, global_y)
            else:
                bound_left = (min(bound_left[0], global_x), min(bound_left[1], global_y))

            if bound_right is None:
                bound_right = (global_x, global_y)
            else:
                bound_right = (max(bound_right[0], global_x), max(bound_right[1], global_y))

        mask = partial_solution.available_points & bitboard 

        return mask == bitboard, bitboard, bound_left, bound_right


def get_input():
    with open("day12.txt", "r") as file:
        data = file.read().split("\n\n")

    presents = []
    for i in data[:-1]:
        shape_string = i.splitlines()[1:]
        presents.append(Present(shape_string))

    regions = []
    for i in data[-1].splitlines():
        size, needs = i.split(": ")

        int_size = tuple(int(x) for x in size.split("x"))
        int_needs = [int(x) for x in needs.split(" ")]

        regions.append([int_size, int_needs])

    return presents, regions


def area_bounds(bl, br):
    return (br[0] - bl[0]) * (br[1] - bl[1])


def try_place_presents(presents, partial_solution):
    next_steps = []
    for i, x in enumerate(partial_solution.needs):
        if x == 0:
            continue

        present = presents[i]

        new_needs = partial_solution.needs[:]
        new_needs[i] -= 1

        for tl in partial_solution.gen_possible_points():
            for rot in range(4):
                fits, present_bitboard, bl, br = present.can_fit(partial_solution, tl, rot)

                if fits:
                    new_available = partial_solution.available_points ^ present_bitboard
                    area = area_bounds(bl, br)

                    next_steps.append((PartialSolution(partial_solution.size, new_available, new_needs, bl, br), area))

    return next_steps


def initial_place(presents, needs, size):
    all_points = (1 << (size[0] * size[1])) - 1
    placeholder = PartialSolution(size, all_points, needs, None, None)

    initial_places = try_place_presents(presents, placeholder)
    solution_only = [i[0] for i in initial_places]

    start = solution_only[0]

    return greedy(presents, start)


def greedy(presents, partial_solution):
    if all(i == 0 for i in partial_solution.needs):
        return True
    
    next_steps = try_place_presents(presents, partial_solution)

    next_steps.sort(key=lambda x: x[-1])

    if len(next_steps) == 0:
        return False
    else:
        return greedy(presents, next_steps[0][0])


def part1():
    presents, regions = get_input()

    total = 0
    for size, needs in regions:
        if initial_place(presents, needs, size):
            total += 1
        
    print(total)


part1()
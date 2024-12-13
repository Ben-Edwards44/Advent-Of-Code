class ClawMachine:
    def __init__(self, string):
        self.parse_string(string)

    def parse_string(self, string):
        a, b, t = string.split("\n")

        self.ax, self.ay = self.parse_line(a)
        self.bx, self.by = self.parse_line(b)
        self.target_x, self.target_y = self.parse_line(t)

    def parse_line(self, button_string):
        _, string = button_string.split(": ")
        x, y = string.split(", ")

        return int(x[2:]), int(y[2:])


def get_input():
    with open("day13.txt", "r") as file:
        data = file.read().strip()

    machines = data.split("\n\n")

    return [ClawMachine(i) for i in machines]


def solve_equation(machine):
    denominator = machine.ax * machine.by - machine.bx * machine.ay
    assert denominator != 0

    b = (machine.ax * machine.target_y - machine.ay * machine.target_x) / denominator
    a = (machine.target_x - machine.bx * b) / machine.ax

    return a, b


is_int = lambda x: abs(int(x) - x) < 0.00001


def part1():
    machines = get_input()

    total = 0
    for i in machines:
        a, b = solve_equation(i)

        if is_int(a) and is_int(b):
            total += 3 * int(a) + int(b)

    print(total)


part1()


#--------


def part2():
    add = 10000000000000

    machines = get_input()

    total = 0
    for i in machines:
        i.target_x += add
        i.target_y += add

        a, b = solve_equation(i)

        if is_int(a) and is_int(b):
            total += 3 * int(a) + int(b)

    print(total)


part2()
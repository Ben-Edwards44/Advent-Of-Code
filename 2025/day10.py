import re


class QueueItem:
    def __init__(self, light_state, unused_buttons, num_presses):
        self.light_state = light_state
        self.unused_buttons = unused_buttons
        self.num_presses = num_presses


def get_input():
    with open("day10.txt", "r") as file:
        data = file.read().splitlines()

    lights = []
    buttons = []
    joltages = []
    for i in data:
        light = re.findall(r"\[(?:\.|#)+\]", i)[0]
        button = re.findall(r"\((?:[0-9]|,)+\)", i)
        joltage = re.findall(r"{(?:[0-9]|,)+}", i)[0]

        lights.append([x == "#" for x in light[1:-1]])
        joltages.append(list(map(int, joltage[1:-1].split(","))))
        buttons.append([list(map(int, x[1:-1].split(","))) for x in button])

    return lights, buttons, joltages


def push_button(lights, button):
    new_lights = lights[:]
    for i in button:
        new_lights[i] = not new_lights[i]

    return new_lights


def bfs(target_lights, buttons):
    current = QueueItem([False for _ in target_lights], buttons, 0)
    queue = [current]
    visited_lights = []

    while current.light_state != target_lights:
        current = queue.pop(0)

        if current.light_state in visited_lights:
            continue

        visited_lights.append(current.light_state[:])

        for i in current.unused_buttons:
            new_light_state = push_button(current.light_state, i)

            if new_light_state not in visited_lights:
                new_buttons = [x for x in current.unused_buttons if x != i]
                queue.append(QueueItem(new_light_state, new_buttons, current.num_presses + 1))

    return current.num_presses


def part1():
    lights, buttons, _ = get_input()

    total = 0
    for i, x in zip(lights, buttons):
        total += bfs(i, x)

    print(total)


part1()


#------


class Matrix:
    def __init__(self, items):
        self.items = items

    def swap_rows(self, inx1, inx2):
        self.items[inx1], self.items[inx2] = self.items[inx2], self.items[inx1]

    def mult_row(self, inx, scalar):
        self.items[inx] = [i * scalar for i in self.items[inx]]

    def add_rows(self, start, to, mult):
        self.items[to] = [x + mult * self.items[start][i] for i, x in enumerate(self.items[to])]

    def reduce_col(self, col_inx):
        for i in range(col_inx, len(self.items)):
            if abs(self.items[i][col_inx]) > 0.0001:
                self.swap_rows(col_inx, i)
                self.mult_row(col_inx, 1 / self.items[col_inx][col_inx])
                break
            
        for i in range(len(self.items)):
            if i != col_inx:
                self.add_rows(col_inx, i, -self.items[i][col_inx])

    def rre_form(self):
        max_inx = min(len(self.items), len(self.items[0]))
        for i in range(max_inx):
            self.reduce_col(i)

    def system_consistent(self):
        self.rre_form()

        for i in self.items:
            if all(abs(x) < 0.0001 for x in i[:-1]) and abs(i[-1]) > 0.0001:
                return False
            
        return True


def has_solutions(joltage, buttons):
    mat_items = [[] for _ in joltage]
    for i in buttons:
        for x in range(len(joltage)):
            if x in i:
                mat_items[x].append(1)
            else:
                mat_items[x].append(0)

    for i, x in enumerate(joltage):
        mat_items[i].append(x)

    mat = Matrix(mat_items)

    return mat.system_consistent()


def is_good(joltage, buttons):
    for i in joltage:
        if i < 0:
            return False

    if not has_solutions(joltage, buttons):
        return False
        
    return True


def new_push_button(joltage, button, num_pushes):
    new_joltage = [i for i in joltage]
    for i in button:
        new_joltage[i] -= num_pushes

    return tuple(new_joltage)


def dfs(joltage, sorted_buttons, button_inx):
    if all(i == 0 for i in joltage):
        return 0
    elif button_inx >= len(sorted_buttons):
        return -1
    elif not is_good(joltage, sorted_buttons[button_inx:]):
        return -1
        
    button = sorted_buttons[button_inx]
    max_pushes = min(joltage[i] for i in button)

    result = -1
    for pushes in range(max_pushes, -1, -1):
        new_joltage = new_push_button(joltage, button, pushes)
        subsequent = dfs(new_joltage, sorted_buttons, button_inx + 1)

        if subsequent != -1:
            if result == -1:
                result = pushes + subsequent
            else:
                result = min(result, pushes + subsequent)        

    return result
                        

def get_num_presses(target_joltage, buttons):
    current_joltage = tuple(target_joltage)
    sorted_buttons = sorted(buttons, key=lambda x: len(x), reverse=True)

    result = dfs(current_joltage, sorted_buttons, 0)

    return result


def part2():
    _, buttons, joltages = get_input()

    total = 0
    for i, x in zip(joltages, buttons):
        total += get_num_presses(i, x)

    print(total)


part2()
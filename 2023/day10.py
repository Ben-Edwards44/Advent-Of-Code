class Pipe:
    def __init__(self, grid, x, y):
        self.grid = grid

        #x, y are cartesian coords
        self.x = x
        self.y = y

    def get_pipe(self, x, y):
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x]
        else:
            return None
        
    def __hash__(self) -> int:
        prime1 = 4967
        prime2 = 7919

        return self.x * prime1 + self.y * prime2

    
class Vert(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        if s_x != self.x:
            return None
        
        if s_y < self.y:
            new_y = self.y + 1
        else:
            new_y = self.y - 1

        return self.get_pipe(self.x, new_y)
    

class Hor(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        if s_y != self.y:
            return None
        
        if s_x < self.x:
            new_x = self.x + 1
        else:
            new_x = self.x - 1

        return self.get_pipe(new_x, self.y)
    

class NE(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        if s_y == self.y and s_x == self.x + 1:
            #start E
            new_y = self.y - 1
            new_x = self.x
        elif s_y == self.y - 1 and s_x == self.x:
            new_y = self.y
            new_x = self.x + 1
        else:
            return None

        return self.get_pipe(new_x, new_y)


class NW(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        if s_y == self.y and s_x == self.x - 1:
            #start W
            new_y = self.y - 1
            new_x = self.x
        elif s_y == self.y - 1 and s_x == self.x:
            new_y = self.y
            new_x = self.x - 1
        else:
            return None

        return self.get_pipe(new_x, new_y)
    

class SW(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        if self.y == s_y and s_x == self.x - 1:
            #start W
            new_y = self.y + 1
            new_x = self.x
        elif s_y == self.y + 1 and s_x == self.x:
            new_y = self.y
            new_x = self.x - 1
        else:
            return None

        return self.get_pipe(new_x, new_y)


class SE(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        if s_y == self.y and s_x == self.x + 1:
            #start E
            new_y = self.y + 1
            new_x = self.x
        elif s_y == self.y + 1 and s_x == self.x:
            new_y = self.y
            new_x = self.x + 1
        else:
            return None

        return self.get_pipe(new_x, new_y)
    

class Ground(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        return None
    

class Start(Pipe):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y)

    def get_connect(self, s_x, s_y):
        adj = []
        for i in range(-1, 2):
            for x in range(-1, 2):
                if i == x or i != 0 and x != 0:
                    continue

                if 0 <= self.x + i < len(self.grid[0]) and 0 <= self.y + x < len(self.grid):
                    adj.append(self.grid[self.y + x][self.x + i])

        return adj


def get_input():
    with open("day10.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    pipes = [[None for _ in i] for i in data]

    start_x = 0
    start_y = 0

    for i, x in enumerate(data):
        for j, k in enumerate(x):
            if k == "|":
                p = Vert
            elif k == "-":
                p = Hor
            elif k == "L":
                p = NE
            elif k == "J":
                p = NW
            elif k == "7":
                p = SW
            elif k == "F":
                p = SE
            elif k == "S":
                p = Start
                start_x = j
                start_y = i
            else:
                p = Ground

            pipes[i][j] = p(None, j, i)

    for i in pipes:
        for x in i:
            x.grid = pipes

    return pipes, start_x, start_y


def travel_through(start_x, start_y, pipe):
    path = [pipe]

    current = pipe
    prev_x = start_x
    prev_y = start_y

    is_loop = False
    while not is_loop:
        c_x = current.x
        c_y = current.y

        current = current.get_connect(prev_x, prev_y)

        prev_x = c_x
        prev_y = c_y

        if current == None:
            break

        path.append(current)
        is_loop = current.x == start_x and current.y == start_y

    return is_loop, path


def part1():
    pipes, s_x, s_y = get_input()

    adj = pipes[s_y][s_x].get_connect(None, None)

    two_ways = []
    for i in adj:
        if type(i) == Ground:
            continue

        good, path = travel_through(s_x, s_y, i)

        if good:
            two_ways.append(path)

    step = 0
    for i in range(len(two_ways[0])):
        if two_ways[0][i] == two_ways[1][i]:
            step = i + 1
            break

    print(step)


part1()


#--------


def expand(pipes, loop_set):
    expanded = []
    for i in pipes:
        expanded.append([j if j in loop_set else "." for j in i])
        expanded.append(["." for _ in range(len(i))])

    final = []
    for i in expanded:
        line = []
        for x in i:
            line.append(x)
            line.append(".")

        final.append(line)

    return final


def get_item(grid, x, y):
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        return grid[x][y]
    else:
        return None
    

def is_connection(a, b, loop):
    for i, x in enumerate(loop):        
        if x == a or x == b:
            if loop[i + 1] == a or loop[i + 1] == b:
                return True
            elif i != 0:
                return False


def add_connections(expanded, loop):
    for i, x in enumerate(expanded):
        for j, k in enumerate(x):
            if k != ".":
                continue

            l = get_item(expanded, i, j - 1)
            r = get_item(expanded, i, j + 1)
            u = get_item(expanded, i - 1, j)
            d = get_item(expanded, i + 1, j)

            if l != "." and r != "." and is_connection(l, r, loop):
                expanded[i][j] = "X"
            elif u != "." and d != "." and is_connection(u, d, loop):
                expanded[i][j] = "X"


def convert(grid):
    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k != ".":
                grid[i][j] = "X"


def get_adj_inxs(grid, x, y):
    inxs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j or i != 0 and j != 0:
                continue

            if 0 <= x + i < len(grid) and 0 <= y + j < len(grid[0]):
                inxs.append([x + i, y + j])

    return inxs


def fill_out(expanded, steps, step):
    added = False
    for i, x in enumerate(steps):
        for j, k in enumerate(x):
            if k == step:
                inxs = get_adj_inxs(steps, i, j)

                for m, n in inxs:
                    if expanded[m][n] == "." and steps[m][n] == 0:
                        steps[m][n] = step + 1
                        added = True

    return added


def fill_from_start(x, y, steps, expanded):
    step = 1
    steps[x][y] = 1

    while fill_out(expanded, steps, step):
        step += 1


def get_outside(expanded):
    steps = [[0 for _ in i] for i in expanded]

    for i in range(len(expanded)):
        if steps[i][0] == 0 and expanded[i][0] == ".":
            fill_from_start(i, 0, steps, expanded)
        if steps[i][-1] == 0 and expanded[i][-1] == ".":
            fill_from_start(i, -1, steps, expanded)

    for i in range(len(expanded)):
        if steps[0][i] == 0 and expanded[0][i] == ".":
            fill_from_start(0, i, steps, expanded)
        if steps[-1][i] == 0 and expanded[-1][i] == ".":
            fill_from_start(-1, i, steps, expanded)

    return steps


def get_total(og_pipes, out_steps, loop_set):
    total = 0
    for i, x in enumerate(og_pipes):
        for j, k in enumerate(x):
            if k not in loop_set:
                exp_x = i * 2
                exp_y = j * 2

                if out_steps[exp_x][exp_y] == 0:
                    total += 1

    return total


def part2():
    pipes, s_x, s_y = get_input()

    adj = pipes[s_y][s_x].get_connect(None, None)

    loop = []
    for i in adj:
        if type(i) == Ground:
            continue

        good, path = travel_through(s_x, s_y, i)

        if good:
            loop = path
            loop_set = {i for i in path}
            break

    loop.insert(0, pipes[s_y][s_x])
    
    expanded = expand(pipes, loop_set)
    add_connections(expanded, loop)

    convert(expanded)

    out_steps = get_outside(expanded)

    total = get_total(pipes, out_steps, loop_set)

    print(total)


part2()
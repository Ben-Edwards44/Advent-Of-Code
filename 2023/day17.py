class Node:
    def __init__(self, grid, x, y, run, prev_x, prev_y):
        self.grid = grid

        self.x = x
        self.y = y

        self.run = run

        self.prev_x = prev_x
        self.prev_y = prev_y

        self.visited = False

        self.heat_loss = 100_000_000

        self.parent = None
        self.children = []
        
    def get_children(self, all_nodes):
        #all_nodes = [
        #               [[{(x, y) : Node, ...}, {...}, {...}], [...], [...]], [...], [...]
        #               [...], [...], [...]
        #            ]

        coords = get_neighbour_coords(self.grid, self.x, self.y, self.prev_x, self.prev_y)

        dir_x = self.x - self.prev_x
        dir_y = self.y - self.prev_y

        child_prev_coords = (self.x, self.y)

        for x, y in coords:
            d_x = x - self.x
            d_y = y - self.y

            if dir_x == d_x and dir_y == d_y:
                child_run = self.run + 1
            else:
                child_run = 1

            if child_run <= 3:
                cell_nodes = all_nodes[x][y]
                run_nodes = cell_nodes[child_run - 1]
                child_node = run_nodes[child_prev_coords]

                self.children.append(child_node)

    current_heat_loss = lambda self: self.grid[self.x][self.y]


def get_input():
    with open("t.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    return [[int(x) for x in i] for i in data]


def create_nodes(grid):
    all_nodes = [[[{} for _ in range(3)] for _ in grid[0]] for _ in grid]

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for run in range(3):
                act_run = run + 1

                enter_coords = get_neighbour_coords(grid, x, y, None, None)

                for coord in enter_coords:
                    new_node = Node(grid, x, y, act_run, coord[0], coord[1])
                    all_nodes[x][y][run][coord] = new_node

    return all_nodes


def init_nodes(all_nodes):
    for x in all_nodes:
        for y in x:
            for dict in y:
                for node in dict.values():
                    node.get_children(all_nodes)


def get_neighbour_coords(grid, x, y, prev_x, prev_y):
    neighbours = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            elif i != 0 and j != 0:
                continue

            new_x = x + i
            new_y = y + j

            if new_x == prev_x and new_y == prev_y:
                continue
            elif 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                neighbours.append((new_x, new_y))

    return neighbours


def get_lowest(nodes):
    lowest = None
    inx = None
    for i, node in enumerate(nodes):
        if not node.visited and (lowest == None or node.heat_loss < lowest.heat_loss):
            lowest = node
            inx = i

    return lowest, inx


def djisktra(all_nodes, end_x, end_y):
    #assume start node score is already 0

    while True:
        current, inx = get_lowest(all_nodes)

        if current.x == end_x and current.y == end_y:
            return current

        current.visited = True
        all_nodes.pop(inx)

        for child in current.children:
            new_heat_loss = child.current_heat_loss() + current.heat_loss

            if new_heat_loss < child.heat_loss:
                child.parent = current
                child.heat_loss = new_heat_loss


def get_node_list(all_nodes):
    nodes = []
    for x in all_nodes:
        for y in x:
            for dict in y:
                for node in dict.values():
                    nodes.append(node)

    return nodes


def part1():
    grid = get_input()
    
    losses = []
    start_coords = [(0, 1), (1, 0)]
    for coord in start_coords:
        all_nodes = create_nodes(grid)
        init_nodes(all_nodes)
        nodes = get_node_list(all_nodes)

        #run = 2 => run_inx = 1
        node = all_nodes[coord[0]][coord[1]][1][(0, 0)]
        node.heat_loss = node.current_heat_loss()

        end_node = djisktra(nodes, len(grid) - 1, len(grid[0]) - 1)
        losses.append(end_node.heat_loss)

    total = min(losses)

    print(total)


part1()


#-----------


class NewNode:
    def __init__(self, grid, x, y, run, prev_x, prev_y):
        self.grid = grid

        self.x = x
        self.y = y

        self.run = run

        self.prev_x = prev_x
        self.prev_y = prev_y

        self.visited = False

        self.heat_loss = 100_000_000

        self.parent = None
        self.children = []
        
    def get_children(self, all_nodes):
        #all_nodes = [
        #               [[{(x, y) : Node, ...}, {...}, {...}], [...], [...]], [...], [...]
        #               [...], [...], [...]
        #            ]

        coords = get_neighbour_coords(self.grid, self.x, self.y, self.prev_x, self.prev_y)

        dir_x = self.x - self.prev_x
        dir_y = self.y - self.prev_y

        child_prev_coords = (self.x, self.y)

        for x, y in coords:
            d_x = x - self.x
            d_y = y - self.y

            if dir_x == d_x and dir_y == d_y:
                child_run = self.run + 1
            else:
                child_run = 1

            if child_run == 1 and self.run < 4:
                continue
            elif x == len(self.grid) - 1 and y == len(self.grid[0]) - 1:
                if child_run < 4:
                    continue

            if child_run <= 10:
                cell_nodes = all_nodes[x][y]
                run_nodes = cell_nodes[child_run - 1]
                child_node = run_nodes[child_prev_coords]

                self.children.append(child_node)

    current_heat_loss = lambda self: self.grid[self.x][self.y]


def new_create_nodes(grid):
    all_nodes = [[[{} for _ in range(10)] for _ in grid[0]] for _ in grid]

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for run in range(10):
                act_run = run + 1

                enter_coords = get_neighbour_coords(grid, x, y, None, None)

                for coord in enter_coords:
                    new_node = NewNode(grid, x, y, act_run, coord[0], coord[1])
                    all_nodes[x][y][run][coord] = new_node

    return all_nodes


def get_path(last_node):
    path = [last_node]

    while path[-1].parent != None and (path[-1].x != 0 or path[-1].y != 0):
        path.append(path[-1].parent)

    return [[i.x, i.y] for i in path]


def part2():
    grid = get_input()

    losses = []
    start_coords = [(0, 1), (1, 0)]
    for coord in start_coords:
        all_nodes = new_create_nodes(grid)
        init_nodes(all_nodes)
        nodes = get_node_list(all_nodes)

        #run = 2 => run_inx = 1
        node = all_nodes[coord[0]][coord[1]][1][(0, 0)]
        node.heat_loss = node.current_heat_loss()

        end_node = djisktra(nodes, len(grid) - 1, len(grid[0]) - 1)
        losses.append(end_node.heat_loss)

    total = min(losses) + 1

    print(total)


part2()
class Node:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

        self.working_value = None

    def __eq__(self, other_node):
        return self.x == other_node.x and self.y == other_node.y and self.dir == other_node.dir

    def dist_to(self, other_node):
        if abs(self.x - other_node.x) + abs(self.y - other_node.y) != 1: return None

        dir_diff = self.dir - other_node.dir

        if dir_diff == 2:
            return None
        elif dir_diff == 0:
            return 1
        else:
            return 1001


def get_input():
    with open("day16.txt", "r") as file:
        data = file.read().splitlines()

    return data


def get_dir_step(dir):
    match dir:
        case 0:
            return 0, 1
        case 1:
            return 1, 0
        case 2:
            return 0, -1
        case 3:
            return -1, 0


def get_adjacent_nodes(maze, node, current_nodes, done_nodes):
    adjacent = []
    for dir_offset in range(-1, 2):
        new_dir = (node.dir + dir_offset) % 4
        dx, dy = get_dir_step(new_dir)
        new_x, new_y = node.x + dx, node.y + dy

        if not 0 <= new_x < len(maze) or not 0 <= new_y < len(maze[0]): continue
        if maze[new_x][new_y] == "#": continue

        in_list = False
        adj_node = Node(new_x, new_y, new_dir)

        if adj_node in done_nodes: continue

        for i in current_nodes:
            if i == adj_node:
                adj_node = i
                in_list = True

                break

        if not in_list:
            current_nodes.append(adj_node)

        adjacent.append(adj_node)

    return adjacent


def dijkstra(maze, start_node):
    end_x, end_y = get_char_pos(maze, "E")

    start_node.working_value = 0

    done_nodes = []
    current_nodes = [start_node]

    while len(done_nodes) == 0 or done_nodes[-1].x != end_x or done_nodes[-1].y != end_y:
        current_nodes.sort(key=lambda x: x.working_value)
        current = current_nodes.pop(0)

        done_nodes.append(current)

        adjacent = get_adjacent_nodes(maze, current, current_nodes, done_nodes)

        for i in adjacent:
            new_working_value = current.working_value + current.dist_to(i)
            if i.working_value is None: i.working_value = new_working_value
            else: i.working_value = min(i.working_value, new_working_value)

    return done_nodes


def get_char_pos(maze, char):
    for i, x in enumerate(maze):
        for j, k in enumerate(x):
            if k == char: return i, j


def part1():
    maze = get_input()
    x, y = get_char_pos(maze, "S")

    done_nodes = dijkstra(maze, Node(x, y, 0))

    print(done_nodes[-1].working_value)


part1()


#---------


def get_paths(current_node, done_nodes, current_path, start_pos):
    global all_seats

    if current_node.x == start_pos[0] and current_node.y == start_pos[1]:
        for i in current_path:
            all_seats.add((i.x, i.y))

        return
    
    for i in done_nodes:
        if i == current_node: continue

        dist = current_node.dist_to(i)

        if dist == current_node.working_value - i.working_value:
            get_paths(i, done_nodes, current_path + [i], start_pos)


def part2():
    global all_seats

    maze = get_input()
    x, y = get_char_pos(maze, "S")

    done_nodes = dijkstra(maze, Node(x, y, 0))

    all_seats = set()
    end_node = done_nodes[-1]

    get_paths(end_node, done_nodes, [end_node], (x, y))

    print(len(all_seats))


part2()
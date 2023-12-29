from random import choice


class Node:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

        self.parent = None
        self.dist = None

    is_special = lambda self: len(self.connections) >= 2


def get_input():
    with open("day25.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    final = []
    for i in data:
        a, b = i.split(": ")
        b = b.split(" ")

        final.append([a, b])

    return final


def build_graph(connections):
    node_dict = {}

    for a, b in connections:
        if a not in node_dict:
            node_dict[a] = Node(a, b)
        else:
            for i in b:
                node_dict[a].connections.append(i)
        
        for i in b:
            if i not in node_dict:
                node_dict[i] = Node(i, [a])
            else:
                node_dict[i].connections.append(a)

    return node_dict


def is_in_group(group, a, b):
    if a in group:
        return True
    else:
        for i in b:
            if i in group:
                return True
            
        return False
    

def need_join(a, b):
    for i in a:
        if i in b:
            return True
        
    return False


def check_group_join(groups):
    joined = True
    while joined:
        joined = False

        for i, x in enumerate(groups):
            for j in groups[i + 1:]:
                if need_join(x, j):
                    for y in j:
                        joined = True
                        groups[i].add(y)

                    groups.remove(j)


def get_connected_groups(connections):
    groups = []

    for a, b in connections:
        done = False
        for i in groups:
            if is_in_group(i, a, b):
                i.add(a)

                for x in b:
                    i.add(x)

                done = True
                break

        if not done:
            s = {a}

            for i in b:
                s.add(i)

            groups.append(s)

    check_group_join(groups)

    return groups


def bfs(start_node, end_node, node_dict):
    start_node.dist = 0

    queue = [start_node]
    searched = set()

    dist = 0
    while end_node not in queue:
        dist += 1

        current = queue[0]
        queue.pop(0)

        for i in current.connections:
            child = node_dict[i]

            if child in searched:
                continue

            if child in queue:
                if dist < child.dist:
                    child.parent = current
                    child.dist = dist
            else:
                child.parent = current
                child.dist = dist
                queue.append(child)

            searched.add(current)

    return end_node


def get_path(start_node, end_node):
    path = [end_node]

    while start_node not in path:
        next = path[-1].parent
        path.append(next)

    return path


def reset_nodes(node_dict):
    for i in node_dict.values():
        i.parent = None
        i.dist = None


def get_common(node_dict):
    paths = []

    for _ in range(100):
        reset_nodes(node_dict)

        i = choice(list(node_dict.values()))
        x = choice(list(node_dict.values()))
        
        if i == x:
            continue

        node = bfs(i, x, node_dict)
        path = get_path(i, node)

        paths.append(path)

    freqs = {}
    for i in paths:
        for j, k in enumerate(i):
            if j > 0:
                a = i[j - 1].name
                b = k.name

                if (a, b) in freqs.keys():
                    freqs[(a, b)] += 1
                elif (b, a) in freqs.keys():
                    freqs[(b, a)] += 1
                else:
                    freqs[(a, b)] = 1

    sort_by_value = dict(sorted(freqs.items(), key=lambda item: item[1], reverse=True))

    s = []
    for k, _ in sort_by_value.items():
        s.append(k)

    return s


def remove_from_conns(connections, a, b):
    for i, x in enumerate(connections):
        main, conns = x

        for j, k in enumerate(conns):
            if main == a and k == b:
                return i, j, True
            elif main == b and k == a:
                return i, j, False
            

def remove_connections(connections, num, sorted_connections):
    if num == 3:
        groups = get_connected_groups(connections)

        if len(groups) == 2:
            total = len(groups[0]) * len(groups[1])
            print(total)
            quit()

        return
    
    inx = 0
    for a, b in sorted_connections:
        inx1, inx2, is_normal = remove_from_conns(connections, a, b)
        inx += 1

        connections[inx1][1].pop(inx2)

        remove_connections(connections, num + 1, sorted_connections[inx:])

        if is_normal:
            connections[inx1][1].append(b)
        else:
            connections[inx1][1].append(a)


def part1():
    connections = get_input()
    node_dict = build_graph(connections)

    sorted = get_common(node_dict)
    
    remove_connections(connections, 0, sorted)


part1()
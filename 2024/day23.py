class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.children.append(self)


def get_input():
    with open("day23.txt", "r") as file:
        data = file.read().splitlines()

    return [i.split("-") for i in data]


def get_node(name, node_names):
    if name in node_names:
        return node_names[name]
    else:
        node = Node(name)
        node_names[name] = node

        return node


def build_graph(connections):
    node_names = {}
    for a, b in connections:
        a = get_node(a, node_names)
        b = get_node(b, node_names)

        a.add_child(b)

    return node_names.values()


def complete_triplet(a, b):
    triplets = []
    for i in a.children:
        if i in b.children:
            sorted_triplet = tuple(sorted((a.name, b.name, i.name)))
            triplets.append(sorted_triplet)

    return triplets


def get_triplets(nodes):
    triplets = []
    for a in nodes:
        if a.name[0] != "t": continue

        for b in a.children:
            triplets += complete_triplet(a, b)

    return set(triplets)


def part1():
    connections = get_input()
    nodes = build_graph(connections)
    triplets = get_triplets(nodes)

    print(len(triplets))


part1()


#---------


def get_connected_subgraph(node, connections, checked_nodes):
    max_size = len(connections)
    max_connections = connections

    for i in node.children:
        if len(i.children) < max_size - 1 or i in connections or i in checked_nodes: continue

        is_connected = True
        for x in connections:
            if i not in x.children:
                is_connected = False
                break

        if not is_connected: continue

        checked_nodes.append(i)

        new_size, new_connections = get_connected_subgraph(i, connections + [i], checked_nodes)
        
        if new_size > max_size:
            max_size = new_size
            max_connections = new_connections

    return max_size, max_connections


def part2():
    connections = get_input()
    nodes = build_graph(connections)

    max_size = 0
    max_subgraph = []
    for i in nodes:
        size, subgraph = get_connected_subgraph(i, [i], [])
        
        if size > max_size:
            max_size = size
            max_subgraph = sorted([i.name for i in subgraph])

    print(",".join(max_subgraph))


part2()
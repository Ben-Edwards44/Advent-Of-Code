from math import gcd


class Node:
    def __init__(self, name):
        self.name = name

    def add_children(self, children):
        self.left = children[0]
        self.right = children[1]


def get_input():
    with open("day8.txt", "r") as file:
        data = file.read()

    map, nodes = data.split("\n\n")

    nodes = nodes.split("\n")[:-1]
    
    final_n = []
    for i in nodes:
        parent, children = i.split(" = ")
        children = children[1:-1].split(", ")

        final_n.append([parent, children])

    return map, final_n


def build_nodes(nodes):
    built = {}

    all_nodes = []

    for p, childs in nodes:
        if p in built.keys():
            parent = built[p]
        else:
            parent = Node(p)
            built[p] = parent

        children = []

        for i in childs:
            if i in built.keys():
                c = built[i]
            else:
                c = Node(i)
                built[i] = c

            children.append(c)
        
        parent.add_children(children)

        all_nodes.append(parent)

    return all_nodes


def get_total(map, all_nodes, start):
    total = 0

    current = all_nodes[start]

    while current.name != "ZZZ":
        inst = map[total % len(map)]
        total += 1

        if inst == "R":
            current = current.right
        else:
            current = current.left

    return total


def part1():
    map, node_txt = get_input()
    nodes = build_nodes(node_txt)

    for i, x in enumerate(nodes):
        if x.name == "AAA":
            start = i
            break

    total = get_total(map, nodes, start)

    print(total)


part1()


#------


def new_total(map, all_nodes, start):
    current_node = all_nodes[start]

    total = 0
    while current_node.name[-1] != "Z":
        inst = map[total % len(map)]
        total += 1

        if inst == "R":
            current_node = current_node.right
        else:
            current_node = current_node.left

    return total


def find_lcm(list):
    lcm = 1
    for i in list:
        lcm = lcm * i // gcd(lcm, i)

    return lcm


def part2():
    map, node_txt = get_input()
    nodes = build_nodes(node_txt)

    starts = []
    for i, x in enumerate(nodes):
        if x.name[-1] == "A":
            starts.append(i)

    totals = [new_total(map, nodes, i) for i in starts]
    totals.append(len(map))

    total = find_lcm(totals)

    print(total)


part2()
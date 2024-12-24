class Wire:
    def __init__(self, name):
        self.name = name

        self.value = None

        self.inp1 = None
        self.inp2 = None
        
        self.gate = None

    def set_gate(self, connection, all_wires):
        assert connection[3] == self.name

        self.inp1 = all_wires[connection[0]]
        self.inp2 = all_wires[connection[2]]

        self.gate = connection[1]

    def get_value(self):
        if self.value is not None: return self.value
        
        inp1 = self.inp1.get_value()
        inp2 = self.inp2.get_value()

        if self.gate == "AND":
            self.value = inp1 and inp2
        elif self.gate == "OR":
            self.value = inp1 or inp2
        elif self.gate == "XOR":
            self.value = inp1 ^ inp2
        else:
            raise Exception("Invalid gate")

        return self.value
    
    def get_roots(self):
        if self.name[0] == "x" or self.name[0] == "y": return [self]

        return self.inp1.get_roots() + self.inp2.get_roots()


def get_input():
    with open("day24.txt", "r") as file:
        data = file.read().strip()

    initial, conns = data.split("\n\n")

    conns = conns.splitlines()
    initial = initial.splitlines()

    initial_values = []
    for i in initial:
        name, val = i.split(": ")
        initial_values.append([name, int(val)])

    connections = []
    for i in conns:
        inp1, gate, inp2, _, out = i.split(" ")

        connections.append([inp1, gate, inp2, out])

    return initial_values, connections


def build_wires(initial_values, connections):
    all_wires = {}
    for inp1, _, inp2, out in connections:
        if inp1 not in all_wires:
            all_wires[inp1] = Wire(inp1)
        if inp2 not in all_wires:
            all_wires[inp2] = Wire(inp2)
        if out not in all_wires:
            all_wires[out] = Wire(out)

    for name, value in initial_values:
        all_wires[name].value = value

    for i in connections:
        out = i[3]
        all_wires[out].set_gate(i, all_wires)

    return all_wires


def get_num(all_wires):
    z_wires = sorted([i for i in all_wires.keys() if i[0] == "z"])

    bin_num = ""
    for i in z_wires:
        bit = str(all_wires[i].get_value())

        bin_num = f"{bit}{bin_num}"

    return bin_num


def part1():
    initial, connections = get_input()
    all_wires = build_wires(initial, connections)

    bin_num = get_num(all_wires)

    print(int(bin_num, 2))


part1()


#------------


def reset_wires(all_wires):
    for i in all_wires.values():
        i.value = None


def set_initial(x_num, y_num, all_wires):
    while len(x_num) < 45:
        x_num = f"0{x_num}"
    while len(y_num) < 45:
        y_num = f"0{y_num}"

    for i, x in enumerate(x_num[::-1]):
        name = f"x{i}" if i >= 10 else f"x0{i}"
        all_wires[name].value = int(x)

    for i, x in enumerate(y_num[::-1]):
        name = f"y{i}" if i >= 10 else f"y0{i}"
        all_wires[name].value = int(x)


def get_bad_bits(all_wires):
    bad = []
    for i in range(1, 45):
        if len(bad) == 0:
            num = "1" * i
        else:
            num = "1" * (i - bad[-1]) + "0" * bad[-1]
        
        reset_wires(all_wires)
        set_initial(num, num, all_wires)

        result = get_num(all_wires)

        if int(result, 2) != 2 * int(num, 2): bad.append(i)

    return bad


def xor_output_swap(all_wires, bad_bit):
    #the output must be an XOR
    name = f"{bad_bit}" if bad_bit >= 10 else f"0{bad_bit}"

    if all_wires[f"z{name}"].gate == "XOR": return None, None

    for i in all_wires.values():
        if i.gate == "XOR":
            op1 = i.inp1.name == f"x{name}" and i.inp2.name == f"y{name}"
            op2 = i.inp1.name == f"y{name}" and i.inp2.name == f"x{name}"

            if op1 or op2:
                xor_operand = i
                break

    for i in all_wires.values():
        if i.gate == "XOR" and (i.inp1 == xor_operand or i.inp2 == xor_operand):
            swap_with = i
            break

    return f"z{name}", swap_with.name


def prev_carry_swap(all_wires, bad_carry):
    #if it is not the xor output swap, it is a problem with the previous carry
    name = f"{bad_carry}" if bad_carry >= 10 else f"0{bad_carry}"

    for i in all_wires.values():
        if i.gate is None: continue

        op1 = i.inp1.name == f"x{name}" and i.inp2.name == f"y{name}"
        op2 = i.inp1.name == f"y{name}" and i.inp2.name == f"x{name}"

        if op1 or op2:
            if i.gate == "XOR":
                swap1 = i
            elif i.gate == "AND":
                swap2 = i
    
    return swap1.name, swap2.name



def swap_wire(a, b, all_wires):
    a = all_wires[a]
    b = all_wires[b]

    a.inp1, b.inp1 = b.inp1, a.inp1
    a.inp2, b.inp2 = b.inp2, a.inp2  
    a.gate, b.gate = b.gate, a.gate


def part2():
    #NOTE: I had to make some assumptions about my input to get this to work, it may not work on every input.
    initial, connections = get_input()
    all_wires = build_wires(initial, connections)

    bad_bits = get_bad_bits(all_wires)

    wires_involved = []
    while len(bad_bits) > 0:
        bit = bad_bits[0]

        a, b = xor_output_swap(all_wires, bit)

        if a is None and b is None:
            a, b = prev_carry_swap(all_wires, bit - 1)

        wires_involved.append(a)
        wires_involved.append(b)

        swap_wire(a, b, all_wires)

        bad_bits = get_bad_bits(all_wires)

    print(",".join(sorted(wires_involved)))


part2()
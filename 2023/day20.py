class Module:
    def __init__(self, name, broad_to) -> None:
        self.name = name
        self.broad_to = broad_to

        self.all_modules = {}

    def update_scores(self, high_pulse):
        global highs, lows

        if high_pulse:
            highs += 1
        else:
            lows += 1


class FlipFlop(Module):
    def __init__(self, name, broad_to):
        super().__init__(name, broad_to)

        self.on = False

    def recieve(self, high_pulse, send_name):
        self.update_scores(high_pulse)

        if not high_pulse:
            send_pulse = not self.on
            self.on = not self.on

            return self.broad_to, send_pulse
        
        return [], high_pulse


class Conjunction(Module):
    def __init__(self, name, broad_to):
        super().__init__(name, broad_to)

        self.prev_high_pulses = {}

    def recieve(self, high_pulse, send_name):
        self.update_scores(high_pulse)

        if send_name not in self.prev_high_pulses.keys():
            raise Exception("not init properly")
        
        self.prev_high_pulses[send_name] = high_pulse

        for i in self.prev_high_pulses.values():
            if not i:
                return self.broad_to, True
            
        return self.broad_to, False


class Broadcast(Module):
    def __init__(self, name, broad_to):
        super().__init__(name, broad_to)

    def recieve(self, high_pulse, send_name):
        self.update_scores(high_pulse)

        return self.broad_to, high_pulse


def get_input():
    with open("day20.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    types = {"%" : FlipFlop, "&" : Conjunction}

    modules = {}
    for i in data:
        name, broad = i.split(" -> ")

        broad = broad.split(", ")

        if name == "broadcaster":
            new = Broadcast(name, broad)
        else:
            type = name[0]
            n = name[1:]

            new = types[type](n, broad)

        modules[new.name] = new

    return modules


def init_conj(modules):
    conj = set()

    for i in modules.values():
        i.all_modules = modules

        if type(i) == Conjunction:
            conj.add(i.name)

    d = {i : [] for i in conj}

    for i in modules.values():
        for x in i.broad_to:
            if x in conj:
                d[x].append(i.name)

    for i in modules.values():
        if type(i) == Conjunction:
            i.prev_high_pulses = {x : False for x in d[i.name]}


def button_press(modules):
    global highs, lows

    mod, pulse = modules["broadcaster"].recieve(False, None)

    queue = [[i, pulse, "broadcaster"] for i in mod]

    while len(queue) > 0:
        current_name, pulse, send_name = queue[0]
        queue.pop(0)

        try:
            current = modules[current_name]
        except KeyError:
            if pulse:
                highs += 1
            else:
                lows += 1

            continue

        new_send_name = current_name
        new_names, new_pulse = current.recieve(pulse, send_name)

        for i in new_names:
            queue.append([i, new_pulse, new_send_name])


def part1():
    global highs, lows

    highs = 0
    lows = 0

    modules = get_input()

    init_conj(modules)

    for _ in range(1000):
        button_press(modules)

    total = highs * lows

    print(total)


part1()


#-------

#Did not manage part 2
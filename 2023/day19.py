class Rule:
    def __init__(self, name, condition_str):
        self.name = name

        self.parse_str(condition_str)

    def parse_str(self, condition_str):
        condition_str = condition_str[1:-1]
        rules = []

        for i, x in enumerate(condition_str.split(",")):
            if i == len(condition_str.split(",")) - 1:
                self.final = x
                break

            cond, result = x.split(":")

            type = cond[0]
            op = cond[1]
            num = int(cond[2:])

            rules.append([type, op, num, result])

        self.rules = rules

    def do_rules(self, part):
        #part is dict
        for type, op, num, result in self.rules:
            part_num = part[type]

            if part_num < num and op == "<" or part_num > num and op == ">":
                return result
            
        return self.final
    

def get_input():
    with open("day19.txt", "r") as file:
        data = file.read()[:-1]

    rules, parts = data.split("\n\n")

    part_dicts = []
    for i in parts.split("\n"):
        part = i[1:-1].split(",")
        part_dict = {}

        for x in part:
            type, num = x.split("=")

            part_dict[type] = int(num)

        part_dicts.append(part_dict)

    r_name = []
    for i in rules.split("\n"):
        name = ""
        for x in i:
            if x == "{":
                break
            else:
                name += x

        r_name.append([name, i[len(name):]])

    return r_name, part_dicts


def build_rules(r_name):
    rules = {}
    for name, rule in r_name:
        r = Rule(name, rule)
        rules[name] = r

    return rules


def check_part(part_dict, rules):
    current_rule = rules["in"]

    while True:
        next = current_rule.do_rules(part_dict)

        if next == "A":
            return True
        elif next == "R":
            return False
        else:
            current_rule = rules[next]


def get_total(part_dicts, rules):
    total = 0

    for i in part_dicts:
        if check_part(i, rules):
            total += i["x"] + i["m"] + i["a"] + i["s"]

    return total


def part1():
    r_name, part_dicts = get_input()
    rules = build_rules(r_name)

    total = get_total(part_dicts, rules)

    print(total)


part1()


#--------


def combs_from_bounds(bounds):
    combs = 1
    
    for min, max in bounds:
        if min > max:
            return 0

        combs *= max - min + 1

    return combs


def get_combs(rule, bounds, rule_names):
    inxs = ["x", "m", "a", "s"]
    bounds = [[x for x in i] for i in bounds]

    total_combs = 0
    for type, op, num, result in rule.rules:
        bound_inx = inxs.index(type)

        if op == "<":
            prev_upper = bounds[bound_inx][1]
            bounds[bound_inx][1] = min(bounds[bound_inx][1], num - 1)
        else:
            prev_lower = bounds[bound_inx][0]
            bounds[bound_inx][0] = max(bounds[bound_inx][0], num + 1)

        if result == "A":
            total_combs += combs_from_bounds(bounds)
        elif result != "R":
            new_rule = rule_names[result]
            total_combs += get_combs(new_rule, bounds, rule_names)

        if op == "<":
            bounds[bound_inx][1] = prev_upper
            bounds[bound_inx][0] = max(bounds[bound_inx][0], num)
        else:
            bounds[bound_inx][1] = min(bounds[bound_inx][1], num)
            bounds[bound_inx][0] = prev_lower

    if rule.final == "A":
        total_combs += combs_from_bounds(bounds)
    elif rule.final != "R":
        new_rule = rule_names[rule.final]
        total_combs += get_combs(new_rule, bounds, rule_names)

    return total_combs


def part2():
    r_name, _ = get_input()
    rules = build_rules(r_name)

    bounds = [[1, 4000], [1, 4000], [1, 4000], [1, 4000]]
    total = get_combs(rules["in"], bounds, rules)

    print(total)


part2()
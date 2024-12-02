def get_input():
    with open("day2.txt", "r") as file:
        data = file.read().split("\n")[:-1]

    return [[int(x) for x in i.split(" ")] for i in data]


def check_report(report):
    if len(report) <= 1:
        return True
    
    inc = report[1] > report[0]
    for i, x in enumerate(report):
        if i == 0:
            continue

        diff = x - report[i - 1]

        if diff == 0 or diff < -3 or diff > 3:
            return False
        
        if (diff > 0) != inc:
            return False
        
    return True


def part1():
    reports = get_input()

    total = 0
    for i in reports:
        if check_report(i):
            total += 1

    print(total)


part1()


#-------


def new_check_safe(report):
    if check_report(report):
        return True

    for i in range(len(report)):
        if check_report(report[:i] + report[i + 1:]):
            return True
        
    return False
        

def part2():
    reports = get_input()

    total = 0
    for i in reports:
        if new_check_safe(i):
            total += 1

    print(total)


part2()
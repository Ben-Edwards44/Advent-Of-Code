def get_input():
    with open("day7.txt", "r") as file:
        data = file.read().splitlines()

    tests = []
    nums = []
    for i in data:
        t, n = i.split(": ")

        tests.append(int(t))
        nums.append([int(x) for x in n.split(" ")])

    return tests, nums


def evaluate(nums, ops):
    result = nums[0]

    for i in range(1, len(nums)):
        if ops[i - 1] == "+":
            result += nums[i]
        elif ops[i - 1] == "*":
            result *= nums[i]
        else:
            result = int(str(result) + str(nums[i]))

    return result


def is_possible(test, nums, ops, possible_ops):
    current = evaluate(nums[:len(ops) + 1], ops)

    if len(ops) >= len(nums) - 1:
        return current == test
    elif current > test:
        return False
    
    for i in possible_ops:
        works = is_possible(test, nums, ops + [i], possible_ops)
    
        if works:
            return True

    return False


def part1():
    tests, nums = get_input()

    total = 0
    for i, x in zip(tests, nums):
        if is_possible(i, x, [], ("*", "+")):
            total += i

    print(total)


part1()


#-----


def part2():
    tests, nums = get_input()

    total = 0
    for i, x in zip(tests, nums):
        if is_possible(i, x, [], ("*", "+", "||")):
            total += i

    print(total)


part2()
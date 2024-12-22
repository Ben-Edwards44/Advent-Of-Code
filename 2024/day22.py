def get_input():
    with open("day22.txt", "r") as file:
        data = file.read().splitlines()

    return [int(i) for i in data]


mix = lambda secret, value: secret ^ value
prune = lambda secret: secret % 16777216


def process1(secret):
    secret = mix(secret << 6, secret)

    return prune(secret)


def process2(secret):
    secret = mix(secret >> 5, secret)

    return prune(secret)


def process3(secret):
    secret = mix(secret << 11, secret)

    return prune(secret)


next_secret_num = lambda secret: process3(process2(process1(secret)))


def part1():
    nums = get_input()

    total = 0
    for i in nums:
        for _ in range(2000):
            i = next_secret_num(i)

        total += i

    print(total)


part1()


#------


def get_price_changes(secret):
    prev = secret

    prices = []
    changes = []
    for _ in range(2000):
        new = next_secret_num(prev)
        changes.append(new % 10 - prev % 10)
        prices.append(new % 10)

        prev = new

    return changes, prices


def evaluate_changes(price_changes, prices, group_totals):
    seen = set()
    for i in range(0, len(price_changes) - 3):
        buy_price = prices[i + 3]
        change_sequence = tuple(price_changes[i + x] for x in range(4))

        if change_sequence in seen: continue
        seen.add(change_sequence)

        if change_sequence in group_totals:
            group_totals[change_sequence] += buy_price
        else:
            group_totals[change_sequence] = buy_price


def part2():
    nums = get_input()

    group_totals = {}
    for i in nums:
        changes, prices = get_price_changes(i)

        evaluate_changes(changes, prices, group_totals)

    best = max(group_totals.values())

    print(best)


part2()
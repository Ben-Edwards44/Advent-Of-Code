CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def get_input():
    with open("day7.txt", "r") as file:
        data = file.read()

    data = data.split("\n")[:-1]

    hands = []
    for i in data:
        card, bid = i.split(" ")
        hands.append([card, int(bid)])

    return hands


def get_type(cards):
    counts = {}

    for i in cards:
        if i in counts.keys():
            counts[i] += 1
        else:
            counts[i] = 1

    values = sorted(counts.values(), reverse=True)

    if values[0] == 5:
        return 7
    elif values[0] == 4:
        return 6
    elif values[0] == 3 and values[1] == 2:
        return 5
    elif values[0] == 3:
        return 4
    elif values[0] == 2 and values[1] == 2:
        return 3
    elif values[0] == 2:
        return 2
    else:
        return 1
    

def get_card_num(card, all_cards):
    inx = all_cards.index(card)

    return len(all_cards) - inx


def score_hand(cards):
    type = get_type(cards)

    max_pwr = len(cards)

    score = len(CARDS)**max_pwr * type

    for i, x in enumerate(cards):
        mult = len(CARDS)**(max_pwr - i - 1)
        score += get_card_num(x, CARDS) * mult

    return score


def get_total(scores):
    scores = sorted(scores, key=lambda x: x[2])

    rank = 1
    total = 0

    for _, bid, _ in scores:
        total += bid * rank
        rank += 1

    return total


def part1():
    hands = get_input()

    scores = [[hand, bid, score_hand(hand)] for hand, bid in hands]
    
    print(get_total(scores))


part1()


#------


NEW_CARDS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def new_type(cards):
    counts = {}

    j_count = 0
    for i in cards:
        if i == "J":
            j_count += 1
        elif i in counts.keys():
            counts[i] += 1
        else:
            counts[i] = 1

    values = sorted(counts.values(), reverse=True)

    if j_count == len(cards):
        return 7

    max_same = values[0] + j_count

    if max_same == 5:
        return 7
    elif max_same == 4:
        return 6
    elif max_same == 3 and values[1] == 2:
        return 5
    elif max_same == 3:
        return 4
    elif max_same == 2 and values[1] == 2:
        return 3
    elif max_same == 2:
        return 2
    else:
        return 1
    

def new_score_hand(cards):
    type = new_type(cards)

    max_pwr = len(cards)

    score = len(NEW_CARDS)**max_pwr * type

    for i, x in enumerate(cards):
        mult = len(NEW_CARDS)**(max_pwr - i - 1)
        score += get_card_num(x, NEW_CARDS) * mult

    return score


def part2():
    hands = get_input()

    scores = [[hand, bid, new_score_hand(hand)] for hand, bid in hands]
    
    print(get_total(scores))


part2()
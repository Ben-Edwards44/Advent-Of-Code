def get_input():
    with open("day9.txt", "r") as file:
        data = file.read().strip()

    return [int(i) for i in data]


def move_file(to_inx, start_move_inx, array):
    for i in range(start_move_inx, -1, -1):
        if array[i] != -1:
            from_inx = i
            break

        if i <= to_inx: return False, None

    array[to_inx], array[from_inx] = array[from_inx], -1

    return True, from_inx


def move_all_files(array):
    start_move_inx = len(array) - 1
    for front, item in enumerate(array):
        if item == -1:
            moved, start_move_inx = move_file(front, start_move_inx, array)

            if not moved: return


def create_array(files):
    array = []
    for i, x in enumerate(files):
        if i % 2 == 0:
            id = i // 2
        else:
            id = -1

        array += [id for _ in range(x)]

    return array


def part1():
    files = get_input()
    array = create_array(files)
    
    move_all_files(array)

    total = sum(i * x for i, x in enumerate(array) if x != -1)

    print(total)


part1()


#--------


class Block:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.is_empty = id == -1

    def __repr__(self):
        s = str(self.id) if not self.is_empty else "."
        return s * self.size


def move_block(moving_inx, blocks):
    moving_block = blocks[moving_inx]

    for i, x in enumerate(blocks):
        if i >= moving_inx: return

        if x.is_empty and x.size >= moving_block.size:
            blocks[moving_inx] = Block(-1, moving_block.size)
            blocks.insert(i, moving_block)
            x.size -= moving_block.size

            return


def move_all_blocks(blocks, final_id):
    move_id = final_id
    for i in range(len(blocks) - 1, -1, -1):
        block = blocks[i]

        if block.id == move_id:
            move_block(i, blocks)
            move_id -= 1


def create_blocks(files):
    blocks = []

    final_id = 0
    for i, x in enumerate(files):
        if i % 2 == 0:
            id = i // 2
            final_id = id
        else:
            id = -1

        blocks.append(Block(id, x))

    return blocks, final_id


def part2():
    files = get_input()
    blocks, final_id = create_blocks(files)

    move_all_blocks(blocks, final_id)

    pos = 0
    total = 0
    for i in blocks:
        if i.is_empty:
            id = 0
        else:
            id = i.id

        for _ in range(i.size):
            total += id * pos
            pos += 1

    print(total)


part2()
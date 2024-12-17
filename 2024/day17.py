import re


def get_input():
    with open("t.txt", "r") as file:
        data = file.read().strip()

    registers, program = data.split("\n\n")

    registers = [int(re.findall(r"[0-9]+", i)[0]) for i in registers.splitlines()]
    program = [int(i) for i in re.findall(r"[0-9]+", program)]

    return registers, program


def get_combo_operand(registers, combo_operand):
    if combo_operand <= 3 or combo_operand == 7: return combo_operand
    else: return registers[combo_operand - 4]


def run_command(registers, opcode, literal_operand, inst_pointer, output):
    combo_operand = get_combo_operand(registers, literal_operand)

    match opcode:
        case 0:
            registers[0] = int(registers[0] / 2**combo_operand)
        case 1:
            registers[1] = registers[1] ^ literal_operand
        case 2:
            registers[1] = combo_operand % 8
        case 3:
            if registers[0] != 0:
                inst_pointer = literal_operand - 2
        case 4:
            registers[1] = registers[1] ^ registers[2]
        case 5:
            output.append(combo_operand % 8)
        case 6:
            registers[1] = int(registers[0] / 2**combo_operand)
        case 7:
            registers[2] = int(registers[0] / 2**combo_operand)

    return inst_pointer


def run_program(registers, program):
    inst_pointer = 0
    output = []

    while inst_pointer < len(program):
        opcode, operand = program[inst_pointer], program[inst_pointer + 1]
        
        inst_pointer = run_command(registers, opcode, operand, inst_pointer, output)

        inst_pointer += 2

    return output


def part1():
    registers, program = get_input()
    output = run_program(registers, program)

    print(",".join([str(i) for i in output]))


part1()


#-------


def get_single_output(registers, program):
    output = []
    for i in range(0, len(program), 2):
        opcode, operand = program[i], program[i + 1]
        run_command(registers, opcode, operand, 0, output)

        if opcode == 5: return output[0]


def get_lookup_table(registers, program):
    table = [[] for _ in range(8)]
    repeat_after = 2**10

    for a in range(repeat_after):
        registers[0] = a
        output = get_single_output(registers, program)

        bin_num = bin(a)[2:]
        while len(bin_num) < 10:
            bin_num = "0" + bin_num

        table[output].append(bin_num)

    return table


def get_a(lookup_table, desired_output, current_bits):
    if len(desired_output) == 0:
        print(int(current_bits, 2))
        quit()
    
    prev_bits = current_bits[-7:] if len(current_bits) != 0 else None
    possible = lookup_table[desired_output[-1]]

    for i in possible:
        if prev_bits is None:
            appended_bits = i
        else:
            if i[:7] != prev_bits: continue
            appended_bits = current_bits + i[7:]

        get_a(lookup_table, desired_output[:-1], appended_bits)


def part2():
    #In order for this to work, I made certain assumptions about the input. It works for my input and for the example, so hopefully it works for all inputs
    registers, program = get_input()
    lookup_table = get_lookup_table(registers, program)

    get_a(lookup_table, program, "")


part2()
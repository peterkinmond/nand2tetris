import os
import sys

output = []

def main():
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    print('Populating symbol table')
    with open(filepath) as fp:
        line_number = 0
        for line in fp:
            line = preprocess_line(line)
            if line.startswith('//') or line == '':
                continue
            elif line.startswith('('):
                process_label(line, line_number)
            elif line.startswith('@'):
                process_symbol(line)
                line_number += 1
            else: # C-instruction
                line_number += 1

    process_custom_symbols()

    print('Processing all instructions (converting to binary code)')
    with open(filepath) as fp:
        line_number = 1
        for line in fp:
            line = preprocess_line(line)
            print("Line {} contents {}".format(line_number, line))
            processed_line = process_line(line)
            print(processed_line)
            line_number += 1

    # Print output program
    print("Binary code output")
    for item in output:
        print(item)

    hack_filepath = os.path.splitext(filepath)[0] + ".hack"
    print("Writing code output to file: {}".format(hack_filepath))
    with open(hack_filepath, 'w') as hack_fp:
        for line in output:
            hack_fp.write(line + '\n')

def preprocess_line(line):
    # Remove all comments, even from mid-line
    result = line.split('//')[0]
    result = result.strip()
    return result

def process_symbol(line):
    symbol = line.replace('@', '')
    if symbol in symbols.keys():
        return
    elif symbol.isdigit():
        return

    # Placeholder value will be replaced when we get the label's line number
    symbols[symbol] = "PLACEHOLDER"
    print(symbol)

def process_label(line, line_number):
    symbol = line.replace('(', '').replace(')', '')
    symbols[symbol] = line_number

def process_custom_symbols():
    address = 16 # Custom symbols start at address 16
    for symbol, value in symbols.items():
        if value == 'PLACEHOLDER':
            symbols[symbol] = address
            address += 1

def process_line(line):
    if line == '':
        return 'Empty line'
    elif line.startswith('('):
        return 'Label line'
    elif line.startswith('@'):
        a_instruction = process_a_instruction(line)
        output.append(a_instruction)
        return "A-instruction: {}".format(a_instruction)
    else:
        c_instruction = process_c_instruction(line)
        output.append(c_instruction)
        return "C-instruction: {}".format(c_instruction)

def process_a_instruction(inst):
    # A-instruction is 1-bit op code then 15 bits data value
    # For example:  0000000000000010 = @R2 = @2

    result = inst.replace("@", "")

    if result in symbols.keys():
        # Built-in symbol (R1, KBD, etc)
        result = symbols[result]

    # Convert int value to binary
    result = bin(int(result))[2:]

    # Pad front with zeros until we reach 16 bits
    while len(result) < 16:
        result = '0' + result
    return result

def process_c_instruction(inst):
    # C-instruction is:
    # 1-bit op code, 2 bits unused
    # 7 bits computation (a bit and 6 ALU control bits)
    # 3 bits destination (A, D, M registers)
    # 3 bits jump
    # dest = comp; jump (dest and jump are optional)

    dest_asm = comp_asm = jump_asm = ''
    dest_bin = comp_bin = jump_bin = ''

    jump_split = inst.split(';')
    dest_cont = jump_split[0]
    if len(jump_split) == 2: # has jump portion
        jump_asm = jump_split[1].strip()

    dest_split = dest_cont.split('=')
    if len(dest_split) == 2: # has dest portion
        dest_asm = dest_split[0]
        comp_asm = dest_split[1]
    else:
        comp_asm = dest_split[0]

    dest_bin = process_dest(dest_asm)
    comp_bin = comp[comp_asm]
    jump_bin = jump[jump_asm]

    op_code = '111' # Op code plus unused bits
    result = op_code + comp_bin + dest_bin + jump_bin
    return result

def process_dest(dest_asm):
    # The dest bits are the A, D, and M registers
    # null = '000', ADM = '111, etc
    dest_A = '1' if 'A' in dest_asm else '0'
    dest_D = '1' if 'D' in dest_asm else '0'
    dest_M = '1' if 'M' in dest_asm else '0'
    return dest_A + dest_D + dest_M

symbols = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}

jump = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

# This hash returns full 7-bit comp value
# 1 bit for a + 6 bits for c1 - c6
comp = {
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    'M':   '1110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '!M':  '1110001',
    '-D':  '0001111',
    '-A':  '0110011',
    '-M':  '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

if __name__ == '__main__':
    main()

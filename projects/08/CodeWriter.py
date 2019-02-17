import Constants

class CodeWriter:
    def __init__(self, output_filepath):
        self.output_filepath = output_filepath
        self.output_file = open(output_filepath, 'w')
        self.label_counter = 0

    # Writes to the output_file the assembly code that implements the given
    # arithmetic command
    def write_arithmetic(self, command):
        result = []
        if command in ['add', 'sub', 'and', 'or']:
            result = self.convert_builtin_operator_command(command)
        elif command in ['eq', 'gt', 'lt']:
            result = self.convert_comparison_command(command)
        elif command == 'neg':
            result = self.convert_neg_command()
        elif command == 'not':
            result = self.convert_not_command()
        else:
            raise Exception("Command '{}' not handled".format(command))

        for line in result:
            self.output_file.write(line + '\n')

    # Writes to the output_file the assembly code that implements the given
    # command, where command is either C_PUSH or C_POP
    def write_push_pop(self, command, segment, index):
        if command == Constants.C_PUSH:
            result = self.convert_push_command(command, segment, index)
        elif command == Constants.C_POP:
            result = self.convert_pop_command(command, segment, index)
        else:
            raise Exception("Command '{}' not handled".format(command))

        for line in result:
            self.output_file.write(line + '\n')

    # Handle add, sub, and, or commands
    # Since they're all the same except for operator
    def convert_builtin_operator_command(self, command_type):
        return \
            ["// {}".format(command_type)] + \
            self.decrement_sp() + \
            self.d_equals_star_sp() + \
            self.decrement_sp() + \
            self.star_sp_equals_star_sp_operator_d(command_type) + \
            self.increment_sp()

    def convert_neg_command(self):
        return \
            ['// neg'] + \
            self.decrement_sp() + \
            self.star_sp_equals_neg_star_sp() + \
            self.increment_sp()

    def convert_not_command(self):
        return \
            ['// not'] + \
            self.decrement_sp() + \
            self.star_sp_equals_not_star_sp() + \
            self.increment_sp()

    # Handle eq, gt, lt commands
    # Since they're all the same except for jump condition
    def convert_comparison_command(self, command_type):
        return \
            ["// {}".format(command_type)] + \
            self.decrement_sp() + \
            self.d_equals_star_sp() + \
            self.decrement_sp() + \
            self.star_sp_equals_star_sp_command_d(command_type) + \
            self.increment_sp()

    def convert_push_command(self, command, segment, index):
        if segment == "constant":
            return \
                ["// {} {} {}".format(command, segment, index)] + \
                self.star_sp_equals_index(index) + \
                self.increment_sp()

        if segment == "pointer" or segment == "static":
            return \
                ["// {} {} {}".format(command, segment, index)] + \
                self.star_sp_equals_segment(segment, index) + \
                self.increment_sp()

        return \
            ["// {} {} {}".format(command, segment, index)] + \
            self.addr_equals_segment_plus_i(segment, index) + \
            self.star_sp_equals_star_addr() + \
            self.increment_sp()

    def convert_pop_command(self, command, segment, index):
        if segment == "pointer" or segment == "static":
            return \
                ["// {} {} {}".format(command, segment, index)] + \
                self.decrement_sp() + \
                self.segment_equals_star_sp(segment, index)

        return \
            ["// {} {} {}".format(command, segment, index)] + \
            self.addr_equals_segment_plus_i(segment, index) + \
            self.decrement_sp() + \
            self.star_addr_equals_star_sp()

    def segment_equals_star_sp(self, segment, index):
        return [
            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@' + self.get_segment_type(segment, index), # segment = D
            'M=D'
        ]

    def addr_equals_segment_plus_i(self, segment, index):
        return [
            '@' + self.get_segment_type(segment, index), # D = segment + i
            self.set_d(segment),
            '@' + str(index),
            'D=D+A',
            '@R13', # addr = D, store for later
            'M=D',
        ]

    def set_d(self, segment):
        # For temp segment we use value 5 (stored as address)
        # rather than the memory address at that value
        if segment == 'temp':
            return 'D=A'
        else:
            return 'D=M'

    def increment_sp(self):
        return [
            '@SP', # SP++
            'M=M+1',
        ]

    def decrement_sp(self):
        return [
            '@SP', # SP--
            'M=M-1',
        ]

    def star_sp_equals_star_addr(self):
        return [
            '@R13', # D = *addr
            'A=M',
            'D=M',

            '@SP', # *SP = D
            'A=M',
            'M=D',
        ]

    def star_addr_equals_star_sp(self):
        return [
            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@R13', # *addr = D
            'A=M',
            'M=D',
        ]

    def star_sp_equals_neg_star_sp(self):
        return [
            '@SP', # *SP = -*SP
            'A=M',
            'M=-M',
        ]

    def star_sp_equals_not_star_sp(self):
        return [
            '@SP', # *SP = !*SP
            'A=M',
            'M=!M',
        ]

    def star_sp_equals_index(self, index):
        return [
            '@' + str(index), # *SP = i
            'D=A', # Get address value, not memory value
            '@SP',
            'A=M',
            'M=D',
        ]

    def star_sp_equals_segment(self, segment, index):
        return [
            '@' + self.get_segment_type(segment, index), # D = segment
            'D=M',

            '@SP', # *SP = D
            'A=M',
            'M=D',
        ]

    def d_equals_star_sp(self):
        return [
            '@SP', # D = *SP
            'A=M',
            'D=M',
        ]

    def star_sp_equals_star_sp_operator_d(self, command_type):
        return [
            '@SP', # *SP = *SP - D
            'A=M',
            'M=M' + self.get_operator(command_type) + 'D',
        ]

    def star_sp_equals_star_sp_command_d(self, command_type):
        # TODO: Less hacky way to ensure labels are unique?
        self.label_counter += 1

        return [
            '@SP', # *SP = *SP - D
            'A=M',
            'M=M-D',
            'D=M', # if M > 0

            "@SETTRUE{}".format(self.label_counter),
            'D;' + self.get_jump_type(command_type),

            "(SETFALSE{})".format(self.label_counter),
            '@SP',
            'A=M',
            'M=0', # false
            "@FINISH{}".format(self.label_counter),
            '0;JMP',

            "(SETTRUE{})".format(self.label_counter),
            '@SP',
            'A=M',
            'M=-1', # true
            "@FINISH{}".format(self.label_counter),
            '0;JMP',

            "(FINISH{})".format(self.label_counter),
        ]

    def get_operator(self, command_type):
        return {
            'add': '+',
            'sub': '-',
            'and': '&',
            'or':  '|'
        }[command_type]

    def get_jump_type(self, command_type):
        return {
            'gt': 'JGT',
            'lt': 'JLT',
            'eq': 'JEQ',
        }[command_type]

    def get_segment_type(self, segment, index):
        if (segment == 'pointer'):
            return ['THIS', 'THAT'][index]

        if (segment == 'static'):
            return self.get_static_segment_type(segment, index)

        segment_types = {
            'local': 'LCL',
            'argument': 'ARG',
            'temp': '5',
            'this': 'THIS',
            'that': 'THAT',
        }
        return segment_types[segment]

    def get_static_segment_type(self, segment, index):
        # Figure out name of the fuxkin thing
        vm_filename = self.output_filepath.split("/")[-1].split(".")[0]
        return "{}.{}".format(vm_filename, index)

    def close(self):
        self.output_file.close()


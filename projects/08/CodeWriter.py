import Constants

class CodeWriter:
    def __init__(self, output_filepath):
        self.output_filepath = output_filepath
        self.output_file = open(output_filepath, 'w')
        self.filename_no_extension = self.output_file.name.split(".")[0]
        self.label_counter = 0
        self.return_label_counter = 1

    # Informs the CodeWriter that the translation of a new VM file
    # has started
    def set_file_name(self, filename):
        pass

    # Writes the assembly instructions that effect the bootstrap code
    # that initializes the VM. This code must be placed at the beginning
    # of the generated *.asm file
    def write_init(self):
        # Boostrap code is:
        # SP = 256
        # call Sys.init

        sp_equals_256 = [
            '@256',
            'D=A',
            '@SP',
            'M=D'
        ]
        for line in sp_equals_256:
            self.output_file.write(line + '\n')

        self.write_call('Sys.init', 0)

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

    # Writes assembly code that effects the label command.
    def write_label(self, label):
        for line in self.convert_label_command(label):
            self.output_file.write(line + '\n')

    # Writes assembly code that effects the goto command.
    def write_goto(self, label):
        for line in self.convert_goto_command(label):
            self.output_file.write(line + '\n')

    # Writes assembly code that effects the if-goto command.
    def write_if(self, label):
        for line in self.convert_if_goto_command(label):
            self.output_file.write(line + '\n')

    # Writes assembly code that effects the function command.
    def write_function(self, function_name, num_vars):
        for line in self.convert_function_command(function_name, num_vars):
            self.output_file.write(line + '\n')

    # Writes assembly code that effects the call command.
    def write_call(self, function_name, num_args):
        for line in self.convert_call_command(function_name, num_args):
            self.output_file.write(line + '\n')

    # Writes assembly code that effects the return command.
    def write_return(self):
        for line in self.convert_return_command():
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

    def convert_push_segment(self, segment):
        return \
            ["// push {}".format(segment)] + \
            self.star_sp_equals_segment(segment) + \
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
            self.star_addr_equals_star_sp('R13') # Use R13 as temp storage

    def convert_label_command(self, label):
        return [
            "// label {}".format(label),
            "({})".format(label)
        ]

    def convert_goto_command(self, label):
        return [
            "// goto {}".format(label),
            "@{}".format(label),
            '0;JMP',
        ]

    def convert_if_goto_command(self, label):
        return \
            ["// if-goto {}".format(label)] + \
            self.decrement_sp() + \
            self.d_equals_star_sp() + \
            ["@{}".format(label),
            'D;JNE']

    def convert_function_command(self, function_name, num_vars):
        result = \
            ["// function {} {}".format(function_name, num_vars)] + \
            ["({})".format(function_name)]
        for x in range(0, num_vars):
            result += self.convert_push_command(Constants.C_PUSH, 'constant', 0)
        return result

    def convert_call_command(self, function_name, num_args):
        # Format for return address label is "Filename$ret.1"
        return_address_label = "{}$ret.{}".format(self.filename_no_extension, self.return_label_counter)
        self.return_label_counter += 1

        return \
            ["// call {} {}".format(function_name, num_args)] + [ \
            "// push {}".format(return_address_label),
            "@{}".format(return_address_label),
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1', ] + \
            self.convert_push_segment('LCL') + \
            self.convert_push_segment('ARG') + \
            self.convert_push_segment('THIS') + \
            self.convert_push_segment('THAT') + [ \
            '// ARG = SP-5-nArgs', # Repositions ARG
            '@SP', # SP - 5 - nArgs
            'D=M',
            '@5',
            'D=D-A',
            "@{}".format(num_args), # nArgs
            'D=D-A',
            '@ARG',
            'M=D',

            '// LCL = SP', # Repositions LCL
            '@SP',
            'D=M',
            '@LCL',
            'M=D'] + \
            self.convert_goto_command(function_name) + [ \
            '// (retAddrLabel)', # The same translator-gen label
            "({})".format(return_address_label),
            ]

    def convert_return_command(self):
        expected = [
            '// return',

            '// endFrame = LCL', # endFrame is a temp var
            '@LCL',
            'D=M',
            '@R13',  # Store endFrame here
            'M=D',
            ] + \
            self.addr_equals_star_addr_minus_offset('R14', 'retAddr', 'endFrame', 5) + \
            ['// *ARG = pop()'] + \
            self.decrement_sp() + \
            self.star_addr_equals_star_sp('ARG') + [ \

            '// SP = ARG + 1', # reposition SP of caller
            '@ARG',
            'D=M+1',
            '@SP',
            'M=D',

            ] + \
            self.addr_equals_star_addr_minus_offset('THAT', 'THAT', 'endFrame', 1) + \
            self.addr_equals_star_addr_minus_offset('THIS', 'THIS', 'endFrame', 2) + \
            self.addr_equals_star_addr_minus_offset('ARG', 'ARG', 'endFrame', 3) + \
            self.addr_equals_star_addr_minus_offset('LCL', 'LCL', 'endFrame', 4) + [ \

            '// goto retAddr',
            '@R14', # retAddr stored here
            'A=M',
            '0;JMP',
        ]
        return expected

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

    def star_addr_equals_star_sp(self, addr):
        return [
            '@SP', # D = *SP
            'A=M',
            'D=M',

            "@{}".format(addr),
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

    def star_sp_equals_segment(self, segment, index=0):
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

    def addr_equals_star_addr_minus_offset(self, target_addr, target_addr_symbol, source_addr, offset):
        return [
            # For example:
            #'// retAddr = *(endFrame - 5)', # gets ret address
            #'// THAT = *(endFrame - 1)', # restores THAT of caller
            "// {} = *({} - {})".format(target_addr_symbol, source_addr, offset),
            "@{}".format(offset), # offset
            'D=A',
            '@R13',
            'D=M-D',  # source_addr - 5
            'A=D',
            'D=M',
            "@{}".format(target_addr), # target_addr
            'M=D',
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
        if len(segment.split('.')) > 1:
            return segment
        if (segment == 'pointer'):
            return ['THIS', 'THAT'][index]

        if (segment == 'static'):
            return self.get_static_segment_type(segment, index)

        segment_types = {
            'local': 'LCL',
            'LCL': 'LCL',
            'argument': 'ARG',
            'ARG': 'ARG',
            'temp': '5',
            'this': 'THIS',
            'THIS': 'THIS',
            'that': 'THAT',
            'THAT': 'THAT',
        }
        return segment_types[segment]

    def get_static_segment_type(self, segment, index):
        # Figure out name of the fuxkin thing
        vm_filename = self.output_filepath.split("/")[-1].split(".")[0]
        return "{}.{}".format(vm_filename, index)

    def close(self):
        self.output_file.close()


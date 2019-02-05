class CodeWriter:
    def __init__(self, output_filepath):
        self.output_filepath = output_filepath
        self.output_file = open(output_filepath, 'w')

    # Writes to the output_file the assembly code that implements the given
    # arithmetic command
    def write_arithmetic(self, command):
        pass

    # Writes to the output_file the assembly code that implements the given
    # command, where command is either C_PUSH or C_POP
    def write_push_pop(self, command, segment, index):
        pass

    def convert_push_command(self, command, segment, index):
        expected = [
            "// {} {} {}".format(command, segment, index),
            '@' + str(index),
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1'
        ]
        return expected

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



#        expected = [
#            "// {} {} {}".format(command, segment, index),
#
#            '@' + self.get_segment_type(segment), # D = segment + i
#            'D=M',
#            '@' + str(index),
#            'D=D+A',
#            '@R13', # addr = D, store for later
#            'M=D',
#
#            '@SP', # SP--
#            'M=M-1',
#
#            '@SP', # D = *SP
#            'A=M',
#            'D=M',
#
#            '@R13', # *addr = D
#            'M=A',
#            'M=D'
#        ]
#        return expected

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
            'D=M',
            '@' + str(index),
            'D=D+A',
            '@R13', # addr = D, store for later
            'M=D',
        ]

    def decrement_sp(self):
        return [
            '@SP', # SP--
            'M=M-1',
        ]

    def star_addr_equals_star_sp(self):
        return [
            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@R13', # *addr = D
            'M=A',
            'M=D',
        ]

    def close(self):
        self.output_file.close()

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



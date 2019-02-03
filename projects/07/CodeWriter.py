class CodeWriter:
    def __init__(self, output_filepath):
        self.output_file = open(output_filepath, 'w')

    # Writes to the output_file the assembly code that implements the given
    # arithmetic command
    def write_arithmetic(self, command):
        pass

    # Writes to the output_file the assembly code that implements the given
    # command, where command is either C_PUSH or C_POP
    def write_push_pop(self, command, segment, index):
        pass

    def close(self):
        pass

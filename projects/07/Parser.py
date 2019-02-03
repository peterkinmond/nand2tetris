class Parser:
    def __init__(self, filepath):
        self.input_file = open(filepath, 'r')
        line = self.input_file.readline()
        print(line)

    def has_more_commands(self):
        pass

    def advance(self):
        pass

    def command_type(self):
        command_types = {
            'add': C_ARITHMETIC,
            # TODO: add all arithmetic/logic commands
            'push': C_PUSH,
            'pop': C_POP,
            'label': C_LABEL,
            'goto': C_GOTO,
            'if-goto': C_IF,
            'function': C_FUNCTION,
            'call': C_CALL,
            'return': C_RETURN
        }

    def arg1(self):
        pass

    def arg2(self):
        pass



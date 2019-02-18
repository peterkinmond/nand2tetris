import Constants

class Parser:
    def __init__(self, filepath):
        self.commands = []
        self.current_command = ''
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line == '' or line.startswith('//'):
                    continue
                self.commands.append(line)

    def has_more_commands(self):
        return len(self.commands) > 0

    def advance(self):
        self.current_command = self.commands.pop(0)
        self.parse_command()

    def parse_command(self):
        command_parts = self.current_command.split(' ')
        self.command_type = self.get_command_type(command_parts[0])
        self.arg1 = None
        self.arg2 = None

        if self.command_type == Constants.C_ARITHMETIC:
            self.arg1 = command_parts[0]
        elif self.command_type in [Constants.C_PUSH, Constants.C_POP]:
            self.arg1 = command_parts[1]
            self.arg2 = int(command_parts[2])
        elif self.command_type in [Constants.C_LABEL, Constants.C_GOTO, Constants.C_IF]:
            self.arg1 = command_parts[1]

        print('Current command: ' + self.current_command)
        print('Command type: ' + self.command_type)
        print('Arg 1: ' + str(self.arg1))
        print('Arg 2: ' + str(self.arg2))

    def get_command_type(self, command):
        command_types = {
            'add': Constants.C_ARITHMETIC,
            'sub': Constants.C_ARITHMETIC,
            'neg': Constants.C_ARITHMETIC,
            'eq': Constants.C_ARITHMETIC,
            'gt': Constants.C_ARITHMETIC,
            'lt': Constants.C_ARITHMETIC,
            'and': Constants.C_ARITHMETIC,
            'or': Constants.C_ARITHMETIC,
            'not': Constants.C_ARITHMETIC,
            'push': Constants.C_PUSH,
            'pop': Constants.C_POP,
            'label': Constants.C_LABEL,
            'goto': Constants.C_GOTO,
            'if-goto': Constants.C_IF,
            # TODO: branching/function commands
#            'function': Constants.C_FUNCTION,
#            'call': Constants.C_CALL,
#            'return': Constants.C_RETURN
        }
        return command_types[command]

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
        if len(command_parts) > 1:
            self.arg1 = command_parts[1]
            self.arg2 = command_parts[2]

        print('Command type: ' + self.command_type)
        print('Arg 1: ' + str(self.arg1))
        print('Arg 2: ' + str(self.arg2))
        print('Current command: ' + self.current_command)

    def get_command_type(self, command):
        command_types = {
            'add': Constants.C_ARITHMETIC,
            # TODO: add all arithmetic/logic commands
            'push': Constants.C_PUSH,
            'pop': Constants.C_POP,
#            'label': C_LABEL,
#            'goto': C_GOTO,
#            'if-goto': C_IF,
#            'function': C_FUNCTION,
#            'call': C_CALL,
#            'return': C_RETURN
        }
        return command_types[command]

#    def arg1(self):
#        pass
#
#    def arg2(self):
#        pass
#


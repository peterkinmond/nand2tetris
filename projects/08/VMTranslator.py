import os
import sys
import CodeWriter
import Constants
import Parser

def main():
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    asm_filepath = os.path.splitext(filepath)[0] + ".asm"

    print('Loading file: ' + filepath)
    parser = Parser.Parser(filepath)
    code_writer = CodeWriter.CodeWriter(asm_filepath)

    print('Running through all commands in VM code')
    while parser.has_more_commands():
        parser.advance()

        if parser.command_type == Constants.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1)
        elif parser.command_type in [Constants.C_PUSH, Constants.C_POP]:
            code_writer.write_push_pop(parser.command_type, parser.arg1, parser.arg2)
        elif parser.command_type == Constants.C_LABEL:
            code_writer.write_label(parser.arg1)
        elif parser.command_type == Constants.C_GOTO:
            code_writer.write_goto(parser.arg1)
        elif parser.command_type == Constants.C_IF:
            code_writer.write_if(parser.arg1)
        elif parser.command_type == Constants.C_FUNCTION:
            code_writer.write_function(parser.arg1, parser.arg2)
        elif parser.command_type == Constants.C_CALL:
            code_writer.write_call(parser.arg1, parser.arg2)
        elif parser.command_type == Constants.C_RETURN:
            code_writer.write_return()
        else:
            raise Exception("Command '{}' not handled".format(parser.command_type))

    print('Closing file: ' + filepath)
    code_writer.close()

if __name__ == '__main__':
    main()


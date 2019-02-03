import os
import sys
import CodeWriter
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

        if parser.command_type() in [C_PUSH, C_POP]:
            code_writer.write_push_pop()
        else:
            code_writer.write_arithmetic()

    print('Closing file: ' + filepath)
    code_writer.close()

if __name__ == '__main__':
    main()


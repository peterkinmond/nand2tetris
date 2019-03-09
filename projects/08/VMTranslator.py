import glob
import os
import sys
import CodeWriter
import Constants
import Parser

def main():
    path = sys.argv[1]
    vm_files = []
    asm_filepath = ''
    is_directory = False

    if os.path.isfile(path):
        vm_files = [path]
        asm_filepath = os.path.splitext(path)[0] + ".asm"
    elif os.path.isdir(path):
        is_directory = True
        if path.endswith('/'):
            path = path[:-1]
        os.chdir(path)
        for file in glob.glob("*.vm"):
            vm_files.append(file)
        asm_filepath = os.path.split(path)[1] + ".asm"
    else:
        print("Path {} does not exist. Exiting...".format(path))
        sys.exit()

    code_writer = CodeWriter.CodeWriter(asm_filepath)

    # Only run bootstrap code when multiple files (in a dir)
    # are being translated since it kicks off Sys.init function
    # which isn't present in the single file VM tests.
    if is_directory:
        code_writer.write_init()

    for vm_file in vm_files:
        print('Loading file: ' + vm_file)
        code_writer.set_file_name(vm_file)
        parser = Parser.Parser(vm_file)
        parse_file(code_writer, parser)

    code_writer.close()
    print('Closing file: ' + vm_file)

def parse_file(code_writer, parser):
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

if __name__ == '__main__':
    main()


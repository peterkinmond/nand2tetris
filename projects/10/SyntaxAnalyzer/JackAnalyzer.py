import glob
import os
import sys
from CompilationEngine import CompilationEngine

def main():
    path = sys.argv[1]
    jack_files = []

    if os.path.isfile(path):
        jack_files = [path]
    elif os.path.isdir(path):
        if path.endswith('/'):
            path = path[:-1]
        os.chdir(path)
        for file in glob.glob("*.jack"):
            jack_files.append(file)
    else:
        print("Path {} does not exist. Exiting...".format(path))
        sys.exit()

    for jack_file in jack_files:
        print('Loading file: ' + jack_file)
        output_file = os.path.splitext(jack_file)[0] + ".xml"
        compilation_engine = CompilationEngine(jack_file, output_file)
        compilation_engine.compile_class()
        compilation_engine.save_output_file()
        print('Finished processing file: ' + jack_file)

if __name__ == '__main__':
    main()

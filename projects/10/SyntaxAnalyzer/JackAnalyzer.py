import glob
import os
import sys

def main():
    path = sys.argv[1]
    jack_files = []
    output_filepath = ''
    is_directory = False

    if os.path.isfile(path):
        jack_files = [path]
        output_filepath = os.path.splitext(path)[0] + ".xml"
    elif os.path.isdir(path):
        is_directory = True
        if path.endswith('/'):
            path = path[:-1]
        os.chdir(path)
        for file in glob.glob("*.jack"):
            jack_files.append(file)
        output_filepath = os.path.split(path)[1] + ".xml"
    else:
        print("Path {} does not exist. Exiting...".format(path))
        sys.exit()

    for jack_file in jack_files:
        print('Loading file: ' + jack_file)
        # TODO: analyze each file

    print('Closing file: ' + jack_file)

if __name__ == '__main__':
    main()

class VMWriter(object):
    def __init__(self, output_file):
        """Creates a new output .vm file and prepares it for
        writing.
        """
        pass

    def write_push(self, segment, index):
        """Writes a VM push command."""
        pass

    def write_pop(self, segment, index):
        """Writes a VM pop command."""
        pass

    def write_arithmetic(self, command):
        """Writes a VM arithmetic-logical command."""
        pass

    def write_label(self, label):
        """Writes a VM label command."""
        pass

    def write_goto(self, label):
        """Writes a VM goto command."""
        pass

    def write_if(self, label):
        """Writes a VM if-goto command."""
        pass

    def write_call(self, name, num_args):
        """Writes a VM call commmand."""
        pass

    def write_function(self, name, num_locals):
        """Writes a VM function command."""
        pass

    def write_return(self):
        """Writes a VM return command."""
        pass

    def close(self):
        """Closes the output file"""
        pass



class VMWriter(object):
    # TODO: Handle VM file writing here? Or just figuring
    # out what the VM commands output would be?
    #def __init__(self, output_file):
    def __init__(self):
        """Creates a new output .vm file and prepares it for
        writing.
        """
        pass

    def write_push(self, segment, index):
        """Writes a VM push command."""
        return "push {} {}".format(segment, index)

    def write_pop(self, segment, index):
        """Writes a VM pop command."""
        return "pop {} {}".format(segment, index)

    def write_arithmetic(self, command):
        """Writes a VM arithmetic-logical command."""
        return command

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
        return "call {} {}".format(name, num_args)

    def write_function(self, name, num_locals):
        """Writes a VM function command."""
        return "function {} {}".format(name, num_locals)

    def write_return(self):
        """Writes a VM return command."""
        return "return"

    def close(self):
        """Closes the output file"""
        pass



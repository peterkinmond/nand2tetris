from Constants import *

class VMWriter(object):
    # TODO: Handle VM file writing here? Or just figuring
    # out what the VM commands output would be?
    #def __init__(self, output_file):
    def __init__(self):
        """Creates a new output .vm file and prepares it for
        writing.
        """
        self.output = []

    def write_push(self, segment, index):
        """Writes a VM push command."""
        segment = self._convert_segment_to_vm_segment(segment)
        self.output.append(f"push {segment} {index}")

    def write_pop(self, segment, index):
        """Writes a VM pop command."""
        segment = self._convert_segment_to_vm_segment(segment)
        self.output.append(f"pop {segment} {index}")

    def write_arithmetic(self, command, unary=False):
        """Writes a VM arithmetic-logical command."""
        self.output.append(self._convert_op_to_vm_command(command, unary))

    def write_label(self, label):
        """Writes a VM label command."""
        self.output.append(f"label {label}")

    def write_goto(self, label):
        """Writes a VM goto command."""
        self.output.append(f"goto {label}")

    def write_if(self, label):
        """Writes a VM if-goto command."""
        self.output.append(f"if-goto {label}")

    def write_call(self, name, num_args):
        """Writes a VM call commmand."""
        self.output.append(f"call {name} {num_args}")

    def write_function(self, name, num_locals):
        """Writes a VM function command."""
        self.output.append(f"function {name} {num_locals}")

    def write_return(self):
        """Writes a VM return command."""
        self.output.append("return")

    def close(self):
        """Closes the output file"""
        pass

    def _convert_op_to_vm_command(self, op, unary):
        if op == "+":
            return "add"
        elif op == "*":
            return "call Math.multiply 2"
        elif op == "/":
            return "call Math.divide 2"
        # TODO: Distinguish between neg and sub for "-" symbol
        elif op == "-" and unary == True:
            return "neg"
        elif op == "-" and unary == False:
            return "sub"
        elif op == "~":
            return "not"
        elif op == "=":
            return "eq"
        elif op == "&gt;":
            return "gt"
        elif op == "&lt;":
            return "lt"
        elif op == "&amp;":
            return "and"
        elif op == "|":
            return "or"
        else:
            return op

    def _convert_segment_to_vm_segment(self, segment):
        if segment == FIELD:
            return THIS
        else:
            return segment

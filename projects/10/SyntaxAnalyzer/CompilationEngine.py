class CompilationEngine(object):
    """CompilationEngine: generates the compiler's output."""

    def __init__(self):
        """Creates a new compilation engine with the
        given input and output.

        The next routine called must be compile_class
        """
        pass

    def compile_class(self):
        """Compiles a complete class."""
        pass

    def compile_class_var_dec(self):
        """Compiles a static variable declaration,
        or a field declaration."""
        pass


    def compile_subroutine_dec(self):
        """Compiles a complete method, function, or constructor."""
        pass

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list.
        Does not handle the enclosing "()".
        """
        pass

    def compile_subroutine_body(self):
        """Compiles a subroutine's body."""
        pass

    def compile_var_dec(self):
        """Compiles a var declaration."""
        pass

    def compile_statements(self):
        """Compiles a sequence of statements.
        Does not handle the enclosing "{}".
        """
        pass

    def compile_let(self):
        """Compiles a let statement."""
        pass

    def compile_if(self):
        """Compiles a if statement."""
        pass

    def compile_while(self):
        """Compiles a while statement."""
        pass

    def compile_do(self):
        """Compiles a do statement."""
        pass

    def compile_return(self):
        """Compiles a return statement."""
        pass

    def compile_expression(self):
        """Compiles an expression."""
        pass

    def compile_term(self):
        """Compiles a term. If the current token is an identifier,
        the routine must distinguish between a variable, an array entry,
        or a subroutine call. A single look-ahead token, which may
        be one of "[", "(", or ".", suffices to distinguish between
        the possibilities. Any other token is not part of this term
        and should not be advanced over.
        """
        pass

    def compile_expression_list(self):
        """Compiles a (possibly empyt) comma-separated list of expressions."""
        pass

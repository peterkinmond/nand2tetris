class SymbolTable(object):
    def __init__(self):
        """Creates a new symbol table"""
        pass

    def start_subroutine(self):
        """Starts a new subroutine scope (i.e. resets the
        subroutine's symbol table).
        """
        pass

    def define(self, name, type, kind):
        """Defines a new identifier of the given name, type
        and kind, and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while
        ARG and VAR identifiers have a subroutine scope.
        """
        pass

    def var_count(self, kind):
        """Returns the number of vars of the given kind
        already defined in the current scope.
        """
        pass

    def kind_of(self, name):
        """Returns the kind of the named identifier in the
        current scope. If the identifier is unknown in the
        current scope, returns NONE.
        """
        pass

    def type_of(self, name):
        """Returns the type of the named identifier in the
        current scope.
        """
        pass

    def index_of(self, name):
        """Returns the index assigned to the named identifier."""
        pass

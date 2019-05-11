from Constants import *

class SymbolTable(object):
    """
    # self.symbol_table = {
    #     'x': { 'type': int, 'kind': field, 'index': 0 },
    #     'y': { 'type': int, 'kind': field, 'index': 1 },
    #     'pointCount': { 'type': int, 'kind': static, 'index': 0 },
    #     'this': { 'type': Point, 'kind': argument, 'index': 0 }
    #     'other': { 'type': Point, 'kind': argument, 'index': 1 }
    # }
    """

    def __init__(self):
        """Creates a new symbol table"""
        self.symbol_table = {}

    def start_subroutine(self):
        """Starts a new subroutine scope (i.e. resets the
        subroutine's symbol table).
        """
        class_symbol_table = {}
        for (key, value) in self.symbol_table.items():
            if value['kind'] in [FIELD, STATIC]:
                class_symbol_table[key] = value
        self.symbol_table = class_symbol_table

    def define(self, name, type, kind):
        """Defines a new identifier of the given name, type
        and kind, and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while
        ARG and VAR identifiers have a subroutine scope.
        """
        if type == None:
            raise Exception("Type for symbol '{}' cannot be None".format(name))

        self.symbol_table[name] = {
            'type': type,
            'kind': kind,
            'index': self.var_count(kind)
        }

    def var_count(self, kind):
        """Returns the number of vars of the given kind
        already defined in the current scope.
        """
        matching_symbols = dict((k, v) for k, v in self.symbol_table.items() if v['kind'] == kind)
        return len(matching_symbols)

    def kind_of(self, name):
        """Returns the kind of the named identifier in the
        current scope. If the identifier is unknown in the
        current scope, returns NONE.
        """
        if name not in self.symbol_table:
            return None
        else:
            return self.symbol_table[name]['kind']

    def type_of(self, name):
        """Returns the type of the named identifier in the
        current scope.
        """
        return self.symbol_table[name]['type']

    def index_of(self, name):
        """Returns the index assigned to the named identifier."""
        if name not in self.symbol_table:
            return None
        else:
            return self.symbol_table[name]['index']

    def is_in_symbol_table(self, name):
        return name in self.symbol_table

    def is_type(self, type):
        for (key, value) in self.symbol_table.items():
            if value['type'] == type:
                return True

        return False

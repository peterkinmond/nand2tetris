from Constants import *
from SymbolTable import *
import unittest


class SymbolTableTest(unittest.TestCase):
    def test_adding_symbols(self):
        st = SymbolTable()
        st.define('x', INT, FIELD)
        self.assertEqual(st.type_of('x'), INT)
        self.assertEqual(st.kind_of('x'), FIELD)
        self.assertEqual(st.index_of('x'), 0)
        self.assertEqual(st.var_count(FIELD), 1)

        st.define('y', INT, FIELD)
        self.assertEqual(st.type_of('y'), INT)
        self.assertEqual(st.kind_of('y'), FIELD)
        self.assertEqual(st.index_of('y'), 1)
        self.assertEqual(st.var_count(FIELD), 2)

    def test_starting_new_subroutine(self):
        st = SymbolTable()
        st.define('x', INT, LOCAL)
        self.assertEqual(st.var_count(LOCAL), 1)
        st.define('count', INT, STATIC)
        self.assertEqual(st.var_count(STATIC), 1)

        # Subroutine reset - delete arg/local
        st.start_subroutine()
        self.assertEqual(st.var_count(LOCAL), 0)
        self.assertEqual(st.kind_of('x'), None)
        self.assertEqual(st.var_count(STATIC), 1)
        self.assertEqual(st.kind_of('count'), STATIC)


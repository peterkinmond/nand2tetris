import unittest
from CompilationEngine import CompilationEngine

class CompilationEngineTest(unittest.TestCase):
    def test_compile_class(self):
        engine = CompilationEngine("BasicTestClass.jack", "BasicTestClass.xml")
        engine.compile_class()
        self.assertEqual(engine.output, [
            '<class>',
                '<keyword> class </keyword>',
                '<identifier> BasicTestClass </identifier>',
                '<symbol> { </symbol>',
                '<symbol> } </symbol>',
            '</class>'])

    def test_compile_let(self):
        engine = CompilationEngine("let x = 4;", "BasicTestClass.xml", True)
        engine.compile_let()
        self.assertEqual(engine.output, [
            '<letStatement>',
                '<keyword> let </keyword>',
                '<identifier> x </identifier>',
                '<symbol> = </symbol>',
                '<expression>',
                    '<term>',
                        '<integerConstant> 4 </integerConstant>',
                    '</term>',
                '</expression>',
                '<symbol> ; </symbol>',
            '</letStatement>'])

    def test_compile_return(self):
        engine = CompilationEngine("return;", "fakeOutputFile", True)
        engine.compile_return()
        self.assertEqual(engine.output, [
            '<returnStatement>',
                '<keyword> return </keyword>',
                '<symbol> ; </symbol>',
            '</returnStatement>'])

#    def test_compile_return_2(self):
#        engine = CompilationEngine("return this;", "fakeOutputFile", True)
#        engine.compile_return()
#        self.assertEqual(engine.output, [
#            '<returnStatement>',
#                '<keyword> return </keyword>',
#                '<expression>',
#                    '<term>',
#                        '<keyword> this </keyword>',
#                    '</term>',
#                '</expression>',
#                '<symbol> ; </symbol>',
#            '</returnStatement>'])

#    def test_compile_var_dec(self):
#        engine = CompilationEngine("var int countA, countB;")
#        self.assertEqual(engine.output, [
#            '<varDec>',
#                '<keyword> var </keyword>',
#                '<identifier> BasicTestClass </identifier>',
#                '<symbol> ; </symbol>',
#            '</varDec>'])



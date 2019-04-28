import unittest
from CompilationEngine import CompilationEngine

class CompilationEngineTest(unittest.TestCase):
    def test_compile_class(self):
        engine = CompilationEngine("BasicTestClass.jack", "fakeOutputFile")
        engine.compile_class()
        self.assertEqual(engine.output, [
            '<class>',
                '<keyword> class </keyword>',
                '<identifier> BasicTestClass </identifier>',
                '<symbol> { </symbol>',
                '<symbol> } </symbol>',
            '</class>'])

    def test_compile_class_var_dec(self):
        engine = CompilationEngine("field int direction;", "fakeOutputFile", True)
        engine.compile_class_var_dec()
        self.assertEqual(engine.output, [
            '<classVarDec>',
                '<keyword> field </keyword>',
                '<keyword> int </keyword>',
                '<identifier> direction </identifier>',
                '<symbol> ; </symbol>',
            '</classVarDec>'])

    def test_compile_class_var_dec_2(self):
        engine = CompilationEngine("field int directionA, directionB;", "fakeOutputFile", True)
        engine.compile_class_var_dec()
        self.assertEqual(engine.output, [
            '<classVarDec>',
                '<keyword> field </keyword>',
                '<keyword> int </keyword>',
                '<identifier> directionA </identifier>',
                '<symbol> , </symbol>',
                '<identifier> directionB </identifier>',
                '<symbol> ; </symbol>',
            '</classVarDec>'])

    def test_compile_var_dec(self):
        engine = CompilationEngine("var char key;", "fakeOutputFile", True)
        engine.compile_var_dec()
        self.assertEqual(engine.output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> char </keyword>',
                '<identifier> key </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>'])

    def test_compile_var_dec_2(self):
        engine = CompilationEngine("var char keyA, keyB;", "fakeOutputFile", True)
        engine.compile_var_dec()
        self.assertEqual(engine.output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> char </keyword>',
                '<identifier> keyA </identifier>',
                '<symbol> , </symbol>',
                '<identifier> keyB </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>'])

    def test_compile_let(self):
        engine = CompilationEngine("let x = 4;", "fakeOutputFile", True)
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

    def test_compile_while(self):
        engine = CompilationEngine("while (key = 0) {}", "fakeOutputFile", True)
        engine.compile_while()
        self.assertEqual(engine.output, [
            '<whileStatement>',
                '<keyword> while </keyword>',
                '<symbol> ( </symbol>',
                '<expression>',
                    '<term>',
                        '<identifier> key </identifier>',
                    '</term>',
                    '<symbol> = </symbol>',
                    '<term>',
                        '<integerConstant> 0 </integerConstant>',
                    '</term>',
                '</expression>',
                '<symbol> ) </symbol>',
                '<symbol> { </symbol>',
                '<symbol> } </symbol>',
            '</whileStatement>'])

#    def test_compile_do(self):
#        engine = CompilationEngine("do draw();", "fakeOutputFile", True)
#        engine.compile_do()
#        self.assertEqual(engine.output, [
#            '<doStatement>',
#                '<keyword> do </keyword>',
#                '<identifier> draw </identifier>',
#                '<symbol> ( </symbol>',
#                '<expressionList>',
#                '</expressionList>',
#                '<symbol> ) </symbol>',
#                '<symbol> ; </symbol>',
#            '</doStatement>'])

    def test_compile_return(self):
        engine = CompilationEngine("return;", "fakeOutputFile", True)
        engine.compile_return()
        self.assertEqual(engine.output, [
            '<returnStatement>',
                '<keyword> return </keyword>',
                '<symbol> ; </symbol>',
            '</returnStatement>'])

    def test_compile_return_2(self):
        engine = CompilationEngine("return this;", "fakeOutputFile", True)
        engine.compile_return()
        self.assertEqual(engine.output, [
            '<returnStatement>',
                '<keyword> return </keyword>',
                '<expression>',
                    '<term>',
                        '<keyword> this </keyword>',
                    '</term>',
                '</expression>',
                '<symbol> ; </symbol>',
            '</returnStatement>'])


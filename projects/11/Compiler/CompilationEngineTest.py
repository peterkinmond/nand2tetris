import re
import unittest
from CompilationEngine import CompilationEngine

class CompilationEngineTest(unittest.TestCase):
    def test_compile_class(self):
        engine = CompilationEngine("BasicTestClass.jack", "fakeOutputFile")
        engine.compile_class()
        self.assertEqual(engine.xml_output, [
            '<class>',
                '<keyword> class </keyword>',
                '<identifier> BasicTestClass, category: class, definedOrUsed: defined </identifier>',
                '<symbol> { </symbol>',
                '<symbol> } </symbol>',
            '</class>'])

    def test_compile_class_var_dec(self):
        engine = CompilationEngine("field int direction;", "fakeOutputFile", True)
        engine.compile_class_var_dec()
        self.assertEqual(engine.xml_output, [
            '<classVarDec>',
                '<keyword> field </keyword>',
                '<keyword> int </keyword>',
                '<identifier> direction, category: field, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> ; </symbol>',
            '</classVarDec>'])

    def test_compile_class_var_dec_2(self):
        engine = CompilationEngine("static int directionA, directionB;", "fakeOutputFile", True)
        engine.compile_class_var_dec()
        self.assertEqual(engine.xml_output, [
            '<classVarDec>',
                '<keyword> static </keyword>',
                '<keyword> int </keyword>',
                '<identifier> directionA, category: static, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> , </symbol>',
                '<identifier> directionB, category: static, definedOrUsed: defined, index: 1 </identifier>',
                '<symbol> ; </symbol>',
            '</classVarDec>'])


    def test_compile_subroutine_dec(self):
        engine = CompilationEngine("method void decSize(int Ax, int Ay) { var boolean exit; }", "fakeOutputFile", True)
        engine.compile_subroutine_dec()
        self.assertEqual(engine.xml_output, [
            '<subroutineDec>',
                '<keyword> method </keyword>',
                '<keyword> void </keyword>',
                '<identifier> decSize, category: subroutine, definedOrUsed: defined </identifier>',
                '<symbol> ( </symbol>',
                '<parameterList>',
                    '<keyword> int </keyword>',
                    '<identifier> Ax, category: argument, definedOrUsed: defined, index: 0 </identifier>',
                    '<symbol> , </symbol>',
                    '<keyword> int </keyword>',
                    '<identifier> Ay, category: argument, definedOrUsed: defined, index: 1 </identifier>',
                '</parameterList>',
                '<symbol> ) </symbol>',
                '<subroutineBody>',
                    '<symbol> { </symbol>',
                    '<varDec>',
                        '<keyword> var </keyword>',
                        '<keyword> boolean </keyword>',
                        '<identifier> exit, category: local, definedOrUsed: defined, index: 0 </identifier>',
                        '<symbol> ; </symbol>',
                    '</varDec>',
                    '<statements>',
                    '</statements>',
                    '<symbol> } </symbol>',
                '</subroutineBody>',
            '</subroutineDec>'])

    def test_compile_var_dec(self):
        engine = CompilationEngine("var char key;", "fakeOutputFile", True)
        engine.compile_var_dec()
        self.assertEqual(engine.xml_output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> char </keyword>',
                '<identifier> key, category: local, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>'])

    def test_compile_var_dec_2(self):
        engine = CompilationEngine("var char keyA, keyB;", "fakeOutputFile", True)
        engine.compile_var_dec()
        self.assertEqual(engine.xml_output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> char </keyword>',
                '<identifier> keyA, category: local, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> , </symbol>',
                '<identifier> keyB, category: local, definedOrUsed: defined, index: 1 </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>'])

    def test_compile_let(self):
        engine = CompilationEngine('var char x; let x = "string constant";', "fakeOutputFile", True)
        engine.compile_var_dec()
        engine.compile_let()
        self.assertEqual(engine.xml_output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> char </keyword>',
                '<identifier> x, category: local, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>',
            '<letStatement>',
                '<keyword> let </keyword>',
                '<identifier> x, category: local, definedOrUsed: used, index: 0 </identifier>',
                '<symbol> = </symbol>',
                '<expression>',
                    '<term>',
                        '<stringConstant> string constant </stringConstant>',
                    '</term>',
                '</expression>',
                '<symbol> ; </symbol>',
            '</letStatement>'])

    def test_compile_if(self):
        engine = CompilationEngine("var int key; if (key = 81) { return; } else {}", "fakeOutputFile", True)
        engine.compile_var_dec()
        engine.compile_if()
        self.assertEqual(engine.xml_output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> int </keyword>',
                '<identifier> key, category: local, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>',
            '<ifStatement>',
                '<keyword> if </keyword>',
                '<symbol> ( </symbol>',
                '<expression>',
                    '<term>',
                        '<identifier> key, category: local, definedOrUsed: used, index: 0 </identifier>',
                    '</term>',
                    '<symbol> = </symbol>',
                    '<term>',
                        '<integerConstant> 81 </integerConstant>',
                    '</term>',
                '</expression>',
                '<symbol> ) </symbol>',
                '<symbol> { </symbol>',
                '<statements>',
                    '<returnStatement>',
                        '<keyword> return </keyword>',
                        '<symbol> ; </symbol>',
                    '</returnStatement>',
                '</statements>',
                '<symbol> } </symbol>',
                '<keyword> else </keyword>',
                '<symbol> { </symbol>',
                '<statements>',
                '</statements>',
                '<symbol> } </symbol>',
            '</ifStatement>'])

    def test_compile_while(self):
        engine = CompilationEngine("var int key; while (key = 0) {}", "fakeOutputFile", True)
        engine.compile_var_dec()
        engine.compile_while()
        self.assertEqual(engine.xml_output, [
            '<varDec>',
                '<keyword> var </keyword>',
                '<keyword> int </keyword>',
                '<identifier> key, category: local, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> ; </symbol>',
            '</varDec>',
            '<whileStatement>',
                '<keyword> while </keyword>',
                '<symbol> ( </symbol>',
                '<expression>',
                    '<term>',
                        '<identifier> key, category: local, definedOrUsed: used, index: 0 </identifier>',
                    '</term>',
                    '<symbol> = </symbol>',
                    '<term>',
                        '<integerConstant> 0 </integerConstant>',
                    '</term>',
                '</expression>',
                '<symbol> ) </symbol>',
                '<symbol> { </symbol>',
                '<statements>',
                '</statements>',
                '<symbol> } </symbol>',
            '</whileStatement>'])

    def test_compile_do(self):
        engine = CompilationEngine("do draw();", "fakeOutputFile", True)
        engine.compile_do()
        self.assertEqual(engine.xml_output, [
            '<doStatement>',
                '<keyword> do </keyword>',
                '<identifier> draw, category: subroutine, definedOrUsed: used </identifier>',
                '<symbol> ( </symbol>',
                '<expressionList>',
                '</expressionList>',
                '<symbol> ) </symbol>',
                '<symbol> ; </symbol>',
            '</doStatement>'])

    def test_compile_do_2(self):
        engine = CompilationEngine("field Square square; do square.dispose();", "fakeOutputFile", True)
        engine.compile_class_var_dec()
        engine.compile_do()
        self.assertEqual(engine.xml_output, [
            '<classVarDec>',
                '<keyword> field </keyword>',
                '<identifier> Square, category: class, definedOrUsed: used </identifier>',
                '<identifier> square, category: field, definedOrUsed: defined, index: 0 </identifier>',
                '<symbol> ; </symbol>',
            '</classVarDec>',
            '<doStatement>',
                '<keyword> do </keyword>',
                '<identifier> square, category: field, definedOrUsed: used, index: 0 </identifier>',
                '<symbol> . </symbol>',
                '<identifier> dispose, category: subroutine, definedOrUsed: used </identifier>',
                '<symbol> ( </symbol>',
                '<expressionList>',
                '</expressionList>',
                '<symbol> ) </symbol>',
                '<symbol> ; </symbol>',
            '</doStatement>'])

    def test_compile_return(self):
        engine = CompilationEngine("return;", "fakeOutputFile", True)
        engine.compile_return()
        self.assertEqual(engine.xml_output, [
            '<returnStatement>',
                '<keyword> return </keyword>',
                '<symbol> ; </symbol>',
            '</returnStatement>'])

    def test_compile_return_2(self):
        engine = CompilationEngine("return this;", "fakeOutputFile", True)
        engine.compile_return()
        self.assertEqual(engine.xml_output, [
            '<returnStatement>',
                '<keyword> return </keyword>',
                '<expression>',
                    '<term>',
                        '<keyword> this </keyword>',
                    '</term>',
                '</expression>',
                '<symbol> ; </symbol>',
            '</returnStatement>'])

    def test_code_write(self):
        engine = CompilationEngine(";", "fakeOutputFile", True)
        engine.code_write([[2]])
        self.assertEqual(engine.vm_output, [
            'push constant 2'])

    def test_code_write_2(self):
        engine = CompilationEngine(";", "fakeOutputFile", True)
        engine.code_write([[2], '+', [3]])
        self.assertEqual(engine.vm_output, [
            'push constant 2',
            'push constant 3',
            'add'])

    def test_code_write_3(self):
        engine = CompilationEngine(";", "fakeOutputFile", True)
        engine.code_write([[8], '*', [9]])
        self.assertEqual(engine.vm_output, [
            'push constant 8',
            'push constant 9',
            'call Math.multiply 2'])

    def test_code_write_4(self):
        engine = CompilationEngine(";", "fakeOutputFile", True)
        engine.code_write([['-'], [1]])
        self.assertEqual(engine.vm_output, [
            'push constant 1',
            'neg'])

    def test_square_main_file(self):
        engine = CompilationEngine("../Square/Main.jack", "fakeOutputFile")
        engine.compile_class()
        xml_file = self.convert_xml_file("../Square/Main.xml")
        self.assertEqual(len(engine.xml_output), 244)
        self.assertEqual(engine.xml_output, xml_file)

# TODO: Do we want to add extra identifier info to these (large) classes?
#    def test_square_file(self):
#        engine = CompilationEngine("../Square/Square.jack", "fakeOutputFile")
#        engine.compile_class()
#        xml_file = self.convert_xml_file("../Square/Square.xml")
#        self.assertEqual(len(engine.xml_output), 1211)
#        self.assertEqual(engine.xml_output, xml_file)
#
#    def test_square_game_file(self):
#        engine = CompilationEngine("../Square/SquareGame.jack", "fakeOutputFile")
#        engine.compile_class()
#        xml_file = self.convert_xml_file("../Square/SquareGame.xml")
#        self.assertEqual(len(engine.xml_output), 643)
#        self.assertEqual(engine.xml_output, xml_file)
#
    def convert_xml_file(self, filepath):
        file_text = open(filepath, 'r').read()
        file_text_in_array = file_text.split('\n')
        result = []
        for line in file_text_in_array:
            if len(line) == 0:
                continue
            result.append(line.strip())
        return result

    def test_vm_file_seven(self):
        engine = CompilationEngine("../Seven/Main.jack", "fakeOutputfile")
        engine.compile_class()
        self.assertEqual(engine.vm_output, [
            'function Main.main 0',
            'push constant 2',
            'push constant 3',
            'call Math.multiply 2',
            'push constant 1',
            'add',
            'call Output.printInt 1',
            'pop temp 0',
            'push constant 0',
            'return'])

    def test_vm_file_convert_to_bin(self):
        engine = CompilationEngine("../ConvertToBin/Main.jack", "fakeOutputfile")
        engine.compile_class()
        self.assertEqual(engine.vm_output, [
            # **********************************************
            # function void main() {
            # **********************************************
            'function Main.main 0',

            # do Main.fillMemory(8001, 16, -1);
            'push constant 8001',
            'push constant 16',
            'push constant 1',
            'neg',
            'call Main.fillMemory 3',
            'pop temp 0',

            # let value = Memory.peek(8000);
            'push constant 8000',
            'call Memory.peek 1',
            'pop local 0',

            # do Main.convert(value);
            'push local 0',
            'call Main.convert 1',
            'pop temp 0',

            # return
            'push constant 0',
            'return',

            # **********************************************
            # function void convert(int value) {
            # **********************************************
            'function Main.convert 1',

            # let loop = true;
            'push constant 1',
            'neg',
            'pop local 2',

            # while (loop) {
        'label L1',
            # compiled (expression)
            'push local 2',
            'not',
            'if-goto L2',

            # compiled (statements)
    	    # let position = position + 1;
            'push local 1',
            'push constant 1',
            'add',
            'pop local 1',

            'goto L1',
        'label L2',

            # return;
            'push constant 0',
            'return'
            ])

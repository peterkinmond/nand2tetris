import re
import unittest
from CompilationEngine import CompilationEngine

class CompilationEngineUnitTests(unittest.TestCase):
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
                    '<identifier> Ax, category: argument, definedOrUsed: defined, index: 1 </identifier>',
                    '<symbol> , </symbol>',
                    '<keyword> int </keyword>',
                    '<identifier> Ay, category: argument, definedOrUsed: defined, index: 2 </identifier>',
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

class CompilationEngineXmlFileTests(unittest.TestCase):
    def test_square_main_file_xml(self):
        engine = CompilationEngine("../Square/Main.jack", "fakeOutputFile")
        engine.compile_class()
        xml_file = self.convert_xml_file("../Square/Main.xml")
        self.assertEqual(len(engine.xml_output), 244)
        self.assertEqual(engine.xml_output, xml_file)

    def convert_xml_file(self, filepath):
        file_text = open(filepath, 'r').read()
        file_text_in_array = file_text.split('\n')
        result = []
        for line in file_text_in_array:
            if len(line) == 0:
                continue
            result.append(line.strip())
        return result

class CompilationEngineVmFileTests(unittest.TestCase):
    """ These tests compare the VM output from the official Jack compiler
    (which was provided in the Nand2Tetris courseware) with the VM output
    from my compiler. The VM output should match for all 7 test projects.
    This gives a great safety net for refactoring the Compilation Engine.
    """
    def test_vm_file_seven(self):
        engine = CompilationEngine("../Seven/Main.jack", "fakeOutputfile")
        engine.compile_class()
        vm_file_commands = self.get_all_commands_from_vm_file("../Seven/Main.vm")
        self.assertEqual(engine.vm_writer.output, vm_file_commands)

    def test_vm_file_convert_to_bin(self):
        engine = CompilationEngine("../ConvertToBin/Main.jack", "fakeOutputfile")
        engine.compile_class()
        vm_file_commands = self.get_all_commands_from_vm_file("../ConvertToBin/Main.vm")
        self.assertEqual(engine.vm_writer.output, vm_file_commands)

    def test_vm_file_square(self):
        jack_files = [
                "../Square/Main.jack",
                "../Square/Square.jack",
                "../Square/SquareGame.jack"
        ]

        for jack_file in jack_files:
            vm_file = jack_file.replace(".jack", ".vm")
            engine = CompilationEngine(jack_file, "fakeOutputfile")
            engine.compile_class()
            vm_file_commands = self.get_all_commands_from_vm_file(vm_file)
            self.assertEqual(engine.vm_writer.output, vm_file_commands)

    def test_vm_file_average(self):
        engine = CompilationEngine("../Average/Main.jack", "fakeOutputfile")
        engine.compile_class()
        vm_file_commands = self.get_all_commands_from_vm_file("../Average/Main.vm")
        self.assertEqual(engine.vm_writer.output, vm_file_commands)

    def test_vm_file_pong(self):
        jack_files = [
                "../Pong/Ball.jack",
                "../Pong/Bat.jack",
                "../Pong/Main.jack",
                "../Pong/PongGame.jack"
        ]

        for jack_file in jack_files:
            vm_file = jack_file.replace(".jack", ".vm")
            engine = CompilationEngine(jack_file, "fakeOutputfile")
            engine.compile_class()
            vm_file_commands = self.get_all_commands_from_vm_file(vm_file)
            self.assertEqual(engine.vm_writer.output, vm_file_commands)

    def test_vm_file_complex_arrays(self):
        engine = CompilationEngine("../ComplexArrays/Main.jack", "fakeOutputfile")
        engine.compile_class()
        vm_file_commands = self.get_all_commands_from_vm_file("../ComplexArrays/Main.vm")
        self.assertEqual(engine.vm_writer.output, vm_file_commands)

    def get_all_commands_from_vm_file(self, filepath):
        file_text = open(filepath, 'r').read()
        file_text_in_array = file_text.split('\n')
        result = []
        for line in file_text_in_array:
            if len(line) == 0:
                continue
            result.append(line.strip())
        return result

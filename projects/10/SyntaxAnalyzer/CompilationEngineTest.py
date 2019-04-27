import unittest
from CompilationEngine import CompilationEngine

class CompilationEngineTest(unittest.TestCase):
    def test_compile_class(self):
        engine = CompilationEngine("BasicTestClass.jack", "BasicTestClass.xml")
        engine.compile_class()
        self.assertEqual(engine.output, [
            '<class>',
                '<keyword>class</keyword>',
                '<identifier>BasicTestClass</identifier>',
                '<symbol>{</symbol>',
                '<symbol>}</symbol>',
            '</class>'])


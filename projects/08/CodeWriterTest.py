import unittest
import colour_runner
import CodeWriter

class TestCodeWriterPush(unittest.TestCase):

    def test_push_local(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'local', 1)
        expected = [
            '// push local 1',

            '@LCL', # addr = segment + i
            'D=M',
            '@1',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@R13', # *SP = *addr
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_argument(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'argument', 2)
        expected = [
            '// push argument 2',

            '@ARG', # addr = segment + i
            'D=M',
            '@2',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@R13', # *SP = *addr
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_this(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'this', 3)
        expected = [
            '// push this 3',

            '@THIS', # addr = segment + i
            'D=M',
            '@3',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@R13', # *SP = *addr
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_that(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'that', 4)
        expected = [
            '// push that 4',

            '@THAT', # addr = segment + i
            'D=M',
            '@4',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@R13', # *SP = *addr
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_constant(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'constant', 10)
        expected = [
            '// push constant 10',

            '@10', # D = i
            'D=A',

            '@SP', # *SP = D
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_static(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'static', 5)
        expected = [
            '// push static 5',

            '@test1.5', # D = var
            'D=M',

            '@SP', # *SP = D
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_pointer_0(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'pointer', 0)
        expected = [
            '// push pointer 0',

            '@THIS', # D = THIS
            'D=M',

            '@SP', # *SP = D
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_pointer_1(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'pointer', 1)
        expected = [
            '// push pointer 1',

            '@THAT', # D = THAT
            'D=M',

            '@SP', # *SP = D
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_push_temp(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_push_command('push', 'temp', 4)
        expected = [
            '// push temp 4',

            '@5', # addr = segment + i
            'D=A',
            '@4',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@R13', # *SP = *addr
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)



class TestCodeWriterPop(unittest.TestCase):
    def test_pop_local(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'local', 1)
        expected = [
            '// pop local 1',
            '@LCL', # addr = LCL + i
            'D=M',
            '@1',
            'D=D+A', # D = LCL + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@SP', # SP--
            'M=M-1',

            '@SP',
            'A=M', # *SP, M is now value to pop
            'D=M',
            '@R13',
            'A=M',
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_pop_argument(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'argument', 2)
        expected = [
            '// pop argument 2',
            '@ARG', # addr = ARG + i
            'D=M',
            '@2',
            'D=D+A', # D = ARG + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@SP', # SP--
            'M=M-1',

            '@SP',
            'A=M', # *SP, M is now value to pop
            'D=M',
            '@R13',
            'A=M',
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_pop_this(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'this', 3)
        expected = [
            '// pop this 3',
            '@THIS', # addr = segment + i
            'D=M',
            '@3',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@SP', # SP--
            'M=M-1',

            '@SP',
            'A=M', # *SP, M is now value to pop
            'D=M',
            '@R13',
            'A=M',
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_pop_that(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'that', 4)
        expected = [
            '// pop that 4',
            '@THAT', # addr = segment + i
            'D=M',
            '@4',
            'D=D+A', # D = segment + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@SP', # SP--
            'M=M-1',

            '@SP',
            'A=M', # *SP, M is now value to pop
            'D=M',
            '@R13',
            'A=M',
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)


    # There's no pop for constant

    def test_pop_static(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'static', 5)
        expected = [
            '// pop static 5',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@test1.5', # var = D
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_pop_pointer_0(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'pointer', 0)
        expected = [
            '// pop pointer 0',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@THIS', # THIS = D
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_pop_pointer_1(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'pointer', 1)
        expected = [
            '// pop pointer 1',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@THAT', # THAT = D
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_pop_temp(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_pop_command('pop', 'temp', 4)
        expected = [
            '// pop temp 4',
            '@5', # addr = 5 + i
            'D=A',
            '@4',
            'D=D+A', # D = 5 + i
            '@R13',
            'M=D',  # R13 = D, to store it for later

            '@SP', # SP--
            'M=M-1',

            '@SP',
            'A=M', # *SP, M is now value to pop
            'D=M',
            '@R13',
            'A=M',
            'M=D'
        ]
        cw.close()
        self.assertEqual(result, expected)



class TestCodeWriterArithmetic(unittest.TestCase):

    def test_add(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_builtin_operator_command('add')
        expected = [
            '// add',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP + D
            'A=M',
            'M=M+D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_sub(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_builtin_operator_command('sub')
        expected = [
            '// sub',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP - D
            'A=M',
            'M=M-D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_neg(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_neg_command()
        expected = [
            '// neg',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = -*SP
            'A=M',
            'M=-M',

            '@SP', # SP++
            'M=M+1'

#       Sneaky way to do it. Works but feels dirty
#            '@SP', # *SP - 1 = - (*SP - 1)
#            'A=M-1',
#            'M=-M',
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_eq(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_comparison_command('eq')
        expected = [
            '// eq',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP - D
            'A=M',
            'M=M-D',

            'D=M', # if M == 0

            '@SETTRUE1',
            'D;JEQ',

            '(SETFALSE1)',
            '@SP',
            'A=M',
            'M=0', # false
            '@FINISH1',
            '0;JMP',

            '(SETTRUE1)',
            '@SP',
            'A=M',
            'M=-1', # true
            '@FINISH1',
            '0;JMP',

            '(FINISH1)',
            '@SP', # SP++
            'M=M+1',
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_gt(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_comparison_command('gt')
        expected = [
            '// gt',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP - D
            'A=M',
            'M=M-D',

            'D=M', # if M > 0

            '@SETTRUE1',
            'D;JGT',

            '(SETFALSE1)',
            '@SP',
            'A=M',
            'M=0', # false
            '@FINISH1',
            '0;JMP',

            '(SETTRUE1)',
            '@SP',
            'A=M',
            'M=-1', # true
            '@FINISH1',
            '0;JMP',

            '(FINISH1)',
            '@SP', # SP++
            'M=M+1',
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_lt(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_comparison_command('lt')
        expected = [
            '// lt',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP - D
            'A=M',
            'M=M-D',

            'D=M', # if M < 0

            '@SETTRUE1',
            'D;JLT',

            '(SETFALSE1)',
            '@SP',
            'A=M',
            'M=0', # false
            '@FINISH1',
            '0;JMP',

            '(SETTRUE1)',
            '@SP',
            'A=M',
            'M=-1', # true
            '@FINISH1',
            '0;JMP',

            '(FINISH1)',
            '@SP', # SP++
            'M=M+1',
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_and(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_builtin_operator_command('and')
        expected = [
            '// and',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP & D
            'A=M',
            'M=M&D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_or(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_builtin_operator_command('or')
        expected = [
            '// or',

            '@SP', # SP--
            'M=M-1',

            '@SP', # D = *SP
            'A=M',
            'D=M',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = *SP | D
            'A=M',
            'M=M|D',

            '@SP', # SP++
            'M=M+1'
        ]
        cw.close()
        self.assertEqual(result, expected)

    def test_not(self):
        cw = CodeWriter.CodeWriter('test1.test')
        result = cw.convert_not_command()
        expected = [
            '// not',

            '@SP', # SP--
            'M=M-1',

            '@SP', # *SP = !*SP
            'A=M',
            'M=!M',

            '@SP', # SP++
            'M=M+1'

#       Sneaky way to do it. Works but feels dirty
#            '@SP', # *SP - 1 = - (*SP - 1)
#            'A=M-1',
#            'M=!M',
        ]
        cw.close()
        self.assertEqual(result, expected)





#if __name__ == '__main__':
#    unittest.main()

#suite = unittest.TestLoader().loadTestsFromTestCase(TestCodeWriter)
#unittest.TextTestRunner(verbosity=1).run(suite)

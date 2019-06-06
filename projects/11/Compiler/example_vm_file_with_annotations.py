# I used this as a test for Compilation Engine class but
# it's since been replaced by a version of the test that checks
# an output file rather than listing 200 lines of test code. It was
# still a good illustration of the relationship between Jack code and VM commands
# so I've kept it around in this file.
  def test_vm_file_convert_to_bin_extended(self):
        engine = CompilationEngine("../ConvertToBin/Main.jack", "fakeOutputfile")
        engine.compile_class()
        self.assertEqual(engine.vm_output, [
            # **********************************************
            # function void main() {
            # **********************************************
            'function Main.main 1',

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
            'function Main.convert 3',

            # let loop = true;
            'push constant 0',
            'not',
            'pop local 2',

            # while (loop) {
        'label WHILE_EXP0',
            # compiled (expression)
            'push local 2',
            'not',
            'if-goto WHILE_END0',

            # compiled (statements)
            # let position = position + 1;
            'push local 1',
            'push constant 1',
            'add',
            'pop local 1',

            # let mask = Main.nextMask(mask);
            'push local 0',
            'call Main.nextMask 1',
            'pop local 0',

            # if (~(position > 16)) {
            'push local 1',
            'push constant 16',
            'gt',
            'not',

            'if-goto IF_TRUE0',
            'goto IF_FALSE0',
        'label IF_TRUE0',
            # compiled (statements1)

            # if (~((value & mask) = 0)) {
            'push argument 0',
            'push local 0',
            'and',
            'push constant 0',
            'eq',
            'not',

            'if-goto IF_TRUE1',
            'goto IF_FALSE1',
        'label IF_TRUE1',
            # compiled (statements1)
            # do Memory.poke(8000 + position, 1);
            'push constant 8000',
            'push local 1',
            'add',
            'push constant 1',
            'call Memory.poke 2',
            'pop temp 0',

            'goto IF_END1',
        'label IF_FALSE1',
            # compiled (statements2)
            # do Memory.poke(8000 + position, 0);
            'push constant 8000',
            'push local 1',
            'add',
            'push constant 0',
            'call Memory.poke 2',
            'pop temp 0',

        'label IF_END1',

            'goto IF_END0',
        'label IF_FALSE0',

            # compiled (statements2)
            # let loop = false;
            'push constant 0',
            'pop local 2',

        'label IF_END0',

            'goto WHILE_EXP0',
        'label WHILE_END0',

            # return;
            'push constant 0',
            'return',

            # **********************************************
            # function int nextMask(int mask) {
            # **********************************************
            'function Main.nextMask 0',

            # if (mask = 0) {
            # compiled (expression)
            'push argument 0',
            'push constant 0',
            'eq',

            'if-goto IF_TRUE0',
            'goto IF_FALSE0',
        'label IF_TRUE0',

            # compiled (statements1)
            # return 1;
            'push constant 1',
            'return',

            'goto IF_END0',
        'label IF_FALSE0',

            # compiled (statements2)
            # return mask * 2;
            'push argument 0',
            'push constant 2',
            'call Math.multiply 2',
            'return',
        'label IF_END0',

            # **********************************************
            # function void fillMemory(int startAddress, int length, int value) {
            # **********************************************
            'function Main.fillMemory 0',

            # while (length > 0) {
        'label WHILE_EXP0',
            # compiled (expression)
            'push argument 1',
            'push constant 0',
            'gt',

            'not',
            'if-goto WHILE_END0',

            # compiled (statements)
            # do Memory.poke(startAddress, value);
            'push argument 0',
            'push argument 2',
            'call Memory.poke 2',
            'pop temp 0',

            # let length = length - 1;
            'push argument 1',
            'push constant 1',
            'sub',
            'pop argument 1',

            # let startAddress = startAddress + 1;
            'push argument 0',
            'push constant 1',
            'add',
            'pop argument 0',

            'goto WHILE_EXP0',
        'label WHILE_END0',

            # return
            'push constant 0',
            'return'


            ])

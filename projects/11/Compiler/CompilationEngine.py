import re
from Constants import *
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine(object):
    """CompilationEngine: generates the compiler's output."""

    def __init__(self, input_file, output_file, use_text_as_input=False):
        """Creates a new compilation engine with the
        given input and output.

        The next routine called must be compile_class
        """
        self.class_name = ""
        self.tokenizer = JackTokenizer(input_file, use_text_as_input)
        self.output_file = output_file
        self.xml_output = []
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter()
        self.if_loop_index = None
        self.while_loop_index = None

    def save_output_file(self):
        file = open(self.output_file, 'w')
        for line in self.vm_writer.output:
            file.write(line + '\n')

    def compile_class(self):
        """Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.xml_output.append('<class>') # output <class>
        self._handle_keyword() # 'class'
        self.class_name = self._handle_identifier(CLASS, DEFINED) # className
        self._handle_symbol() # '{'

        # classVarDec*
        while self.tokenizer.peek_at_next_token() in [STATIC, FIELD]:
            self.compile_class_var_dec()

        # subroutineDec*
        while self.tokenizer.peek_at_next_token() in [CONSTRUCTOR, FUNCTION, METHOD]:
            self.symbol_table.start_subroutine()
            self.if_loop_index = None
            self.while_loop_index = None
            self.compile_subroutine_dec()

        self._handle_symbol() # '}'
        self.xml_output.append('</class>') # output </class>

    def compile_class_var_dec(self):
        """Compiles a static variable declaration,
        or a field declaration.
        classVarDec: ('static'|'field') type varName(',' varName)* ';'
        """
        self.xml_output.append('<classVarDec>') # output <classVarDec>
        category = self._handle_keyword() # ('static'|'field')
        type = self._handle_type() # type
        self._handle_identifier(category, DEFINED, type) # varName

        while (self.tokenizer.peek_at_next_token() == ','):
            self._handle_symbol() # ','
            self._handle_identifier(category, DEFINED, type) # varName

        self._handle_symbol() # ';'
        self.xml_output.append('</classVarDec>') # output <classVarDec>

    def compile_subroutine_dec(self):
        """Compiles a complete method, function, or constructor.
        subroutineDec: ('constructor'|'function'|'method') ('void'|type)
            subroutineName '(' parameterList ')' subroutineBody
        """
        self.xml_output.append('<subroutineDec>')
        subroutine_type = self._handle_keyword() # ('constructor'|'function'|'method')

        if self.tokenizer.peek_at_next_token() == VOID:
            self._handle_keyword() # 'void'
        else:
            self._handle_type() # type

        subroutine_name = self._handle_identifier(SUBROUTINE, DEFINED) # subroutineName
        if subroutine_type == METHOD:
            # Add "this" to symbol table to represent object
            self.symbol_table.define(THIS, self.class_name, ARGUMENT)

        self._handle_symbol() # '('
        self.compile_parameter_list()
        self._handle_symbol() # ')'

        var_count = self.compile_subroutine_body_vars()
        self.vm_writer.write_function(self.class_name + "." + subroutine_name, var_count)
        if subroutine_type == CONSTRUCTOR:
            field_count = self.symbol_table.var_count(FIELD)
            self.vm_writer.write_push(CONSTANT, field_count)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop(POINTER, 0)
        elif subroutine_type == METHOD:
            self.vm_writer.write_push(ARGUMENT, 0)
            self.vm_writer.write_pop(POINTER, 0)

        self.compile_subroutine_body_statements()

        self.xml_output.append('</subroutineDec>')

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list.
        Does not handle the enclosing "()".
        parameterList: ((type varName) (',' type varName)*)?
        """
        self.xml_output.append('<parameterList>')
        count = 0

        # ((type varName) (',' type varName)*)?
        if self.tokenizer.peek_at_next_token() != ')':
            type = self._handle_type() # type
            self._handle_identifier(ARGUMENT, DEFINED, type) # varName
            count += 1
            while self.tokenizer.peek_at_next_token() != ')':
                self._handle_symbol() # ','
                type = self._handle_type() # type
                self._handle_identifier(ARGUMENT, DEFINED, type) # varName
                count += 1

        self.xml_output.append('</parameterList>')
        return count

    def compile_subroutine_body_vars(self):
        """Compiles a subroutine's body.
        subroutineBody: '{' varDec* statements '}'
        """
        self.xml_output.append('<subroutineBody>')
        var_count = 0
        self._handle_symbol() # '{'

        while self.tokenizer.peek_at_next_token() == VAR:
            var_count += self.compile_var_dec()

        return var_count

    def compile_subroutine_body_statements(self):
        self.compile_statements()
        self._handle_symbol() # '}'
        self.xml_output.append('</subroutineBody>')

    def compile_var_dec(self):
        """Compiles a var declaration.
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.xml_output.append('<varDec>') # output <varDec>
        count = 0
        self._handle_keyword() # 'var'
        type = self._handle_type() # type
        self._handle_identifier(LOCAL, DEFINED, type) # varName
        count += 1

        while (self.tokenizer.peek_at_next_token() == ','):
            self._handle_symbol() # ','
            self._handle_identifier(LOCAL, DEFINED, type) # varName
            count += 1

        self._handle_symbol() # ';'
        self.xml_output.append('</varDec>') # output <varDec>
        return count

    def compile_statements(self):
        """Compiles a sequence of statements.
        Does not handle the enclosing "{}".
        statements: statement*
        """
        self.xml_output.append('<statements>') # output <statements>
        next_token = self.tokenizer.peek_at_next_token()
        while next_token in [LET, IF, WHILE, DO, RETURN]:
            if next_token == LET:
                self.compile_let()
            elif next_token == IF:
                self.compile_if()
            elif next_token == WHILE:
                self.compile_while()
            elif next_token == DO:
                self.compile_do()
            elif next_token == RETURN:
                self.compile_return()
            next_token = self.tokenizer.peek_at_next_token()
        self.xml_output.append('</statements>') # output </statements>

    def compile_let(self):
        """Compiles a let statement.
        letStatement: 'let' varName('[' expression ']')? '=' expression ';'
        """
        self.xml_output.append('<letStatement>') # output <letStatement>
        self._handle_keyword() # 'let'
        value = self._handle_identifier(definedOrUsed=USED) # varName
        segment = self.symbol_table.kind_of(value)
        index = self.symbol_table.index_of(value)
        is_array = False

        if self.tokenizer.peek_at_next_token() == '[':
            self._handle_symbol() # '['
            self.compile_expression() # expression
            self._handle_symbol() # ']'

            # Assigning to array index - get offset and add to base address
            self.vm_writer.write_push(segment, index)
            self.vm_writer.write_arithmetic('add')
            is_array = True

        self._handle_symbol() # '='
        self.compile_expression() # expression
        self._handle_symbol() # ';'
        self.xml_output.append('</letStatement>') # output </letStatement>

        if is_array:
            # Array access has specific set of VM commands
            self.vm_writer.write_pop(TEMP, 0)
            self.vm_writer.write_pop(POINTER, 1)
            self.vm_writer.write_push(TEMP, 0)
            self.vm_writer.write_pop(THAT, 0)
        else:
            # "let" statements assign a value to a var so pop the value to the var
            self.vm_writer.write_pop(segment, index)

    def _get_next_if_loop_index(self):
        if self.if_loop_index == None:
            self.if_loop_index = 0
        else:
            self.if_loop_index += 1

        return self.if_loop_index

    def _get_next_while_loop_index(self):
        if self.while_loop_index == None:
            self.while_loop_index = 0
        else:
            self.while_loop_index += 1

        return self.while_loop_index


    def compile_if(self):
        """Compiles a if statement.
        ifStatement: 'if' '(' expression ')' '{' statements '}'
            ('else' '{' statements '}')?
        """
        self.xml_output.append('<ifStatement>') # output <ifStatement>

        counter = self._get_next_if_loop_index()

        self._handle_keyword() # 'if'
        self._handle_symbol() # '('
        self.compile_expression() # expression
        self._handle_symbol() # ')'

        self.vm_writer.write_if(f"IF_TRUE{counter}")
        self.vm_writer.write_goto(f"IF_FALSE{counter}")
        self.vm_writer.write_label(f"IF_TRUE{counter}")

        self._handle_symbol() # '{'
        self.compile_statements() # statements
        self._handle_symbol() # '}'

        if self.tokenizer.peek_at_next_token() == ELSE:
            self.vm_writer.write_goto(f"IF_END{counter}")
            self.vm_writer.write_label(f"IF_FALSE{counter}")

            self._handle_keyword() # 'else'
            self._handle_symbol() # '{'
            self.compile_statements() # statements
            self._handle_symbol() # '}'

            self.vm_writer.write_label(f"IF_END{counter}")
        else:
            self.vm_writer.write_label(f"IF_FALSE{counter}")

        self.xml_output.append('</ifStatement>') # output </ifStatement>

    def compile_while(self):
        """Compiles a while statement.
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        self.xml_output.append('<whileStatement>') # output <whileStatement>
        self._handle_keyword() # 'while'

        counter = self._get_next_while_loop_index()
        self.vm_writer.write_label(f"WHILE_EXP{counter}")

        self._handle_symbol() # '('
        self.compile_expression() # expression
        self._handle_symbol() # ')'

        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if(f"WHILE_END{counter}")

        self._handle_symbol() # '{'
        self.compile_statements() # statements
        self._handle_symbol() # '}'

        self.vm_writer.write_goto(f"WHILE_EXP{counter}")
        self.vm_writer.write_label(f"WHILE_END{counter}")

        self.xml_output.append('</whileStatement>') # output </whileStatement>

    def compile_do(self):
        """Compiles a do statement.
        doStatement: 'do' subroutineCall ';'
        """
        self.xml_output.append('<doStatement>') # output <doStatement>
        self._handle_keyword() # 'do'
        self.compile_subroutine_call() # subroutineCall
        self._handle_symbol() # ';'
        self.xml_output.append('</doStatement>') # output </doStatement>

        # "do" statements have an implicit empty return value
        # which we handle by calling "pop temp 0"
        self.vm_writer.write_pop("temp", 0)

    def compile_subroutine_call(self):
        """subroutineCall: subroutineName'('expressionList')'|
            (className|varName)'.'subroutineName'('expressionList')'
        """
        subroutine_name = self._handle_identifier(definedOrUsed=USED) # subroutineName or (className|varName)
        self._handle_subroutine(subroutine_name)

    def _handle_subroutine(self, subroutine_name):
        expression_count = 0

        if self.tokenizer.peek_at_next_token() == '.':
            if self.symbol_table.is_in_symbol_table(subroutine_name):
                # Method is being called on var
                # Need to push var (object) representing that class prior to calling the method
                segment = self.symbol_table.kind_of(subroutine_name)
                index = self.symbol_table.index_of(subroutine_name)
                self.vm_writer.write_push(segment, index)
                # Need to replace var name with the class name for VM command
                subroutine_name = self.symbol_table.type_of(subroutine_name)
                expression_count += 1 # Count the calling object as an expression that gets passed

            subroutine_name += str(self._handle_symbol()) # '.'
            subroutine_name += self._handle_identifier(SUBROUTINE, USED) # subroutineName
        else:
            # Method is being called on object instance
            subroutine_name = f"{self.class_name}.{subroutine_name}"
            expression_count += 1 # Count the calling object as an expression that gets passed
            self.vm_writer.write_push(POINTER, 0)

        self._handle_symbol() # '('
        expression_count += self.compile_expression_list() # expressionList
        self._handle_symbol() # ')'
        self.vm_writer.write_call(subroutine_name, expression_count)

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions.
        expressionList: (expression (','expression)* )?
        """
        self.xml_output.append('<expressionList>') # output <expressionList>
        count = 0

        if self.tokenizer.peek_at_next_token() != ')':
            self.compile_expression() # expression
            count += 1
            while self.tokenizer.peek_at_next_token() != ')':
                self._handle_symbol() # ','
                self.compile_expression() # type
                count += 1
        self.xml_output.append('</expressionList>') # output </expressionList>
        return count

    def compile_return(self):
        """Compiles a return statement.
        returnStatement: 'return' expression? ';'
        """
        self.xml_output.append('<returnStatement>') # output <returnStatement>
        self._handle_keyword() # 'return'

        if (self.tokenizer.peek_at_next_token() != ';'):
            self.compile_expression()
        else:
            # Every Jack function needs to return some value, so for "return"
            # statements without an explicit value, we use constant 0 as a default
            self.vm_writer.write_push(CONSTANT, 0)

        self._handle_symbol() # ';'
        self.xml_output.append('</returnStatement>') # output </returnStatement>

        self.vm_writer.write_return()

    def compile_expression(self):
        """Compiles an expression.
        expression: term (op term)*
        """
        self.xml_output.append('<expression>') # output <expression>

        # Need to compile ops after the terms
        ops = []
        self.compile_term()

        while (self.tokenizer.peek_at_next_token() in OPS):
            ops.append(self._handle_symbol()) # op
            self.compile_term() # term

        self.xml_output.append('</expression>') # output </expression>

        for op in ops:
            self.vm_writer.write_arithmetic(op)

    def compile_term(self):
        """Compiles a term. If the current token is an identifier,
        the routine must distinguish between a variable, an array entry,
        or a subroutine call. A single look-ahead token, which may
        be one of "[", "(", or ".", suffices to distinguish between
        the possibilities. Any other token is not part of this term
        and should not be advanced over.

        term: integerConstant|stringConstant|keywordConstant|varName|
            varName'['expression']'|subroutineCall|'('expression')'|unaryOp term
        """
        self.xml_output.append('<term>') # output <term>

        next_token = self.tokenizer.peek_at_next_token()

        if next_token.isdigit():
            print(f"type - numeric constant: {next_token}")
            self._handle_int_const()
        elif next_token.startswith('"') and next_token.endswith('"'):
            print(f"type - string constnat: {next_token}")
            self._handle_string_const()
        elif next_token in KEYWORDS:
            self._handle_keyword()
        elif self.tokenizer.is_identifier(next_token):
            print(f"type - identifier: {next_token}")
            next_next_token = self.tokenizer.peek_at_next_next_token()
            if next_next_token == '.': # subroutineCall
                print(f"type - identifier - subroutine: {next_token}")
                self.compile_subroutine_call()
            elif next_next_token == "[": # varname'['expression']'
                print(f"type - array access 'a[b]': {next_token}")
                array_var = self._handle_identifier(definedOrUsed=USED) # varname
                self._handle_symbol() # '['
                self.compile_expression() # expression
                self._handle_symbol() # ']'

                segment = self.symbol_table.kind_of(array_var)
                index = self.symbol_table.index_of(array_var)
                self.vm_writer.write_push(segment, index)

                self.vm_writer.write_arithmetic('add')
                self.vm_writer.write_pop(POINTER, 1)
                self.vm_writer.write_push(THAT, 0)
            elif self.symbol_table.is_in_symbol_table(next_token): # symbol
                print(f"type - identifier - symbol: {next_token}")
                segment = self.symbol_table.kind_of(next_token)
                index = self.symbol_table.index_of(next_token)
                self.vm_writer.write_push(segment, index)
                self._handle_identifier(definedOrUsed=USED) # symbol
            else:
                raise Exception(f"identifier not matched: {next_token}")
        elif next_token == '(': # '('expression')'
            print(f"type - new expression: {next_token}")
            self._handle_symbol() # '('
            self.compile_expression()
            self._handle_symbol() # ')'
        elif next_token in ['-', '~']: # unaryOp term
            print(f"type - unaryOp: {next_token}")
            op = self._handle_symbol()
            self.compile_term()
            self.vm_writer.write_arithmetic(op, unary = True)
        else:
            raise Exception(f"Token not matched: {next_token}")

        self.xml_output.append('</term>') # output </term>

    def _handle_type(self):
        """ type: 'int'|'char'|'boolean'|className"""
        if self.tokenizer.peek_at_next_token() in [INT, CHAR, BOOLEAN]:
            return self._handle_keyword()
        else:
            return self._handle_identifier(CLASS, USED)

    def _handle_keyword(self):
        self.tokenizer.advance()

        if self.tokenizer.keyword() == THIS:
            self.vm_writer.write_push(POINTER, 0)
        elif self.tokenizer.keyword() in ['null', 'false', 'true']:
            # "null/false" represented by CONSTANT 0, "true" represented by NOT 0
            self.vm_writer.write_push(CONSTANT, 0)
            if self.tokenizer.keyword() == TRUE:
                self.vm_writer.write_arithmetic("~", unary = True)

        self.xml_output.append(f"<keyword> {self.tokenizer.keyword()} </keyword>")
        return self.tokenizer.keyword()

    def _handle_identifier(self, category=None, definedOrUsed=None, type=None):
        self.tokenizer.advance()
        if category is None:
            if self.symbol_table.is_in_symbol_table(self.tokenizer.identifier()):
                category = self.symbol_table.kind_of(self.tokenizer.identifier())
            elif self.symbol_table.is_type(self.tokenizer.identifier()):
                # Symbol table stores Class names as type
                category = CLASS
            else:
                category = SUBROUTINE

        identifier = f"{self.tokenizer.identifier()}, category: {category}, definedOrUsed: {definedOrUsed}"

        # TODO: Move "add to symbol table" logic into compile_* methods? Sort of unexpected
        # to have it happen as side-effect of this method
        if category in [LOCAL, ARGUMENT, STATIC, FIELD]:
            index = None
            if self.symbol_table.index_of(self.tokenizer.current_token) == None:
                # Symbol not yet in table - add it
                self.symbol_table.define(self.tokenizer.current_token, type, category)

            index = self.symbol_table.index_of(self.tokenizer.current_token)
            identifier += f", index: {index}"
        self.xml_output.append(f"<identifier> {identifier} </identifier>")
        return self.tokenizer.identifier()

    def _handle_symbol(self):
        self.tokenizer.advance()
        self.xml_output.append(f"<symbol> {self.tokenizer.symbol()} </symbol>")
        return self.tokenizer.symbol()

    def _handle_int_const(self):
        self.tokenizer.advance()
        self.vm_writer.write_push(CONSTANT, self.tokenizer.current_token)
        self.xml_output.append(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")

    def _handle_string_const(self):
        self.tokenizer.advance()
        string_const = self.tokenizer.string_val()
        self.vm_writer.write_push(CONSTANT, len(string_const))
        self.vm_writer.write_call('String.new', 1)

        for letter in string_const:
            self.vm_writer.write_push(CONSTANT, ord(letter))
            self.vm_writer.write_call('String.appendChar', 2)

        self.xml_output.append(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")

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
        self.vm_output = []
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter()

    def save_output_file(self):
        file = open(self.output_file, 'w')
        for line in self.vm_output:
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
        self._handle_keyword() # ('constructor'|'function'|'method')

        if self.tokenizer.peek_at_next_token() == VOID:
            self._handle_keyword() # 'void'
        else:
            self._handle_type() # type

        subroutine_name = self._handle_identifier(SUBROUTINE, DEFINED) # subroutineName
        self._handle_symbol() # '('
        parameter_count = self.compile_parameter_list()
        self._handle_symbol() # ')'
        self.vm_output.append(self.vm_writer.write_function(self.class_name + "." + subroutine_name, parameter_count))
        self.compile_subroutine_body()

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
            while self.tokenizer.peek_at_next_token() != ')':
                self._handle_symbol() # ','
                type = self._handle_type() # type
                self._handle_identifier(ARGUMENT, DEFINED, type) # varName

        self.xml_output.append('</parameterList>')
        return count

    def compile_subroutine_body(self):
        """Compiles a subroutine's body.
        subroutineBody: '{' varDec* statements '}'
        """
        self.xml_output.append('<subroutineBody>')
        self._handle_symbol() # '{'

        while self.tokenizer.peek_at_next_token() == VAR:
            self.compile_var_dec()

        self.compile_statements()
        self._handle_symbol() # '}'
        self.xml_output.append('</subroutineBody>')

    def compile_var_dec(self):
        """Compiles a var declaration.
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.xml_output.append('<varDec>') # output <varDec>
        category = self._handle_keyword() # 'var'
        type = self._handle_type() # type
        self._handle_identifier(category, DEFINED, type) # varName

        while (self.tokenizer.peek_at_next_token() == ','):
            self._handle_symbol() # ','
            self._handle_identifier(category, DEFINED, type) # varName

        self._handle_symbol() # ';'
        self.xml_output.append('</varDec>') # output <varDec>

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
        self._handle_identifier(definedOrUsed=USED) # varName

        if self.tokenizer.peek_at_next_token() == '[':
            self._handle_symbol() # '['
            self.compile_expression() # expression
            self._handle_symbol() # ']'

        self._handle_symbol() # '='
        self.compile_expression() # expression
        self._handle_symbol() # ';'
        self.xml_output.append('</letStatement>') # output </letStatement>

    def compile_if(self):
        """Compiles a if statement.
        ifStatement: 'if' '(' expression ')' '{' statements '}'
            ('else' '{' statements '}')?
        """
        self.xml_output.append('<ifStatement>') # output <ifStatement>
        self._handle_keyword() # 'if'
        self._handle_symbol() # '('
        self.compile_expression() # expression
        self._handle_symbol() # ')'
        self._handle_symbol() # '{'
        self.compile_statements() # statements
        self._handle_symbol() # '}'

        if self.tokenizer.peek_at_next_token() == ELSE:
            self._handle_keyword() # 'if'
            self._handle_symbol() # '{'
            self.compile_statements() # statements
            self._handle_symbol() # '}'

        self.xml_output.append('</ifStatement>') # output </ifStatement>

    def compile_while(self):
        """Compiles a while statement.
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        self.xml_output.append('<whileStatement>') # output <whileStatement>
        self._handle_keyword() # 'while'
        self._handle_symbol() # '('
        self.compile_expression() # expression
        self._handle_symbol() # ')'
        self._handle_symbol() # '{'
        self.compile_statements() # statements
        self._handle_symbol() # '}'
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

    def compile_subroutine_call(self):
        """subroutineCall: subroutineName'('expressionList')'|
            (className|varName)'.'subroutineName'('expressionList')'
        """
        subroutine_name = self._handle_identifier(definedOrUsed=USED) # subroutineName or (className|varName)
        if self.tokenizer.peek_at_next_token() == '.':
            subroutine_name += str(self._handle_symbol()) # '.'
            subroutine_name += self._handle_identifier(SUBROUTINE, USED) # subroutineName
        self._handle_symbol() # '('
        expression_count = self.compile_expression_list() # expressionList
        self._handle_symbol() # ')'
        self.vm_output.append(self.vm_writer.write_call(subroutine_name, expression_count))
        self.vm_output.append(self.vm_writer.write_pop("temp", 0))

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

        self._handle_symbol() # ';'
        self.xml_output.append('</returnStatement>') # output </returnStatement>

        # TODO: Handle case when there's a return value
        self.vm_output.append(self.vm_writer.write_push("constant", 0))
        self.vm_output.append(self.vm_writer.write_return())

    def compile_expression(self):
        """Compiles an expression.
        expression: term (op term)*
        """
        self.xml_output.append('<expression>') # output <expression>
        expression = []
        expression.append(self.compile_term())

        while (self.tokenizer.peek_at_next_token() in OPS):
            expression.append(self._handle_symbol()) # op
            expression.append(self.compile_term()) # term

        self.xml_output.append('</expression>') # output </expression>
        self.code_write(expression)
        return expression

    def code_write(self, exp):
        print(f"exp is {exp}")

        if type(exp) is not list and str(exp).isdigit():
            print('here 1')
            self.vm_output.append(self.vm_writer.write_push("constant", exp))
            return
        elif type(exp) is list and len(exp) == 1:
            # Terms are wrapped in a list so unpack them
            self.code_write(exp[0])
            return
        # TODO: What's better way to handle expression list? I think
        # they should be ignored since they'll be handled by a different
        # call to code_write
        elif exp[0] == "(":
            print('here 2')
            return
        elif len(exp) == 3 and exp[1] in OPS: # if exp is "exp1 op exp2":
            print('here 3')
            self.code_write(exp[0])
            self.code_write(exp[2])
            self.vm_output.append(self.vm_writer.write_arithmetic(exp[1]))
        # TODO: Add exception else clause once all expected conditions handled
        #else:
        #    raise Exception(f"Can't write code for expression {exp}")
        # if exp is a variable var:
        #   output "push var"

        # if exp is "exp1 op exp2":
        #   code_write(exp1),
        #   code_write(exp2),
        #   output "op"

        # if exp is "f(exp1, exp2, ...)":
        #   code_write(exp1),
        #   code_write(exp2), ...,
        #   output "call f"

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
        term = []
        next_token = self.tokenizer.peek_at_next_token()
        if next_token.isdigit():
            term.append(self._handle_int_const())
        elif next_token.startswith('"') and next_token.endswith('"'):
            term.append(self._handle_string_const())
        elif next_token in KEYWORDS:
            term.append(self._handle_keyword())
        elif re.match(r'^\w+$', next_token):
            term.append(self._handle_identifier(definedOrUsed=USED))
            next_token = self.tokenizer.peek_at_next_token()
            if next_token == '[': # varName'['expression']'
                term.append(self._handle_symbol()) # '['
                term.append(self.compile_expression()) # expression
                term.append(self._handle_symbol()) # ']'
            elif next_token == '(': # subroutineCall
                term.append(self._handle_symbol()) # '('
                term.append(self.compile_expression_list()) # expressionList
                term.append(self._handle_symbol()) # ')'
            elif next_token == '.': # subroutineCall
                term.append(self._handle_symbol()) # '.'
                term.append(self._handle_identifier(SUBROUTINE, USED)) # subroutineName
                term.append(self._handle_symbol()) # '('
                term.append(self.compile_expression_list()) # expressionList
                term.append(self._handle_symbol()) # ')'
        elif next_token == '(': # '('expression')'
            term.append(self._handle_symbol()) # '('
            term.append(self.compile_expression()) # expression
            term.append(self._handle_symbol()) # ')'
        elif next_token in ['-', '~']: # unaryOp term
            term.append(self._handle_symbol())
            term.append(self.compile_term())
        else:
            raise Exception("Token '{}' not matched to any term".format(self.tokenizer.current_token))

        self.xml_output.append('</term>') # output </term>
        return term

    def _handle_type(self):
        """ type: 'int'|'char'|'boolean'|className"""
        if self.tokenizer.peek_at_next_token() in [INT, CHAR, BOOLEAN]:
            return self._handle_keyword()
        else:
            return self._handle_identifier(CLASS, USED)

    def _handle_keyword(self):
        self.tokenizer.advance()
        self.xml_output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))
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

        identifier = "{}, category: {}, definedOrUsed: {}".format(self.tokenizer.identifier(), category, definedOrUsed)

        # TODO: Move "add to symbol table" logic into compile_* methods? Sort of unexpected
        # to have it happen as side-effect of this method
        if category in [VAR, ARGUMENT, STATIC, FIELD]:
            index = None
            if self.symbol_table.index_of(self.tokenizer.current_token) == None:
                # Symbol not yet in table - add it
                self.symbol_table.define(self.tokenizer.current_token, type, category)

            index = self.symbol_table.index_of(self.tokenizer.current_token)
            identifier += ", index: {}".format(index)
        self.xml_output.append("<identifier> {} </identifier>".format(identifier))
        return self.tokenizer.identifier()

    def _handle_symbol(self):
        self.tokenizer.advance()
        self.xml_output.append("<symbol> {} </symbol>".format(self.tokenizer.symbol()))
        return self.tokenizer.symbol()

    def _handle_int_const(self):
        self.tokenizer.advance()
        self.xml_output.append("<integerConstant> {} </integerConstant>".format(self.tokenizer.int_val()))
        # self.vm_output.append(self.vm_writer.write_push("constant", self.tokenizer.int_val()))
        return self.tokenizer.int_val()

    def _handle_string_const(self):
        self.tokenizer.advance()
        self.xml_output.append("<stringConstant> {} </stringConstant>".format(self.tokenizer.string_val()))
        return self.tokenizer.string_val()

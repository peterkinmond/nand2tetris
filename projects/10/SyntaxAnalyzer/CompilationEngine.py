from Constants import *
from JackTokenizer import JackTokenizer

class CompilationEngine(object):
    """CompilationEngine: generates the compiler's output."""

    def __init__(self, input_file, output_file, use_text_as_input=False):
        """Creates a new compilation engine with the
        given input and output.

        The next routine called must be compile_class
        """
        self.tokenizer = JackTokenizer(input_file, use_text_as_input)
        self.output_file = output_file
        self.output = []

    def save_output_file(self):
        file = open(self.output_file, 'w')
        for line in self.output:
            file.write(line + '\n')

    def compile_class(self):
        """Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.output.append('<class>') # output <class>
        self._handle_keyword() # 'class'
        self._handle_identifier() # className
        self._handle_symbol() # '{'

        # classVarDec*
        while self.tokenizer.peek_at_next_token() in [STATIC, FIELD]:
            self.compile_class_var_dec()

        # subroutineDec*
        while self.tokenizer.peek_at_next_token() in [CONSTRUCTOR, FUNCTION, METHOD]:
            self.compile_subroutine_dec()

        self._handle_symbol() # '}'
        self.output.append('</class>') # output </class>

    def compile_class_var_dec(self):
        """Compiles a static variable declaration,
        or a field declaration.
        classVarDec: ('static'|'field') type varName(',' varName)* ';'
        """
        self.output.append('<classVarDec>') # output <classVarDec>
        self._handle_keyword() # ('static'|'field')
        self._handle_type() # type
        self._handle_identifier() # varName

        while (self.tokenizer.peek_at_next_token() == ','):
            self._handle_symbol() # ','
            self._handle_identifier() # varName

        self._handle_symbol() # ';'
        self.output.append('</classVarDec>') # output <classVarDec>

    def compile_subroutine_dec(self):
        """Compiles a complete method, function, or constructor.
        subroutineDec: ('constructor'|'function'|'method') ('void'|type)
            subroutineName '(' parameterList ')' subroutineBody
        """
        self.output.append('<subroutineDec>')
        self._handle_keyword() # ('constructor'|'function'|'method')

        if self.tokenizer.peek_at_next_token() == VOID:
            self._handle_keyword() # 'void'
        else:
            self._handle_type() # type

        self._handle_identifier() # subroutineName
        self._handle_symbol() # '('
        self.compile_parameter_list()
        self._handle_symbol() # ')'
        self.compile_subroutine_body()
        self.output.append('</subroutineDec>')

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list.
        Does not handle the enclosing "()".
        parameterList: ((type varName) (',' type varName)*)?
        """
        self.output.append('<parameterList>')

        # ((type varName) (',' type varName)*)?
        if self.tokenizer.peek_at_next_token() != ')':
            self._handle_type() # type
            self._handle_identifier() # varName
            while self.tokenizer.peek_at_next_token() != ')':
                self._handle_symbol() # ','
                self._handle_type() # type
                self._handle_identifier() # varName

        self.output.append('</parameterList>')

    def compile_subroutine_body(self):
        """Compiles a subroutine's body.
        subroutineBody: '{' varDec* statements '}'
        """
        self.output.append('<subroutineBody>')
        self._handle_symbol() # '{'

        while self.tokenizer.peek_at_next_token() == VAR:
            self.compile_var_dec()

        self.compile_statements()
        self._handle_symbol() # '}'
        self.output.append('</subroutineBody>')

    def compile_var_dec(self):
        """Compiles a var declaration.
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.output.append('<varDec>') # output <varDec>
        self._handle_keyword() # 'var'
        self._handle_type() # type
        self._handle_identifier() # varName

        while (self.tokenizer.peek_at_next_token() == ','):
            self._handle_symbol() # ','
            self._handle_identifier() # varName

        self._handle_symbol() # ';'
        self.output.append('</varDec>') # output <varDec>

    def compile_statements(self):
        """Compiles a sequence of statements.
        Does not handle the enclosing "{}".
        statements: statement*
        """
        self.output.append('<statements>') # output <statements>
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
        self.output.append('</statements>') # output </statements>

    def compile_let(self):
        """Compiles a let statement.
        letStatement: 'let' varName('[' expression ']')? '=' expression ';'
        """
        self.output.append('<letStatement>') # output <letStatement>
        self._handle_keyword() # 'let'
        self._handle_identifier() # varName

        if self.tokenizer.peek_at_next_token() == '[':
            self._handle_symbol() # '['
            self.compile_expression() # expression
            self._handle_symbol() # ']'

        self._handle_symbol() # '='
        self.compile_expression() # expression
        self._handle_symbol() # ';'
        self.output.append('</letStatement>') # output </letStatement>

    def compile_if(self):
        """Compiles a if statement.
        ifStatement: 'if' '(' expression ')' '{' statements '}'
            ('else' '{' statements '}')?
        """
        self.output.append('<ifStatement>') # output <ifStatement>
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

        self.output.append('</ifStatement>') # output </ifStatement>

    def compile_while(self):
        """Compiles a while statement.
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        self.output.append('<whileStatement>') # output <whileStatement>
        self._handle_keyword() # 'while'
        self._handle_symbol() # '('
        self.compile_expression() # expression
        self._handle_symbol() # ')'
        self._handle_symbol() # '{'
        self.compile_statements() # statements
        self._handle_symbol() # '}'
        self.output.append('</whileStatement>') # output </whileStatement>

    def compile_do(self):
        """Compiles a do statement.
        doStatement: 'do' subroutineCall ';'
        """
        self.output.append('<doStatement>') # output <doStatement>
        self._handle_keyword() # 'do'
        self.compile_subroutine_call() # subroutineCall
        self._handle_symbol() # ';'
        self.output.append('</doStatement>') # output </doStatement>

    def compile_subroutine_call(self):
        """subroutineCall: subroutineName'('expressionList')'|
            (className|varName)'.'subroutineName'('expressionList')'
        """
        self._handle_identifier() # subroutineName or (className|varName)
        if self.tokenizer.peek_at_next_token() == '.':
            self._handle_symbol() # '.'
            self._handle_identifier() # subroutineName
        self._handle_symbol() # '('
        self.compile_expression_list() # expressionList
        self._handle_symbol() # ')'

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions.
        expressionList: (expression (','expression)* )?
        """
        self.output.append('<expressionList>') # output <expressionList>
        if self.tokenizer.peek_at_next_token() != ')':
            self.compile_expression() # expression
            while self.tokenizer.peek_at_next_token() != ')':
                self._handle_symbol() # ','
                self.compile_expression() # type
        self.output.append('</expressionList>') # output </expressionList>

    def compile_return(self):
        """Compiles a return statement.
        returnStatement: 'return' expression? ';'
        """
        self.output.append('<returnStatement>') # output <returnStatement>
        self._handle_keyword() # 'return'

        if (self.tokenizer.peek_at_next_token() != ';'):
            self.compile_expression()

        self._handle_symbol() # ';'
        self.output.append('</returnStatement>') # output </returnStatement>

    def compile_expression(self):
        """Compiles an expression.
        expression: term (op term)*
        """
        self.output.append('<expression>') # output <expression>
        self.compile_term()

        while (self.tokenizer.peek_at_next_token() in OPS):
            self._handle_symbol() # op
            self.compile_term() # term

        self.output.append('</expression>') # output </expression>

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
        self.output.append('<term>') # output <term>
        self.tokenizer.advance()
        token_type = self.tokenizer.token_type()
        if token_type == INT_CONST:
            self.output.append("<integerConstant> {} </integerConstant>".format(self.tokenizer.int_val()))
        elif token_type == STRING_CONST:
            self.output.append("<stringConstant> {} </stringConstant>".format(self.tokenizer.string_val()))
        elif token_type == KEYWORD:
            self.output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))
        elif token_type == IDENTIFIER: # varName|varName'['expression']'|subroutineCall
            self.output.append("<identifier> {} </identifier>".format(self.tokenizer.identifier()))
            next_token = self.tokenizer.peek_at_next_token()
            if next_token == '[': # varName'['expression']'
                self._handle_symbol() # '['
                self.compile_expression() # expression
                self._handle_symbol() # ']'
            elif next_token == '(': # subroutineCall
                self._handle_symbol() # '('
                self.compile_expression_list() # expressionList
                self._handle_symbol() # ')'
            elif next_token == '.': # subroutineCall
                self._handle_symbol() # '.'
                self._handle_identifier() # subroutineName
                self._handle_symbol() # '('
                self.compile_expression_list() # expressionList
                self._handle_symbol() # ')'
        elif self.tokenizer.current_token == '(': # '('expression')'
            self.output.append("<symbol> {} </symbol>".format(self.tokenizer.symbol())) # '('
            self.compile_expression() # expression
            self._handle_symbol() # ')'
        elif self.tokenizer.current_token in ['-', '~']: # unaryOp term
            self.output.append("<symbol> {} </symbol>".format(self.tokenizer.symbol()))
            self.compile_term()
        else:
            raise Exception("Token '{}' not matched to any term".format(self.tokenizer.current_token))

        self.output.append('</term>') # output </term>

    def _handle_type(self):
        """ type: 'int'|'char'|'boolean'|className"""
        self.tokenizer.advance()
        if self.tokenizer.current_token in [INT, CHAR, BOOLEAN]:
            self.output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))
        else:
            self.output.append("<identifier> {} </identifier>".format(self.tokenizer.identifier()))

    def _handle_keyword(self):
        self.tokenizer.advance()
        self.output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))

    def _handle_identifier(self):
        self.tokenizer.advance()
        self.output.append("<identifier> {} </identifier>".format(self.tokenizer.identifier()))

    def _handle_symbol(self):
        self.tokenizer.advance()
        self.output.append("<symbol> {} </symbol>".format(self.tokenizer.symbol()))

    def _handle_int_const(self):
        self.tokenizer.advance()
        self.output.append("<integerConstant> {} </integerConstant>".format(self.tokenizer.int_val()))

    def _handle_string_const(self):
        self.tokenizer.advance()
        self.output.append("<stringConstant> {} </stringConstant>".format(self.tokenizer.string_val()))

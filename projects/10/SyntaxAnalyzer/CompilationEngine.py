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

    def compile_class(self):
        """Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.output.append('<class>') # output <class>
        self._handle_keyword() # 'class'
        self._handle_identifier() # className
        self._handle_symbol() # '{'

        # TODO: How to handle multiple classVarDecs? How to handle 0?
        # classVarDec*
        #self.compile_class_var_dec()

        # TODO: subroutineDec*
        #self.compile_subroutine_dec()

        self._handle_symbol() # '}'
        self.output.append('</class>') # output </class>

    def compile_class_var_dec(self):
        """Compiles a static variable declaration,
        or a field declaration.
        classVarDec: ('static'|'field') type varName(',' varName)* ';'
        """
        self.output.append('<classVarDec>') # output <classVarDec>
        self._handle_keyword() # ('static'|'field')
        self._handle_keyword() # type
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
        pass

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list.
        Does not handle the enclosing "()".
        parameterList: ((type varName) (',' type varName)*)?
        """
        pass

    def compile_subroutine_body(self):
        """Compiles a subroutine's body.
        subroutineBody: '{' varDec* statements '}'
        """
        pass

    def compile_var_dec(self):
        """Compiles a var declaration.
        varDec: 'var' type varName (',' varName)* ';'
        """
        self.output.append('<varDec>') # output <varDec>
        self._handle_keyword() # 'var'
        self._handle_keyword() # type
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
        pass

    def compile_let(self):
        """Compiles a let statement.
        letStatement: 'let' varName('[' expression ']')? '=' expression ';'
        """
        self.output.append('<letStatement>') # output <letStatement>
        self._handle_keyword() # 'let'
        self._handle_identifier() # varName
        self._handle_symbol() # '='
        self.compile_expression() # expression
        self._handle_symbol() # ';'
        self.output.append('</letStatement>') # output </letStatement>

    def compile_if(self):
        """Compiles a if statement.
        ifStatement: 'if' '(' expression ')' '{' statements '}'
            ('else' '{' statements '}')?
        """
        pass

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

        # TODO: subroutineCall
        #self.compile_subroutine_call()

        self._handle_symbol() # ';'
        self.output.append('</doStatement>') # output </doStatement>

    def compile_return(self):
        """Compiles a return statement.
        returnStatement: 'return' expression? ';'
        """
        self.output.append('<returnStatement>') # output <returnStatement>
        self._handle_keyword() # 'return'

        if (self.tokenizer.peek_at_next_token() not in SYMBOLS):
            self.compile_expression()

        self._handle_symbol() # ';'
        self.output.append('</returnStatement>') # output </returnStatement>

    def compile_expression(self):
        """Compiles an expression.
        expression: term (op term)*
        """
        self.output.append('<expression>') # output <expression>
        self.compile_term()

        while (self.tokenizer.peek_at_next_token() == '='):
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
        # TODO: handle all types
        self.tokenizer.advance()
        token = self.tokenizer.token_type()
        if token == INT_CONST:
            self.output.append("<integerConstant> {} </integerConstant>".format(self.tokenizer.int_val()))
        elif token == KEYWORD:
            self.output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))
        elif token == IDENTIFIER:
            self.output.append("<identifier> {} </identifier>".format(self.tokenizer.identifier()))
        self.output.append('</term>') # output </term>

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions.
        expressionList: (expression (','expression)* )?
        """
        pass

    def _handle_keyword(self):
        self.tokenizer.advance()
        self.output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))

    def _handle_identifier(self):
        self.tokenizer.advance()
        self.output.append("<identifier> {} </identifier>".format(self.tokenizer.identifier()))

    def _handle_symbol(self):
        self.tokenizer.advance()
        self.output.append("<symbol> {} </symbol>".format(self.tokenizer.symbol()))

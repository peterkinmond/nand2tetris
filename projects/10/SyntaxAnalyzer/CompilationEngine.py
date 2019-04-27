from JackTokenizer import JackTokenizer

class CompilationEngine(object):
    """CompilationEngine: generates the compiler's output."""

    def __init__(self, input_file, output_file):
        """Creates a new compilation engine with the
        given input and output.

        The next routine called must be compile_class
        """
        self.tokenizer = JackTokenizer(input_file)
        self.output_file = output_file
        self.output = []

    def compile_class(self):
        """Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.output.append('<class>') # output <class>
        self.handle_keyword() # 'class'
        self.handle_identifier() # className
        self.handle_symbol() # '{'


        # classVarDec*
        self.compile_class_var_dec()

        # subroutineDec*
        self.compile_subroutine_dec()

        self.handle_symbol() # '}'
        self.output.append('</class>') # output </class>


    def handle_keyword(self):
        if (self.tokenizer.has_more_tokens()):
            self.tokenizer.advance()
            self.output.append("<keyword>{}</keyword>".format(self.tokenizer.keyword()))
        else:
            raise Exception("Can't handle keyword - file has no more tokens")


    def handle_identifier(self):
        if (self.tokenizer.has_more_tokens()):
            self.tokenizer.advance()
            self.output.append("<identifier>{}</identifier>".format(self.tokenizer.identifier()))
        else:
            raise Exception("Can't handle identifier - file has no more tokens")

    def handle_symbol(self):
        if (self.tokenizer.has_more_tokens()):
            self.tokenizer.advance()
            self.output.append("<symbol>{}</symbol>".format(self.tokenizer.symbol()))
        else:
            raise Exception("Can't handle symbol - file has no more tokens")

    def compile_class_var_dec(self):
        """Compiles a static variable declaration,
        or a field declaration.
        classVarDec: ('static'|'field') type varName(',' varName)* ';'
        """
        pass


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
        pass

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
        pass

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
        pass

    def compile_do(self):
        """Compiles a do statement.
        doStatement: 'do' subroutineCall ';'
        """
        pass

    def compile_return(self):
        """Compiles a return statement.
        returnStatement: 'return' expression? ';'
        """
        pass

    def compile_expression(self):
        """Compiles an expression.
        expression: term (op term)*
        """
        pass

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
        pass

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions.
        expressionList: (expression (','expression)* )?
        """
        pass

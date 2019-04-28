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
        self.handle_keyword() # 'class'
        self.handle_identifier() # className
        self.handle_symbol() # '{'

        # TODO: How to handle multiple classVarDecs? How to handle 0?
        # classVarDec*
        self.compile_class_var_dec()

        # subroutineDec*
        self.compile_subroutine_dec()

        self.handle_symbol() # '}'
        self.output.append('</class>') # output </class>


    def handle_keyword(self):
        self.tokenizer.advance()
        self.output.append("<keyword> {} </keyword>".format(self.tokenizer.keyword()))

    def handle_identifier(self):
        self.tokenizer.advance()
        self.output.append("<identifier> {} </identifier>".format(self.tokenizer.identifier()))

    def handle_symbol(self):
        self.tokenizer.advance()
        self.output.append("<symbol> {} </symbol>".format(self.tokenizer.symbol()))

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
        self.output.append('<letStatement>') # output <letStatement>
        self.handle_keyword() # 'let'
        self.handle_identifier() # varName
        self.handle_symbol() # '='

        # expression
        self.compile_expression()

        self.handle_symbol() # ';'
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
        self.output.append('<returnStatement>') # output <returnStatement>
        self.handle_keyword() # 'return'

        # TODO: handle optional expression. How to do?
        # Do conditional here or handle in compile_expression method?
        #self.tokenizer.advance()
        #if (self.tokenizer.token_type != SYMBOL):
        #    self.compile_expression()

        self.handle_symbol() # ';'
        self.output.append('</returnStatement>') # output </returnStatement>

    def compile_expression(self):
        """Compiles an expression.
        expression: term (op term)*
        """
        self.output.append('<expression>') # output <expression>
        self.compile_term()
        # TODO: build out the rest
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
        self.output.append("<integerConstant> {} </integerConstant>".format(self.tokenizer.identifier()))
        self.output.append('</term>') # output </term>

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions.
        expressionList: (expression (','expression)* )?
        """
        pass

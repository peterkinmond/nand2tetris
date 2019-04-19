import re

class JackTokenizer:
    """Ignores all comments and white space in the input stream, and
    serializes it into Jack-language tokens. The token types are specified
    according to the Jack grammar.
    """

    def __init__(self, input_file):
        """Opens the input .jack file and gets ready to tokenize it"""
        text = open(input_file, 'r').read()
        # TODO: How to handle single-line comments if we kill newlines? Probably need to bring them back
        # Since tokens are independent of white space, we
        # treat code file as one long string - convert newlines to spaces
        self.text = text.replace('\r', '').replace('\n', ' ')

        self.pos = 0 # Current position within text
        self.current_char = self.text[self.pos]
        self.current_token = ""

    def has_more_tokens(self):
        """Are there more tokens in the input?"""
        # TODO: Ignore comments, both single line and multi-line
        if self.text[self.pos] != " ":
            return True

        while self.pos < len(self.text):
            self.pos += 1
            self.current_char = self.text[self.pos]
            if self.current_char != " ":
                return True

        return False

    def advance(self):
        """Gets the next token from the input, and makes it the current token.

        This method should be called only if has_more_tokens is true.
        Initially there is no current token.
        """
        self.current_token = ""

        while self.text[self.pos] != " ":
            self.current_char = self.text[self.pos]
            self.current_token += self.current_char
            self.pos += 1

    def token_type(self):
        """Returns the type of the current token as a constant."""
        keywords = ['class', 'constructor', 'function', 'method',
            'field', 'static', 'var', 'int', 'char', 'boolean',
            'void', 'true', 'false', 'null', 'this', 'let', 'do',
            'if', 'else', 'while', 'return']

        symbols = ['{', '}', '(', ')', '[', ']', '. ', ', ', '; ', '+', '-', '*',
            '/', '&', '|', '<', '>', '=', '~']

        if self.current_token in keywords:
            return 'keyword'
        elif self.current_token in symbols:
            return 'symbol'
        elif self.is_identifier(self.current_token):
            return 'identifier'
        else:
            return "Error: token type not found for token '{}'".format(self.current_token)

    def is_identifier(self, token):
        if len(token) == 0:
            return False

        if token[0].isdigit(): # Can't start with digit
            return False

        # Must contain only alphanumeric chars or underscores
        return re.match(r'^\w+$', token)

    def keyword(self):
        """Returns the keyword which is the current token, as a constant.

        This method should be called only if token_type is KEYWORD.
        """
        pass

    def symbol(self):
        """Returns the character which is the current token.

        This method should be called only if token_type is SYMBOL.
        """
        pass

    def identifier(self):
        """Returns the identifier which is the current token.

        This method should be called only if token_type is IDENTIFIER.
        """
        pass

    def int_val(self):
        """Returns the int value of the current token.

        This method should be called only if token_type is INT_CONST.
        """
        pass

    def string_val(self):
        """Returns the string value of the current token, without the
        2 enclosing double quotes.

        This method should be called only if token_type is STRING_CONST.
        """
        pass

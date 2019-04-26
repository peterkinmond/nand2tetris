import re

KEYWORDS = ['class', 'constructor', 'function', 'method',
    'field', 'static', 'var', 'int', 'char', 'boolean',
    'void', 'true', 'false', 'null', 'this', 'let', 'do',
    'if', 'else', 'while', 'return']
SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
    '/', '&', '|', '<', '>', '=', '~']

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
        self.current_token = self.text[self.pos]

        if self.current_token in SYMBOLS: # Symbols are all 1 char so we're done
            self.pos += 1 # Move past current token
            return

        # There are valid cases of 2 tokens "touching" (no white space separation)
        # but they always involve symbols, which need to be treated somewhat
        # specially for that reason. If the next char would "change" a token type,
        # then exit the method since the next char should be a separate token.
        # let x =4; (symbol + identifier + symbol)
        while self.text[self.pos + 1] != " " and self.text[self.pos + 1] not in SYMBOLS:
            self.pos += 1
            self.current_char = self.text[self.pos]
            self.current_token += self.current_char

        self.pos += 1 # Move past current token

    def token_type(self):
        """Returns the type of the current token as a constant."""
        if self.current_token in KEYWORDS:
            return 'keyword'
        elif self.current_token in SYMBOLS:
            return 'symbol'
        elif self.is_identifier(self.current_token):
            return 'identifier'
        elif self.current_token.isdigit():
            return 'integer_constant'
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return 'string_constant'
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

import re
from Constants import *

class JackTokenizer:
    """Ignores all comments and white space in the input stream, and
    serializes it into Jack-language tokens. The token types are specified
    according to the Jack grammar.
    """

    def __init__(self, input_file, use_text_as_input=False):
        """Opens the input .jack file and gets ready to tokenize it"""
        if (use_text_as_input): # Used for testing, pass in a string as input
            text = input_file
        else:
            text = open(input_file, 'r').read()
        self.text = self.remove_comments(text)

        self.pos = 0 # Current position within text
        self.current_char = self.text[self.pos]
        self.current_token = ""

    def remove_comments(self, text):
        # Delete single-line style comments (// ...)
        text = re.sub("//.*\n", '', text)
        # Remove newlines
        text = text.replace('\r', '').replace('\n', ' ')
        # Delete multi-line style comments (/*  */)
        text = re.sub("/\*.*\*/", '', text)

        return text

    def has_more_tokens(self):
        """Are there more tokens in the input?"""
        # Special case for when tokenizer starts - may already be on a token
        if (self.pos == 0) and self.text[self.pos] != " ":
            return True

        # Otherwise try to find a non-white space char (which indicates a token)
        while self.pos < (len(self.text) - 1):
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
        if (self.has_more_tokens() == False):
            raise Exception("File has no more tokens - can't advance")

        self.current_token = self.text[self.pos]

        if self.current_token in SYMBOLS: # Symbols are all 1 char so we're done
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

    def token_type(self):
        """Returns the type of the current token as a constant."""
        if self.current_token in KEYWORDS:
            return KEYWORD
        elif self.current_token in SYMBOLS:
            return SYMBOL
        elif self.is_identifier(self.current_token):
            return IDENTIFIER
        elif self.current_token.isdigit():
            return INT_CONST
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return STRING_CONST
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
        return self.current_token

    def symbol(self):
        """Returns the character which is the current token.

        This method should be called only if token_type is SYMBOL.
        """
        # TODO: Convert <, >, ", and & to &lt;, &gt;, &quot;, &amp;
        return self.current_token

    def identifier(self):
        """Returns the identifier which is the current token.

        This method should be called only if token_type is IDENTIFIER.
        """
        return self.current_token

    def int_val(self):
        """Returns the int value of the current token.

        This method should be called only if token_type is INT_CONST.
        """
        return int(self.current_token)

    def string_val(self):
        """Returns the string value of the current token, without the
        2 enclosing double quotes.

        This method should be called only if token_type is STRING_CONST.
        """
        return self.current_token.replace('"','')

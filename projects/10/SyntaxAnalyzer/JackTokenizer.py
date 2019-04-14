class JackTokenizer

    def __init__(self):
        """Opens the input .jack file and gets ready to tokenize it"""
        pass

    def has_more_tokens(self):
        """Are there more tokens in the input?"""
        pass

    def advance(self):
        """Gets the next token from the input, and makes it the current token.

        This method should be called only if has_more_tokens is true.
        Initially there is no current token.
        """
        pass

    def token_type(self):
        """Returns the type of the current token as a constant."""
        pass

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

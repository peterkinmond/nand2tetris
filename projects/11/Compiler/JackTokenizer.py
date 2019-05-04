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
        text = self.remove_comments(text)

        self.tokens = [] # Will store all tokens
        self.token_index = -1 # Position of current token - start with no token selected
        self.current_token = None # Start with no token selected

        # Parse all the tokens in one pass rather than parsing them as needed. This makes it
        # easier since we don't need to track where we are in the text of the file and makes
        # the logic for methods used by compilation engine (advance, peek_at_next_token)
        # much simpler.
        self.parse_all_tokens(text)

    def remove_comments(self, text):
        # Delete single-line style comments (// ...)
        text = re.sub("//.*\n", '', text)
        # Remove newlines
        text = text.replace('\r', '').replace('\n', ' ').replace('\t', ' ')
        # Delete multi-line style comments (/*  */)
        text = re.sub("/\*.*?\*/", '', text)

        return text

    def parse_all_tokens(self, text):
        pos = 0 # Current position within text
        while pos < len(text):
            if text[pos] == " ": # Ignore whitespace
                pos += 1
                continue

            token = text[pos]
            if token in SYMBOLS: # Symbols are all 1 char so we're done
                self.tokens.append(token)
                pos += 1
                continue

            # There are valid cases of 2 tokens "touching" (no white space separation)
            # but they always involve symbols, which need to be treated somewhat
            # specially for that reason. If the next char would "change" a token type,
            # then exit the method since the next char should be a separate token.
            # let x =4; (symbol + identifier + symbol)
            if token == '"': # String constant to match with closing '"'
                end_pos = text.find('"', pos + 1)
                token = text[pos:end_pos + 1]
                pos = end_pos
            else:
                while text[pos + 1] != " " and text[pos + 1] not in SYMBOLS:
                    pos += 1
                    token += text[pos]

            self.tokens.append(token)
            pos += 1

    def has_more_tokens(self):
        """Are there more tokens in the input?"""
        return self.token_index < len(self.tokens) - 1

    def advance(self):
        """Gets the next token from the input, and makes it the current token.

        This method should be called only if has_more_tokens is true.
        Initially there is no current token.
        """
        if (self.has_more_tokens() == False):
            raise Exception("File has no more tokens - can't advance")

        self.token_index += 1
        self.current_token = self.tokens[self.token_index]

    def peek_at_next_token(self):
        """Peek at the next token without advancing the token index.
        This method is useful to help the CompilationEngine make decisions about
        what elements to compile.
        """
        if (self.has_more_tokens() == False):
            raise Exception("File has no more tokens - can't peek at next token")
        return self.tokens[self.token_index + 1]

    def token_type(self):
        """Returns the type of the current token as a constant."""
        if self.current_token in KEYWORDS:
            return KEYWORD
        elif self.current_token in SYMBOLS:
            return SYMBOL
        elif self.is_identifier():
            return IDENTIFIER
        elif self.current_token.isdigit():
            return INT_CONST
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return STRING_CONST
        else:
            return "Error: token type not found for token '{}'".format(self.current_token)

    def is_identifier(self):
        if len(self.current_token) == 0:
            return False

        if self.current_token[0].isdigit(): # Can't start with digit
            return False

        # Must contain only alphanumeric chars or underscores
        return re.match(r'^\w+$', self.current_token)

    def keyword(self):
        """Returns the keyword which is the current token, as a constant.

        This method should be called only if token_type is KEYWORD.
        """
        return self.current_token

    def symbol(self):
        """Returns the character which is the current token.

        This method should be called only if token_type is SYMBOL.
        """
        # Convert <, >, ", and & to &lt;, &gt;, &quot;, &amp;
        if self.current_token == '<':
            return "&lt;"
        elif self.current_token == '>':
            return "&gt;"
        elif self.current_token == '"':
            return "&quot;"
        elif self.current_token == '&':
            return "&amp;"
        else:
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

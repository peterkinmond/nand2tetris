from Constants import *
from JackTokenizer import *
import unittest

class JackTokenizerTest(unittest.TestCase):
    def test_parse_all_tokens(self):
        tokenizer = JackTokenizer("let x = 4;", True)
        self.assertEqual(len(tokenizer.tokens), 5)

    def test_advance(self):
        """Tests all parts of the tokenizer using this Jack code:

        /** Multi-line comment for
        some class. */
        class A{
          // Single-line comment
          let x = -4;
          do Output.printString("Ring Constants!");
        }

        """
        tokenizer = JackTokenizer("test.jack")
        tokenizer.advance()
        self.assertEqual(tokenizer.keyword(), CLASS)
        self.assertEqual(tokenizer.token_type(), KEYWORD)
        tokenizer.advance()
        self.assertEqual(tokenizer.identifier(), 'A')
        self.assertEqual(tokenizer.token_type(), IDENTIFIER)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), '{')
        self.assertEqual(tokenizer.token_type(), SYMBOL)

        tokenizer.advance()
        self.assertEqual(tokenizer.keyword(), LET)
        self.assertEqual(tokenizer.token_type(), KEYWORD)
        tokenizer.advance()
        self.assertEqual(tokenizer.identifier(), 'x')
        self.assertEqual(tokenizer.token_type(), IDENTIFIER)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), '=')
        self.assertEqual(tokenizer.token_type(), SYMBOL)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), '-')
        self.assertEqual(tokenizer.token_type(), SYMBOL)
        tokenizer.advance()
        self.assertEqual(tokenizer.int_val(), 4)
        self.assertEqual(tokenizer.token_type(), INT_CONST)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), ';')
        self.assertEqual(tokenizer.token_type(), SYMBOL)

        tokenizer.advance()
        self.assertEqual(tokenizer.keyword(), DO)
        self.assertEqual(tokenizer.token_type(), KEYWORD)
        tokenizer.advance()
        self.assertEqual(tokenizer.identifier(), 'Output')
        self.assertEqual(tokenizer.token_type(), IDENTIFIER)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), '.')
        self.assertEqual(tokenizer.token_type(), SYMBOL)
        tokenizer.advance()
        self.assertEqual(tokenizer.identifier(), 'printString')
        self.assertEqual(tokenizer.token_type(), IDENTIFIER)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), '(')
        self.assertEqual(tokenizer.token_type(), SYMBOL)
        tokenizer.advance()
        self.assertEqual(tokenizer.string_val(), 'Ring Constants!')
        self.assertEqual(tokenizer.token_type(), STRING_CONST)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), ')')
        self.assertEqual(tokenizer.token_type(), SYMBOL)
        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), ';')
        self.assertEqual(tokenizer.token_type(), SYMBOL)

        tokenizer.advance()
        self.assertEqual(tokenizer.symbol(), '}')
        self.assertEqual(tokenizer.token_type(), SYMBOL)

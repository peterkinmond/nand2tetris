import JackTokenizer
import unittest

class JackTokenizerTest(unittest.TestCase):
    def test_tokenizer(self):
        tokenizer = JackTokenizer.JackTokenizer("test.jack")
        tokenizer.has_more_tokens()
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token, 'class')
        self.assertEqual(tokenizer.token_type(), 'keyword')
        tokenizer.has_more_tokens()
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token, 'A')
        self.assertEqual(tokenizer.token_type(), 'identifier')
        tokenizer.has_more_tokens()
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token, '{')
        self.assertEqual(tokenizer.token_type(), 'symbol')
        tokenizer.has_more_tokens()
        tokenizer.advance()
        self.assertEqual(tokenizer.current_token, '}')
        self.assertEqual(tokenizer.token_type(), 'symbol')

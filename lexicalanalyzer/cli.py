from lexer import Lexer
import sys

if len(sys.argv) > 1:
    lexer = Lexer()
    tokens = lexer.test_lex(sys.argv[1])
    print(tokens)
else:
    print('Use: python3 cli.py <line>')
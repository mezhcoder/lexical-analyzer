from lexer import Lexer
import sys

lexer = Lexer()
tokens = lexer.tokenize('program Test; var x: integer; begin x := 2+3*4; end.')
print('\n'.join(str(token) for token in tokens))
# if len(sys.argv) > 1:
#     lexer = Lexer()
#     tokens = lexer.test_lex('program foo; var x, y: integer; begin end')
#     print(tokens)
# else:
#     print('Use: python3 cli.py <line>')